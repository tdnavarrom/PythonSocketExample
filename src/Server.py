# imporing required modules
import Crud
import Lexer as lx
import os
import socket
import sys

# import thread module
from threading import Thread

class Server:

    def __init__(self, directory):
        self.host = socket.gethostname()

        #Control Socket
        self.control_port = 12345
        self.control_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.control_socket.bind((self.host, self.control_port))
        self.client = None
        self.address = None

        #Data Socket
        self.data_port = 12346
        self.data_socket = None
        self.conn = None
        self.addr = None

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
        self.control_socket.listen(5)
        while True:
            self.client, self.address = self.control_socket.accept()
            print('New Connection accepted. Remote IP addr: ' + self.address[0] + ' Port: ' + str(self.address[1]))
            new_thread = Thread(target=self.connection, args=(self.client, self.address[0], ))
            new_thread.start()
        self.control_socket.close()


    def create_directory(self):

        if not os.path.exists(self.full_path):
            os.mkdir(self.full_path)
            print('buckets folder created succesfully at: ' + self.full_path)


    def connection(self, client, addr):
        connected = True
        while connected:

            rule = client.recv(1024).decode()
            print('Addr: ', addr, ' RULE: ', rule)

            status = lx.check_sintaxis(rule)

            client.send(status.encode())

            if status == '200 OK':

                if rule == 'quit':
                    print("connection closed from addr: ", addr)
                    client.send(rule.encode())
                    connected = False
                    client.close()
                elif 'upload' in rule:
                    self.upload_from_client(rule, client)
                elif 'download' in rule:
                    pass
                else:
                    new_response = Crud.do_operation(client, rule)
                    client.send(new_response.encode())
            
            else:
                client.send('Bad rule: Please Check the available instructions \n'.encode())

    def upload_from_client(self, rule, client):
        try:
            arguments = rule.split(' ', 2)
            bucket = arguments[1]
            file_name = arguments[2].split('/')[-1]
            self.data_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.data_socket.bind((self.host, self.data_port))
            self.data_socket.listen(5)
            self.conn, self.addr = self.data_socket.accept()
            new_thread = Thread(target=self.handle_upload_from_client, args=(client, self.conn, bucket, file_name))
            new_thread.start()
        except:
            client.send('Error uploading file.\n'.encode())

            

    def handle_upload_from_client(self, client, conn, bucket, file_name):
        try:
            path = os.path.join(self.full_path, bucket, file_name)
            with open(path, 'wb') as writer:
                while True:
                    bytes_file = conn.recv(1024)
                    if not bytes_file: break
                    writer.write(bytes_file)
            client.send('Upload complete.\n'.encode())
        except:
            client.send('Cant access file.\n'.encode())
        self.data_socket.close()


    def handle_upload_to_client(self, client, conn, bucket, file_name):

        path = os.path.join(self.full_path, bucket, file_name)
        with open(path, 'wb') as writer:
            while True:
                bytes_file = conn.recv(1024)
                if not bytes_file: break
                writer.write(bytes_file)
        
        client.send('Upload complete.\n'.encode())

if __name__ == '__main__':
    try:
        directory = sys.argv[1]
        Server(directory).start_server()
    except:
        print('The path where the buckets will be stored was not suplied.')
