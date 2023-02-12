import boto3
import os


def set_params_as_dict():
    '''Function of input parameter to determine instance name, id, type
    key pair, region etc...'''
    
    dict_create_instance= {
        'INSTANCE_NAME' : 'pneumonia_detection',
        'AMI_ID' : 'ami-0557a15b87f6559cf', ##free tier UBUNTU 20.04
        'INSTANCE_TYPE' : 't2.micro', ##free tier,
        'USER_DATA' : "#!bin/bash mk",
        'KEY_PAIR_NAME' : 'pneumonia_key_pair',#pneumonia_key_pair nometeste
        'AWS_REGION' : 'us-east-1',

    }

    return dict_create_instance

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
            print('exists locally ') 
            return

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

    return


def get_list_instances_and_start_selected(ec2_resource, INSTANCE_NAME):
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

            #if state is pending wait until running
            if state == 'pending':
                instance[0].wait_until_running()
                print(f'instance {INSTANCE_NAME} is running',)

            #if state is stopped wait until running
            elif state == 'stopped':
                instance.start()
                instance.wait_until_running()
                print(f'instence {INSTANCE_NAME} is running')
            
            #if state is terminated there is no instance
            elif state == 'shutting-down':
                instance.wait_until_terminated()
                there_is_instance = False
                print(f'instence {INSTANCE_NAME} is terminated')

            #if state is terminated there is no instance
            elif state == 'terminated':
                there_is_instance = False
                print(f'instence {INSTANCE_NAME} is terminated')

    return there_is_instance, correct_instance

def create_new_instance( EC2_RESOURCE, dict_create_instance):
    ''' Function to create new instance if there is none by the input name'''
    
    AMI_ID = dict_create_instance['AMI_ID']
    INSTANCE_NAME = dict_create_instance['INSTANCE_NAME']
    INSTANCE_TYPE = dict_create_instance['INSTANCE_TYPE']
    USER_DATA = dict_create_instance['USER_DATA']
    KEY_PAIR_NAME = dict_create_instance['KEY_PAIR_NAME'] 

    instance = EC2_RESOURCE.create_instances(
        MinCount = 1, # número mínimo de instâncias pra criar
        MaxCount = 1, # número máximo de instâncias pra criar
        ImageId = AMI_ID,
        InstanceType = INSTANCE_TYPE,
        KeyName = KEY_PAIR_NAME,
        UserData = USER_DATA,
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
    
    print('initializing instance', instance)
    instance[0].wait_until_running()
    print('instance initialized')

    return instance[0]

def configure_new_instance():
    '''Function to configure including downloading files from s3 and 
    installing required libraires'''

    return

def stop_instance(instance):
    '''Function to stop instances that are running'''

    state = instance.state['Name']
    print('state',state)
    instance.stop()
    instance.wait_until_stopped()
    print('instance stopped')

    return


def ec2_config():

    dict_create_instance = set_params_as_dict()

    ec2_client = boto3.client(
        'ec2', region_name = dict_create_instance['AWS_REGION']
        )

    ec2_resource = boto3.resource(
        'ec2', region_name = dict_create_instance['AWS_REGION']
        )
        
    find_or_create_key_pair_locally(
        ec2_client,dict_create_instance['KEY_PAIR_NAME']
        )

    there_is_instance, correct_instance = get_list_instances_and_start_selected(
        ec2_resource,dict_create_instance['INSTANCE_NAME']
        )
    
    if not there_is_instance:
        correct_instance = create_new_instance(
            ec2_resource, dict_create_instance
            )
            
        #configure_new_instance(

        #)

    if correct_instance != None:
        stop_instance(correct_instance)
    return
    
if __name__ == "__main__":
    ec2_config()
    