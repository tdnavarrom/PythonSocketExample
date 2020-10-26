import os
import uuid
import time
from threading import Thread
import Server as s
import Lexer as lx

root_directory = "buckets"
parent_dir = os.getcwd()
full_path = os.path.join(parent_dir, root_directory)

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

def delete_file(rule, client_socket):
    try:
        parameters = rule.split(' ')
        file_path = os.path.join(full_path,parameters[1],parameters[2])
        os.remove(file_path)
        client_socket.send('File deleted Succesfully.\n'.encode())
    except:
        client_socket.send("File doesn\'t exists.")

def delete_bucket(bucket):
    try:
        path = os.path.join(parent_dir, root_directory, bucket)
        os.rmdir(path)
    except:
        return 'Error, the folder doesn`t exists or may contains files.\n'

def do_operation(client, rule):
    if rule == 'ls_bkt':
        return list_buckets()
    elif rule == 'create_bkt':
        create_bucket()
        return 'Bucket Created Successfully!\n'
    elif 'rm_bkt' in rule:
        try:
            bucket_to_delete = rule.split(' ')[1]
            delete_bucket(bucket_to_delete)
            return 0
        except:
            return 'Syntax Error, unexpected ' + rule + ', expecting DELETE_BKT <bucket_name>\n'
    elif 'rm_file' in rule:
        delete_file(rule, client)
        return 0
    elif 'open_bkt' in rule:
        try:
            bucket_to_open = rule.split(' ')[1]
            return open_bucket(bucket_to_open)
        except:
            return 'Syntax Error, unexpected ' + rule + ', expecting OPEN_BKT <bucket_name>\n'
    elif 'upload' in rule:
        return 0
    elif 'download' in rule:
        return 0
    else:
        return 'Bad rule!\n'
