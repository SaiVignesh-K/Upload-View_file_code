import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
import random
import string
import base64

# Initialize a session using Amazon DynamoDB
session = boto3.Session(
    aws_access_key_id='#yourkey',
    aws_secret_access_key='#yourkey',
    region_name='#yourregion'
    )

bucket_name = '#yourbucketname'

def generate_random_name():
    letters = ''.join(random.choices(string.ascii_letters, k=5))
    digits = ''.join(random.choices(string.digits, k=5))
    return letters + digits

def name_exists_in_s3(s3, bucket_name, file_name):
    try:
        s3.head_object(Bucket=bucket_name, Key=file_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise

Allowed_file_types={'jpg','jpeg','png','txt','pdf','svg'}

def get_file_type(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Allowed_file_types

def upload_file(event):
    try:
        # Get the file name from the event
        file_name=event['params']['header']['filename']
        if file_name == '':
            return "Error: No file name provided"
        
        if not allowed_file(file_name):
            return "Error: File type not allowed"

        # Get the file content from the event
        encoded_file_content = str(event['body'])
        file_content = base64.b64decode(encoded_file_content)

        # Create an S3 client
        s3 = session.client('s3')

        # Generate a random name
        new_file_name = 'test/' + generate_random_name() +'.'+ get_file_type(file_name)
        while name_exists_in_s3(s3, bucket_name, new_file_name):
            new_file_name = 'test/' + generate_random_name() +'.'+ get_file_type(file_name)

        # Upload the file with the generated name
        s3.put_object(Bucket=bucket_name, Key=new_file_name, Body=file_content)

        return {
            'resType': 'success',
            'resTitle': 'new_file_name',
            'resMessage': new_file_name
        }
    
    except NoCredentialsError:
        return "Credentials not available"
    
    except PartialCredentialsError:
        return "Partial Credentials available"
    except ClientError as e:
        return "Error: " + str(e)
    except Exception as e:
        return "Error: " + str(e)
    
view_bucket_name = '#yourbucketname'
cloudfront_url_prefix = "#yourcloudfronturl"

def view_file(event):
    try:
        # Get the file name from the event
        file_name=event['params']['header']['filename']
        if file_name == '':
            return 'Error: No file name provided'

        # Create an S3 client
        s3 = session.client('s3')
        if not name_exists_in_s3(s3, view_bucket_name, 'test/' + file_name):
            return "Error: File does not exist"

        # Send CloudFront file URL if file exists
        clf_url = cloudfront_url_prefix + file_name

        return {
            'resType': 'success',
            'resTitle': 'file_url',
            'resMessage': clf_url
        }
    
    except NoCredentialsError:
        return "Credentials not available"
    
    except PartialCredentialsError:
        return "Partial Credentials available"
    except ClientError as e:
        return "Error: " + str(e)
    except Exception as e:
        return "Error: " + str(e)