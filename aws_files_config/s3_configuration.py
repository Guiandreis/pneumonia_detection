import boto3
import os
import aws_files_config.aws_settings as aws_settings

def check_bucket_existence(s3_client, name_s3_client = ''):
    '''This function list all existing buckets and check for existent one'''
    buckets = s3_client.list_buckets()['Buckets']
    
    BUCKET_ALREADY_EXISTS = False
    for bucket in buckets:

        if bucket['Name'] == name_s3_client:
            BUCKET_ALREADY_EXISTS = True

        print('bucket',bucket)

    return BUCKET_ALREADY_EXISTS

def create_bucket(s3_client, name_s3_bucket= ''):
    '''Create bucket if desired one doesnt exists'''

    print('name_s3_bucket',name_s3_bucket)
    s3_client.create_bucket(
        Bucket = name_s3_bucket, 
        )

    print(f'bucket created with name {name_s3_bucket}')

    return

def list_folders_in_bucket(s3_client, NAME_S3_BUCKET):
    '''this function list all the folders in the bucket'''

    folders_list = s3_client.list_objects(
        Bucket = NAME_S3_BUCKET, Delimiter = '/'
        )
    if "CommonPrefixes" in folders_list:
        existent_folders = [
            folder['Prefix'] for folder in folders_list['CommonPrefixes']]
        
        return existent_folders
    else:
        return []

def check_if_required_folders_exists_ifnot_create(
    s3_client, NAME_S3_BUCKET, existent_folders, folders_required
    ):
    '''This function verify if all folders exists, if not create them'''

    for folder in folders_required:
        if folder not in existent_folders:
            s3_client.put_object(Bucket = NAME_S3_BUCKET, Key = f"{folder}/" )
            print(f"Folder {folder} created.")

    return

def read_configuration_folder_files_and_upload():
    '''This functions read files inside configuration folder and upload any
    missing file'''

    return


def check_if_configuration_files_if_not_upload(
    s3_client, NAME_S3_BUCKET, 
    s3_files_folder, config_folder_s3
        ):

    files_for_upload = os.listdir(s3_files_folder + '/')
    files_listed_in_bucket = s3_client.list_objects(
        Bucket = NAME_S3_BUCKET, Prefix = config_folder_s3 +'/'
        )

    #print(files_listed_in_bucket[''])
    files_in_s3_config = [
        obj["Key"].split('/')[-1] for obj in files_listed_in_bucket.get("Contents",
         []) if not obj["Key"].endswith("/")]

    print('files',files_in_s3_config)
    print('files_for_upload',files_for_upload)
    
    for file in files_for_upload:
        if file not in files_in_s3_config:
            with open(s3_files_folder + '/' + file, 'rb') as data:
                s3_client.upload_fileobj(
                    data, NAME_S3_BUCKET, config_folder_s3 + '/' + file)

    return

def s3_config(dict_input_info_s3): 

    s3_client = boto3.client(
        's3', region_name = dict_input_info_s3['bucket_region']
        )
    BUCKET_ALREADY_EXISTS = check_bucket_existence(s3_client)

    if not BUCKET_ALREADY_EXISTS:
        print('BUCKET_ALREADY_EXISTS',BUCKET_ALREADY_EXISTS)
        create_bucket(s3_client,  dict_input_info_s3['NAME_S3_BUCKET']
        )

    existent_folders= list_folders_in_bucket(
        s3_client, dict_input_info_s3['NAME_S3_BUCKET'] 
        )

    check_if_required_folders_exists_ifnot_create(
        s3_client, dict_input_info_s3['NAME_S3_BUCKET'], 
        existent_folders, dict_input_info_s3['folders_required']
        )

    check_if_configuration_files_if_not_upload(
        s3_client, dict_input_info_s3['NAME_S3_BUCKET'], 
        dict_input_info_s3['s3_files_folder'], 
        dict_input_info_s3['folders_required'][0]
        )

    
    return s3_client
'''
if __name__ == "__main__":

    dict_input_info_s3, dict_input_info_ec2 = aws_settings.configurations()


    s3_config(dict_input_info_s3)
'''