from aws_files_config import aws_settings, ec2_configuration, s3_configuration
import boto3
import os
import io
def aws_configuration(dict_input_info_s3, dict_input_info_ec2):

    client_paramiko, sftp = ec2_configuration.ec2_config(
    dict_input_info_s3, dict_input_info_ec2
    )

    s3_client = s3_configuration.s3_config(dict_input_info_s3)

    return client_paramiko, sftp, s3_client

def upload_exam_to_s3(s3_client, folder_s3, name_s3_bucket, file_storage, name):

    file_path = folder_s3 +'/'+ name
    print('file_path',file_path,'name',name)
    s3_client.put_object(
        Bucket = name_s3_bucket, Key= file_path, Body = file_storage)

    return file_path

def exam_process(s3_client, client_paramiko, sftp, bucket_name, bucket_folder , file_path, name):

    ec2_path = '/home/ubuntu/pneumonia/input/' + name
    file_obj = io.BytesIO()
    s3_client.download_fileobj(bucket_name, file_path  , file_obj)
    file_obj.seek(0)

    sftp.putfo(file_obj,ec2_path)

    client_paramiko.exec_command('python3 /home/ubuntu/pneumonia/preprocess_and_predict_aws.py')

    return

def aws_call_predictions(file_storage, name):

    dict_input_info_s3, dict_input_info_ec2 = aws_settings.configurations()

    client_paramiko, sftp, s3_client = aws_configuration(
        dict_input_info_s3, dict_input_info_ec2)

    file_path = upload_exam_to_s3(
        s3_client, dict_input_info_s3['folders_required'][1], 
        dict_input_info_s3['NAME_S3_BUCKET'], file_storage, name)

    exam_process(s3_client,
        client_paramiko, sftp, dict_input_info_s3['NAME_S3_BUCKET'], dict_input_info_s3['folders_required'][1],
        file_path, name)

    return
