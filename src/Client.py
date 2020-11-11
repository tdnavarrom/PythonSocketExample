import socket
import os
import sys
from _thread import start_new_thread
import time


class Client:

    def __init__(self, dwnload_path):
        self.host = '127.0.0.1'

        #server Socket
        self.port = 12345
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   
        #Data Socket
        self.data_port = 55555
        self.data_port2 = 55556

        self.download_path = dwnload_path
        self.dir_name = 'files'
        self.full_path = os.path.join(self.download_path, self.dir_name)

    def connect_to_server(self):
        self.create_directory()
        try:
            self.server_socket.connect((self.host, self.port))
            addr = self.server_socket.getsockname()
            print('---------------------------------')
            print('Client is running!')
            print('Connected to the server from: ' + '(' + addr[0] + ':' + str(addr[1]) + ')')
            print('---------------------------------')
            self.handle_connection_server()
        except socket.error as e:
            print(str(e))

    def create_directory(self):

        if not os.path.exists(self.full_path):
            os.mkdir(self.full_path)
            print('files folder created succesfully at: ' + self.full_path)

    def handle_connection_server(self):

        connected = True

        print('----------------------')
        print('Input rules below!!')

        while connected:

            rule = input("> ").strip()
            self.server_socket.send(rule.encode())
            response = self.server_socket.recv(1024).decode('utf-8')

            if rule == 'quit':
                connected = False
            elif 'upload' in rule and response == '200 OK':
                self.upload_to_server(rule, self.server_socket)
            elif 'download' in rule and response == '200 OK':
                self.download_from_server(rule, self.server_socket)      
            else:
                response = self.server_socket.recv(1024).decode('utf-8')
                print(response)
            
        self.server_socket.close()       


    def upload_to_server(self, rule, server_socket):
        self.data_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        try:
            parameters = rule.split(' ', 2)
            file_path = os.path.join(parameters[1],parameters[2])
            self.data_socket.connect((self.host, self.data_port))
            print('Connection stablished.')
            start_new_thread(self.handle_upload, (file_path,))
        except:
            print(server_socket.recv(1024).decode('utf-8'))
            self.data_socket.close()


    def handle_upload(self, file_path):
        with open(file_path, 'rb') as reader:
            while True:
                send_bytes = reader.read(1024)
                if not send_bytes: 
                    break
                self.data_socket.send(send_bytes)
            reader.close()
        self.data_socket.close()


    def download_from_server(self, rule, server_socket):
        self.data_socket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:
            parameters = rule.split(' ', 2)
            file_name = parameters[2].split('/')[-1]
            
            self.data_socket2.bind((self.host, self.data_port2))
            self.data_socket2.listen(5)
            self.data_socket2.settimeout(2)
            data_client, self.data_addr2 = self.data_socket2.accept()

            start_new_thread(self.handle_download, (data_client, file_name,))
        except :
            print(server_socket.rcv(1024).decode('utf-8'))
            self.data_socket2.close()
    
    def handle_download(self, data_client, file_name):

        path = os.path.join(self.full_path, file_name)
        with open(path, 'wb') as writer:
            while True:
                bytes_file = data_client.recv(1024)
                if not bytes_file: 
                    break
                writer.write(bytes_file)
            writer.close()
        data_client.close()
        self.data_socket2.close()


if __name__ == '__main__':
    try:
        download_path = sys.argv[1]
        Client(download_path).connect_to_server()
    except:
        print('The path where files will be downloaded to, was not suplied. Please try again')