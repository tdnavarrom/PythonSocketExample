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

    def connect_to_server(self):
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
        print('buenas')
    
        with open(file_path, 'rb') as reader:
            print('buenas2')
            while True:
                send_bytes = reader.read(1024)
                if not send_bytes: 
                    print('hola_buenas')
                    break
                self.data_socket.send(send_bytes)
            reader.close()
        self.data_socket.close()
        print('chao')

    def download_from_server(self, rule, server_socket):
        self.data_socket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:
            arguments = rule.split(' ',2)
            file_name = arguments[2]
            file_path = os.path.join(self.download_path, file_name)
            self.data_socket2.connect((self.host, self.data_port2))
            start_new_thread(self.handle_download, (file_path,))
        except :
            print(server_socket.rcv(1024).decode('utf-8'))
            self.data_socket2.close()
    
    def handle_download(self, file_path):
        f = open(file_path, 'wb')
        while True:
            bytes_file = self.data_socket2.recv(1024)
            if not bytes_file : break
            f.write(bytes_file)
        f.close()
        self.data_socket2.close()


if __name__ == '__main__':
    try:
        download_path = sys.argv[1]
        Client(download_path).connect_to_server()
    except:
        print('The path where files will be downloaded to, was not suplied. Please try again')