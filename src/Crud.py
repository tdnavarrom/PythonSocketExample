import os
import uuid
import time
from threading import Thread
import Server as s
import Lexer as lx

root_directory = "buckets"
parent_dir = os.getcwd()

def list_buckets():
    path = os.path.join(parent_dir, root_directory)
    directories = os.listdir(path)

    result = 'List of buckets:\n'
    if len(directories) > 0:
        for directory in directories:
            result += '-> ' + str(directory) + '\n'     
        return(str(result))
    else:
        result += '--There are no buckets--\n'
        return result

def open_bucket(bucket):
    try:
        path = os.path.join(parent_dir, root_directory, bucket)

        result = 'List of files in bucket: ' + bucket + '\n'
        for (_, _, filenames) in os.walk(path):
            if len(filenames) > 0:
                for filename in filenames:
                    result += '-> ' + str(filename) + '\n'
            else:
                result += '--There are no files--\n'
        return result
    except:
        return 'Error, the bucket may no exist!\n'

def create_bucket():
    current_id = str(uuid.uuid4())[:5].upper()
    path = os.path.join(parent_dir, root_directory, current_id)
    os.mkdir(path)

def delete_bucket(bucket):
    try:
        path = os.path.join(parent_dir, root_directory, bucket)
        os.rmdir(path)
    except:
        return 'Error, the folder doesn`t exists or may contains files.\n'
    return 'Bucket Removed Successfully!\n'

def do_operation(client, command):
    if command == 'ls_bkt':
        return list_buckets()
    elif command == 'create_bkt':
        create_bucket()
        return 'Bucket Created Successfully!\n'
    elif 'rm_bkt' in command:
        try:
            bucket_to_delete = command.split(' ')[1]
            return delete_bucket(bucket_to_delete)
        except:
            return 'Syntax Error, unexpected ' + command + ', expecting DELETE_BKT <bucket_name>\n'
    elif 'open_bkt' in command:
        try:
            bucket_to_open = command.split(' ')[1]
            return open_bucket(bucket_to_open)
        except:
            return 'Syntax Error, unexpected ' + command + ', expecting OPEN_BKT <bucket_name>\n'
    elif 'upload' in command:
        return 'File is being Uploaded \n'
    elif 'download' in command:
        return 'File is being Downloaded \n'
    else:
        return 'Bad Command!\n'
