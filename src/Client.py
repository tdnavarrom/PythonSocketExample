import socket
from threading import Thread
import os



def handle_upload(file_path):
    reader = open(file_path, 'rb')
    size = os.path.getsize(file_path)

    loop = str(int(size/1024)+1)

    loop = loop.encode()

    loop += b' ' * (64 - len(loop))
    s.send(loop)

    for i in range(int(loop)):

        data = reader.read(1024)
        s.send(data)

def handle_download(file_name):
    root_directory = "files"
    parent_dir = os.getcwd()
    file_path = os.path.join(parent_dir, root_directory)
    
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    writer = open(file_path+'/'+file_name, 'wb')
    
    loop = s.recv(64)

    for i in range(int(loop.strip().decode())):
        data = s.recv(1024)
        writer.write(data)

    writer.close()


if __name__ == "__main__":

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server = socket.gethostname()
    port = 12345

    # connect to host
    s.connect((server, port))

    # recv message and decode here 1024 is buffer size.
    print("Connected to: ", server, "!!!")

    connected = True

    print('----------------------')
    print('Input commands below!!')

    while connected:

        rule = input("> ").strip()
        s.send(rule.encode())
        response = s.recv(1024).decode('utf-8')

        print(response)
        if rule == 'QUIT':
            connected = False
            s.close()
        elif 'UPLOAD_FL' in rule and response == '200 OK':
            file_path = rule.split(' ')[2]
            print(file_path)
            new_thread = Thread(target=handle_upload, args=(file_path,))
            new_thread.start()
            print(s.recv(1024).decode('utf-8'))
        elif 'DOWNLOAD_FL' in rule and response == '200 OK':
            file_path = rule.split(' ')[2]
            print(file_path)
            new_thread = Thread(target=handle_download, args=(file_path,))
            new_thread.start()
            message = s.recv(1024)
            print(message.decode())
        else:
            response = s.recv(1024).decode('utf-8')
            print(response)


    print("Exiting Connection to server: ", server)
