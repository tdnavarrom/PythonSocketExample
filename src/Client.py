import socket
from threading import Thread

class Client:

    def __init__(self):
        self.host = socket.gethostname()

        #server Socket
        self.port = 12345
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        #Data Socket
        self.data_port = 12346
        self.data_socket = None

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

            print(response)
            if rule == 'quit':
                connected = False
                self.server_socket.close()
            elif 'upload' in rule and response == '200 OK':
                self.upload_to_server(rule, self.server_socket)
            elif 'download' in rule and response == '200 OK':
                pass      
            else:
                response = self.server_socket.recv(1024).decode('utf-8')
                print(response)        


    def upload_to_server(self, rule, server_socket):
        try:
            arguments = rule.split(' ', 2)
            file_path = arguments[2]
            self.data_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.data_socket.connect((self.host, self.data_port))
            print('Connection stablished.')
            new_thread = Thread(target=self.handle_upload, args=(file_path, server_socket, self.data_socket,))
            new_thread.start()
        except:
            print('Error.\n')

    def handle_upload(self, file_path, server_socket, data_socket):
        try:
            with open(file_path, 'rb') as reader:
                while True:
                    send_bytes = reader.read(1024)
                    if not send_bytes: break
                    data_socket.send(send_bytes)
            server_socket.recv(1024).decode()
        except:
            server_socket.recv(1024).decode()
        data_socket.close()

if __name__ == '__main__':
    Client().connect_to_server()
