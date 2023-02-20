import boto3
import os
import paramiko
import time
import aws_files_config.aws_settings as aws_settings

def find_or_create_key_pair_locally(ec2_client, KEY_PAIR_NAME):
    '''Function to find or create new key_pair if it doesnt exists locally'''

    relative_path_key_pair = 'key_pair_files/' + KEY_PAIR_NAME + '.pem'

    #Check if the key pair exists remotely if yes stores
    exists_remotely = False
    try:
        exists_remotely = ec2_client.describe_key_pairs(
            KeyNames=[KEY_PAIR_NAME]
            )
    except:
        exists_remotely = exists_remotely

    #if exists remotely check the key pair exists locally 
    if exists_remotely:
        exists_locally = os.path.exists(relative_path_key_pair)

        # if exists returns 
        if exists_locally:
            print('exists locally') 
            return relative_path_key_pair

        #if not deletes it remotely since we cannot download it anymore and
        #call again the function
        else:
            print('key pair deleted, created again and downloaded')
            ec2_client.delete_key_pair(KeyName=KEY_PAIR_NAME)
            find_or_create_key_pair_locally(ec2_client, KEY_PAIR_NAME)

    #Create a new key pair and stores it
    else:
        print('doesnt exist')
        KEY_PAIR = ec2_client.create_key_pair(KeyName = KEY_PAIR_NAME)
        with open(relative_path_key_pair, 'w') as key_file:
            key_file.write(KEY_PAIR['KeyMaterial'])

    return relative_path_key_pair

def list_instances_and_start_selected(ec2_resource, INSTANCE_NAME):
    '''Function to list instances and start selected one by name'''

    there_is_instance = False
    correct_instance = None
    instances = ec2_resource.instances.all()

    #Check all listed instances
    for instance in instances:

        #if instance name is in list check status
        if instance.tags[0]['Value'] == INSTANCE_NAME:
            print('instance',instance)
            there_is_instance = True
            state = instance.state['Name']
            print('state',state)
            correct_instance = instance

            #if is running continue
            if state == 'running':
                return there_is_instance, correct_instance

            #if state is pending wait until running  
            elif state == 'pending':
                print('entrou state pendente')
                instance.wait_until_running()
                print(f'instance {INSTANCE_NAME} is running state {instance.state["Name"]}')
                return there_is_instance, correct_instance

            #if state is stopped wait until running
            elif state == 'stopped':
                instance.start()
                instance.wait_until_running()
                print(f'instance {INSTANCE_NAME} is running state')
            
            #if state is terminated there is no instance
            elif state == 'shutting-down':
                instance.wait_until_terminated()
                there_is_instance = False
                print(f'instance {INSTANCE_NAME} is terminated')

            #if state is terminated there is no instance
            elif state == 'terminated':
                there_is_instance = False
                print(f'instance {INSTANCE_NAME} is terminated')

    return there_is_instance, correct_instance

def create_new_instance( ec2_resource, ec2_client, dict_create_instance):
    ''' Function to create new instance if there is none by the input name'''
    
    AMI_ID = dict_create_instance['AMI_ID']
    INSTANCE_NAME = dict_create_instance['INSTANCE_NAME']
    INSTANCE_TYPE = dict_create_instance['INSTANCE_TYPE']
    USER_DATA = dict_create_instance['USER_DATA']
    KEY_PAIR_NAME = dict_create_instance['KEY_PAIR_NAME'] 

    security_group_name = 'standard_security_group'
    try:
        existent_security = ec2_client.describe_security_groups(
            GroupNames=[security_group_name]
            )

        if len(existent_security['SecurityGroups']) > 0:
            security_group_id = existent_security['SecurityGroups'][0]['GroupId']
            ec2_client.delete_security_group(GroupId=security_group_id)
        
    except:
        print('doesnt exists this security group')

    security_group = ec2_resource.create_security_group(
        GroupName= security_group_name,
        Description='Standard security group for SSH access'
    )
    security_group.authorize_ingress(
    IpPermissions=[
        {
            'FromPort': 22,
            'ToPort': 22,
            'IpProtocol': 'TCP',
            'IpRanges': [
                {
                    'CidrIp': '0.0.0.0/0'
                }
            ]
        }
    ]
    )

    instances = ec2_resource.create_instances(
        MinCount = 1, # número mínimo de instâncias pra criar
        MaxCount = 1, # número máximo de instâncias pra criar
        ImageId = AMI_ID,
        InstanceType = INSTANCE_TYPE,
        KeyName = KEY_PAIR_NAME,
        UserData = USER_DATA,
        SecurityGroups = [
            security_group.group_name
        ],
        TagSpecifications = [
            {
                'ResourceType' : 'instance',
                'Tags' : [
                    {
                        'Key':'Name',
                        'Value': INSTANCE_NAME
                    },
                ]
            },
        ]
    )

    instances[0].wait_until_running()

    # Get the instance status
    instance_status = instances[0].state['Name']
    print('instance_status',instance_status)
    # Verify that the instance is running
    while instance_status != 'running':
        instance = ec2_resource.Instance(instances[0].id)
        instance_status = instance.state['Name']
        print(f"Instance status: {instance_status}")
        time.sleep(10)

    print(f"Instance is now running: {instances[0].id}")
    return instances[0]

