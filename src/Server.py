# imporing required modules
import Crud
import Lexer as lx
import os
import socket
import sys
import time

# import thread module
from _thread import start_new_thread

class Server:

    def __init__(self, directory):
        self.host = '127.0.0.1'

        #Control Socket
        self.control_port = 12345
        self.control_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.control_socket.bind((self.host, self.control_port))
        self.client = None
        self.address = None

        #Data Socket
        self.data_port = 55555
        self.data_port2 = 55556

        self.data_addr = None
        self.data_addr2 = None

        #bucket directory
        self.directory_path = directory
        self.directory_name = 'buckets'
        self.full_path = os.path.join(self.directory_path, self.directory_name)


    def start_server(self):
        self.create_directory()
        print('------------------------------')
        print('Server is running...')
        print('IP addr: ' + self.host)
        print('Port: ' + str(self.control_port))
        print('Socket is listening... ' + '(' + self.host + ',' + str(self.control_port) + ')')
        print('-----------------------------')
        self.control_socket.listen(10)
        while True:
            self.client, self.address = self.control_socket.accept()
            print('New Connection accepted. Remote IP addr: ' + self.address[0] + ' Port: ' + str(self.address[1]))
            start_new_thread(self.connection,(self.client, self.address[0]))
        self.control_socket.close()


    def create_directory(self):

        if not os.path.exists(self.full_path):
            os.mkdir(self.full_path)
            print('buckets folder created succesfully at: ' + self.full_path)


    def connection(self, client, addr):
        connected = True
        while connected:

            rule = client.recv(1024).decode()
            print('Addr: ',  addr, ' RULE: ', rule)

            status = lx.check_sintaxis(rule)

            client.send(status.encode())

            if status == '200 OK':

                if rule == 'quit':
                    print("connection closed from addr: ", addr)
                    client.send(rule.encode())
                    connected = False
                elif 'upload' in rule:
                    self.upload_from_client(rule, client)
                elif 'download' in rule:
                    self.download_to_client(rule, client)
                else:
                    new_response = Crud.do_operation(client, rule)
                    if new_response != 0: client.send(new_response.encode())
            else:
                client.send('Bad rule: Please Check the available instructions \n'.encode())
        
        client.close()

    def upload_from_client(self, rule, client):
        self.data_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:
            parameters = rule.split(' ', 2)
            bucket = parameters[1]
            file_name = parameters[2].split('/')[-1]
            
            self.data_socket.bind((self.host, self.data_port))
            self.data_socket.listen(5)
            self.data_socket.settimeout(2)
            data_client, self.data_addr = self.data_socket.accept()
            start_new_thread(self.handle_upload_from_client, (data_client, bucket, file_name,))
        except:
            client.send('Error uploading file.\n'.encode())
            self.data_socket.close()

            

    def handle_upload_from_client(self, data_client, bucket, file_name):

        path = os.path.join(self.full_path, bucket, file_name)
        with open(path, 'wb') as writer:
            while True:
                bytes_file = data_client.recv(1024)
                if not bytes_file: 
                    break
                writer.write(bytes_file)
                

            writer.close()
        data_client.close()
        self.data_socket.close()


    def download_to_client(self, rule, client):

        self.data_socket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:
            parameters = rule.split(' ', 2)
            download_from = parameters[1]
            file_name = parameters[2]
            path = os.path.join(self.full_path, download_from, file_name)
            self.data_socket2.connect((self.host, self.data_port2))
            print('Connection stablished.')
            
            start_new_thread(self.handle_download_to_client,(file_name, download_from,))
        except:
            client.send('Error, file not found or bucket doesn\'t exists.\n'.encode())
            self.data_socket2.close()
    
    def handle_download_to_client(self, file_name, download_from):
        path = os.path.join(self.full_path, download_from, file_name)
        with open(path, 'rb') as reader:
            while True:
                send_bytes = reader.read(1024)
                if not send_bytes: break
                self.data_socket2.send(send_bytes)
            reader.close()
        self.data_socket2.close()

if __name__ == '__main__':
    try:
        directory = sys.argv[1]
        Server(directory).start_server()
    except:
        print('The path where the buckets will be stored was not suplied.')
