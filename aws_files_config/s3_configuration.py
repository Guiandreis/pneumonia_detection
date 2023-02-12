import boto3

def list_buckets(s3_client, name_s3_client = ''):

    buckets = s3_client.list_buckets()['Buckets']
    
    BUCKET_ALREADY_EXISTS = False
    for bucket in buckets:

        if bucket['Name'] == name_s3_client:
            BUCKET_ALREADY_EXISTS = True

        print('bucket',bucket)

    return BUCKET_ALREADY_EXISTS

s3_client = boto3.client('s3')

list_buckets(s3_client)

def create_bucket(s3_client, name_s3_bucket= ''):

    print('name_s3_bucket',name_s3_bucket)
    s3_client.create_bucket(
        Bucket = name_s3_bucket, 
        )

    print(f'bucket created with name {name_s3_bucket}')

    return

def call_methods():

    bucket_region = 'us-east-1'
    name_s3_bucket = 'gra-porfolio-bucket2'

    s3_client = boto3.client('s3', region_name = bucket_region)
    BUCKET_ALREADY_EXISTS = list_buckets(s3_client)

    if not BUCKET_ALREADY_EXISTS:
        print('BUCKET_ALREADY_EXISTS',BUCKET_ALREADY_EXISTS)
        create_bucket(s3_client,  name_s3_bucket)

    return
#if __name__ == "__main__":
#    call_methods()