def connect_to_instance(correct_instance, relative_path_key_pair):
    print('conenct to paramiko')
    print('correct_instance',correct_instance)
    print('relative_path_key_pair',relative_path_key_pair)
    print('correct_instance.platform ',correct_instance.platform )
    print('dns',correct_instance.public_dns_name)
    print('ipadress 1',correct_instance.public_ip_address)

    ip_publico = correct_instance.public_ip_address
    dns = correct_instance.public_dns_name
    conection_username = "ubuntu"
 
    client_paramiko = paramiko.SSHClient()
    client_paramiko.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client_paramiko.connect(dns, username=conection_username, 
    pkey=paramiko.RSAKey.from_private_key_file(relative_path_key_pair))

    return client_paramiko


def verify_files_in_instance_to_configure(client_paramiko):
    # Execute commands on the remote host

    stdin, stdout_folder, stderr = client_paramiko.exec_command('ls {}'.
        format('/home/ubuntu'))

    stdin, stdout_files, stderr = client_paramiko.exec_command('ls {}'.
        format('/home/ubuntu/pneumonia'))

    instance_configured = False
    folders_existent = []
    output_folder = stdout_folder.readlines()

    for line in output_folder:
        print('line strip folder',line.strip())
        folders_existent.append(line.strip())

    files_existent = []
    output_files = stdout_files.readlines()

    for line in output_files:
        print('line strip files',line.strip())
        files_existent.append(line.strip())

    if 'pneumonia' not in folders_existent:
        print('doesnt exists folder not configured')

    else: 
        print('folder exists')
        import glob

        files_required = glob.glob('s3_upload_files/*')
        #files_required = []
        print('files_required',files_required,'files_existent',files_existent)

        if all(elem in files_existent for elem in files_required):
            print('files doesnt exists')

        else:
            print('all files exists',files_existent)
            instance_configured = True

    return instance_configured


def download_files_from_s3(dict_input_info_s3, client_paramiko):
    bucket_name = dict_input_info_s3['NAME_S3_BUCKET']#'gra-portfolio-bucket'
    bucket_folder  = dict_input_info_s3['folders_required'][0]#'config_folder/'
    client_paramiko.exec_command('mkdir pneumonia')
    client_paramiko.exec_command('mkdir pneumonia/input')
    client_paramiko.exec_command('mkdir pneumonia/output')
    sftp = client_paramiko.open_sftp()

    #sftp.mkdir('pneumonia')
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=bucket_folder + '/'):
        if not obj.key.endswith('/'):
            print('obj',obj)
            file_name = os.path.basename(obj.key)
            bucket.download_file(obj.key, file_name)
            sftp.put(file_name, f'/home/ubuntu/pneumonia/{file_name}')
            os.remove(file_name)
    #s3_client = boto3.client('s3')
    #s3_client.download_file('gra-portfolio-bucket')

    return sftp

def execute_config_files(client_paramiko):
    stdin, stdout, stderr = client_paramiko.exec_command('sudo apt-get update && sudo apt-get install python3-pip -y')
    output = stdout.read().decode()
    print('output install pip',output)

    stdin, stdout, stderr = client_paramiko.exec_command('cd /home/ubuntu/pneumonia && sudo pip install -r aws_requirements.txt --no-cache-dir')
    output = stdout.read().decode()
    print('output install requirements',output)
    

    return  

def configure_instance(
    dict_input_info_s3, correct_instance, relative_path_key_pair
    ):
    '''Function to configure including downloading files from s3 and 
    installing required libraires'''

    client_paramiko = connect_to_instance(
        correct_instance, relative_path_key_pair
        )
    is_instance_configured = verify_files_in_instance_to_configure(
        client_paramiko
        )

    if not is_instance_configured:
        sftp = download_files_from_s3(dict_input_info_s3, client_paramiko )
        execute_config_files(client_paramiko)
        print('not configured')
    
    else:
        sftp = client_paramiko.open_sftp()
        print('instance already configured')
        
    #client_paramiko.close()
    return client_paramiko, sftp
        
def stop_instance(instance):
    '''Function to stop instances that are running'''

    state = instance.state['Name']
    print('state',state)
    instance.stop()
    instance.wait_until_stopped()
    print('instance stopped')

    return

def ec2_config(dict_input_info_s3, dict_input_info_ec2):

    ec2_client = boto3.client(
        'ec2', region_name = dict_input_info_ec2['AWS_REGION']
        )

    ec2_resource = boto3.resource(
        'ec2', region_name = dict_input_info_ec2['AWS_REGION']
        )
        
    relative_path_key_pair = find_or_create_key_pair_locally(
        ec2_client,dict_input_info_ec2['KEY_PAIR_NAME']
        )

    there_is_instance, correct_instance = list_instances_and_start_selected(
        ec2_resource,dict_input_info_ec2['INSTANCE_NAME']
        )
        
    if not there_is_instance:

        correct_instance = create_new_instance(
            ec2_resource, ec2_client, dict_input_info_ec2
            )#

        there_is_instance, correct_instance = list_instances_and_start_selected(
            ec2_resource,dict_input_info_ec2['INSTANCE_NAME']
            )

    client_paramiko, sftp = configure_instance(
        dict_input_info_s3, correct_instance, relative_path_key_pair
        )

    print('dns',correct_instance.public_dns_name)

    #if correct_instance != None:
    #    stop_instance(correct_instance)

    return client_paramiko, sftp
    
'''
if __name__ == "__main__":

    dict_input_info_s3, dict_input_info_ec2 = aws_settings.configurations()
    client_paramiko = ec2_config(dict_input_info_s3, dict_input_info_ec2)
'''    