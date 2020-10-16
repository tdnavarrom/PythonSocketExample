import os
import uuid
from bucket import Bucket

root_directory = "buckets"
parent_dir = os.getcwd()

def create_bucket():
    current_id = str(uuid.uuid4())[:5]
    path = os.path.join(parent_dir, root_directory, str(current_id))
    os.mkdir(path)
    return True

def delete_bucket(bucket):
    try:
        os.rmdir(os.path.join(parent_dir, root_directory, bucket))
    except:
        return False

    return True

def list_buckets():
    path = os.path.join(parent_dir, root_directory)
    directories = os.listdir(path)
    
    result = 'List of buckets\n'
    for directory in directories:
        result += '-> ' + str(directory) + '\n'     
    return(result)
    
