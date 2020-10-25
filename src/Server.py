# imporing required modules
import Crud
import Lexer as lx
import os
import socket
import time

# import thread module
from threading import Thread

def threaded(c, addr):
    connected = True
    while connected:

        rule = c.recv(1024).decode()
        print('Addr: ', addr, ' RULE: ', rule)

        status = lx.check_sintaxis(rule)

        c.send(status.encode())

        if status != '200 OK':
            pass

        if rule == 'QUIT':
            print("connection closed from addr: ", addr)
            c.send(rule.encode())
            connected = False
            c.close()
        else:
            new_response = Crud.do_operation(c, rule)
            c.send(new_response.encode())
        
        time.sleep(2)

def handle_upload(c, file_name, upload_to):
    root_directory = "buckets"
    parent_dir = os.getcwd()
    file_path = os.path.join(parent_dir, root_directory, upload_to, file_name)
    writer = open(file_path, 'wb')

    loop = c.recv(64)

    for i in range(int(loop.strip().decode())):
        data = c.recv(1024)
        writer.write(data)

    writer.close()

def handle_upload_to_client(c, bucket, file_name):
    root_directory = "buckets"
    parent_dir = os.getcwd()
    file_path = os.path.join(parent_dir, root_directory, bucket, file_name)


    reader = open(file_path, 'rb')
    size = os.path.getsize(file_path)

    loop = str(int(size/1024)+1)

    loop = loop.encode()

    loop += b' ' * (64 - len(loop))
    c.send(loop)

    for i in range(int(loop)):

        data = reader.read(1024)
        c.send(data)

if __name__ == '__main__':

    # initializing socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 12345

    # binding port and host
    s.bind(('', port))

    directory = "buckets"
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, directory)
    
    if not os.path.exists(path):
        os.mkdir(path)

    # waiting for a client to connect
    s.listen(5)
    
    while True:
       # accept connection
       c, addr = s.accept()
       print('Connected to :', addr[0], ':', addr[1])
       new_thread = Thread(target=threaded, args=(c,addr, ))
       new_thread.start()

    s.close()
