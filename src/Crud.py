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
    if command == 'LIST_BKT':
        return list_buckets()
    elif command == 'CREATE_BKT':
        create_bucket()
        return 'Bucket Created Successfully!\n'
    elif 'DELETE_BKT' in command:
        try:
            bucket_to_delete = command.split(' ')[1]
            return delete_bucket(bucket_to_delete)
        except:
            return 'Syntax Error, unexpected ' + command + ', expecting DELETE_BKT <bucket_name>\n'
    elif 'OPEN_BKT' in command:
        try:
            bucket_to_open = command.split(' ')[1]
            return open_bucket(bucket_to_open)
        except:
            return 'Syntax Error, unexpected ' + command + ', expecting OPEN_BKT <bucket_name>\n'
    elif 'UPLOAD_FL' in command:
        try:
            arguments = command.split(' ', 2)
            upload_to = arguments[1]
            file_name = arguments[2].split('/')[-1]
            new_thread = Thread(target=s.handle_upload, args=(client, file_name, upload_to, ))
            new_thread.start()

            return 'The file ' + file_name + ' has been uploaded to the bucket: ' + upload_to + '\n' 
        except:
            return 'Syntax Error, unexpected ' + command + ', expecting UPLOAD_FL <bucket_name>  <file_path>\n'
    elif 'DOWNLOAD_FL' in command:
        try:
            arguments = command.split(' ')
            bucket_name = arguments[1]
            file_name = arguments[2]
            new_thread = Thread(target=s.handle_upload_to_client, args=(client, bucket_name, file_name, ))
            new_thread.start()
            
            return 'The file ' + file_name + ' is being downloaded from the bucket: ' + bucket_name + '\n'
        except:
            return 'Syntax Error, unexpected ' + command + ', expecting DOWNLOAD_FL <bucket_name> <file_name>\n'
    else:
        return 'Bad Command!\n'
