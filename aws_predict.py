from aws_files_config import aws_settings, ec2_configuration, s3_configuration
import boto3
import os
import io

def aws_configuration(dict_input_info_s3, dict_input_info_ec2):
    '''This function call the files to configure EC2 and S3'''

    client_paramiko, sftp, correct_instance = ec2_configuration.ec2_config(
    dict_input_info_s3, dict_input_info_ec2)

    s3_client = s3_configuration.s3_config(dict_input_info_s3)

    return client_paramiko, sftp, correct_instance, s3_client

def upload_exam_to_s3(s3_client, folder_s3, name_s3_bucket, file_storage, name):
    '''This function upload file to s3 bucket'''

    file_path = folder_s3 +'/'+ name
    s3_client.put_object(
        Bucket = name_s3_bucket, Key= file_path, Body = file_storage)

    return file_path

def exam_process(s3_client, client_paramiko, sftp, bucket_name , file_path, name):
    '''This function process the exam using paramiko'''

    ec2_path_input = '/home/ubuntu/pneumonia/input/' + name

    name_json_file = name.split('.')[0] + '.json'
    ec2_path_output = '/home/ubuntu/pneumonia/output/' + name_json_file
    file_obj = io.BytesIO()
    s3_client.download_fileobj(bucket_name, file_path  , file_obj)
    file_obj.seek(0)

    sftp.putfo(file_obj,ec2_path_input)

    stdin, stdout, stderr = client_paramiko.exec_command('python3 /home/ubuntu/pneumonia/preprocess_and_predict_aws.py')
    client_paramiko.exec_command('rm -rf /home/ubuntu/pneumonia/output')
    client_paramiko.exec_command('mkdir /home/ubuntu/pneumonia/output')
    stdout.channel.recv_exit_status()
    print(stderr.read().decode())
    print('ec2_path_output',ec2_path_output)
    output_json = sftp.open(ec2_path_output)
    output = output_json.read()

    return output, name_json_file

def aws_call_predictions(file_storage, name):
    '''The main function on this file'''
    
    dict_input_info_s3, dict_input_info_ec2 = aws_settings.configurations()

    client_paramiko, sftp, correct_instance, s3_client = aws_configuration(
        dict_input_info_s3, dict_input_info_ec2)

    file_path = upload_exam_to_s3(
        s3_client, dict_input_info_s3['folders_required'][1], 
        dict_input_info_s3['NAME_S3_BUCKET'], file_storage, name)

    output, name_json_file = exam_process(s3_client,
        client_paramiko, sftp, dict_input_info_s3['NAME_S3_BUCKET'], 
        file_path, name)

    upload_exam_to_s3(
            s3_client, dict_input_info_s3['folders_required'][2], 
            dict_input_info_s3['NAME_S3_BUCKET'], output, name_json_file)

    client_paramiko.close()
    ec2_configuration.stop_instance(correct_instance)
    
    return output
