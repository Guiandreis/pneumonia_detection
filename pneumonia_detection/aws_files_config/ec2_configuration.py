from attrs import define
from typing  

@define
class configure_instance(EC2Instance):

    there_is_instance: bool = False
    correct_instance : str = None
    exists_remotely : bool = False
    security_group_name: str
    instance_configured: False
    relative_path_key_pair: str

    def _find_or_create_key_pair_locally(self) -> None:
        return

    def _list_instances_and_start_selected(self) -> None:
        return

    def _connect_to_instance(self) -> None:

        return

    def _verify_files_in_instance_to_configure(self) -> None:
    
        return
    
    def _download_files_from_s3(self) -> None:

        return

    def _execute_config_files(self) -> None:
        '''Execute files and commands to config the instance'''

    def _configure_instance(self) -> None:

        return

    def _stop_instance(self) -> None:

        state = instance.state['Name']
        instance.stop()
        instance.wait_until_stopped()
        
    
    def ec2_config(self) -> None:

        return
    
@define 
class EC2Instance:

    security_group_name: str = 'standard_security_group'


    def _create_security_group(self) -> None:

        try:
            existent_security = ec2_client.describe_security_groups(
                GroupNames=[self.security_group_name]
                )

            if len(existent_security['SecurityGroups']) > 0:
                security_group_id = existent_security['SecurityGroups'][0]['GroupId']
                ec2_client.delete_security_group(GroupId=security_group_id)
            
        except:
            print('doesnt exists this security group')

        security_group = ec2_resource.create_security_group(
            GroupName= self.security_group_name,
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
        self.security_group = security_group

    def create_new_instance(self, ec2_resource, ec2_client, dict_create_instance):
        ''' Function to create new instance if there is none by the input name'''
        
        AMI_ID = dict_create_instance['AMI_ID']
        INSTANCE_NAME = dict_create_instance['INSTANCE_NAME']
        INSTANCE_TYPE = dict_create_instance['INSTANCE_TYPE']
        USER_DATA = dict_create_instance['USER_DATA']
        KEY_PAIR_NAME = dict_create_instance['KEY_PAIR_NAME'] 

        instances = ec2_resource.create_instances(
            MinCount = 1, # número mínimo de instâncias pra criar
            MaxCount = 1, # número máximo de instâncias pra criar
            ImageId = AMI_ID,
            InstanceType = INSTANCE_TYPE,
            KeyName = KEY_PAIR_NAME,
            UserData = USER_DATA,
            SecurityGroups = [
                self.security_group.group_name
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

        # Verify that the instance is running
        while instance_status != 'running':
            instance = ec2_resource.Instance(instances[0].id)
            instance_status = instance.state['Name']
            print(f"Instance status: {instance_status}")
            time.sleep(10)

        print(f"Instance is now running: {instances[0].id}")

        return instances[0]