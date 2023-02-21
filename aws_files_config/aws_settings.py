def set_params_as_dict():
    '''Function of input parameter to determine instance name, id, type
    key pair, region etc...'''
    
    dict_create_instance= {
        'INSTANCE_NAME' : 'pneumonia_detection',
        'AMI_ID' : 'ami-09cd747c78a9add63', ##free tier UBUNTU 20.04
        'INSTANCE_TYPE' : 't2.micro', ##free tier,
        'USER_DATA' : "#!bin/bash mk",
        'KEY_PAIR_NAME' : 'pneumonia_key_pair',#pneumonia_key_pair nometeste
        'AWS_REGION' : 'us-east-1',

    }

    return dict_create_instance

def input_paths_and_names():
    '''This function is the input data for all the info and paths'''

    dict_input_info = {
        'bucket_region' : 'us-east-1',
        'NAME_S3_BUCKET' : 'gra-portfolio-bucket',
        'folders_required' : ['config_folder', 'input_folder', 'output_folder'],
        's3_files_folder' : 's3_upload_files'

    }
    return dict_input_info 

def configurations():
    '''This is the main function of as settings'''
    
    dict_input_info_s3 = input_paths_and_names()

    dict_input_info_ec2 = set_params_as_dict()  
    
    return dict_input_info_s3, dict_input_info_ec2