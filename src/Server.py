# imporing required modules
import crud
import Lexer as lx
import os
import socket

# import thread module
from threading import Thread

def threaded(c, addr):
    connected = True
    while connected:

        data = c.recv(1024).decode()
        print('Addr: ', addr, ' RULE: ', data)
        rule = lx.find_rule(data)

        if data == 'QUIT':
            print("connection closed from addr: ", addr)
            c.send(rule.encode())
            connected = False
            c.close()
        elif data == 'DATA_SEND':
            c.send(rule.encode())
            new_data = c.recv(1024).decode()
            status = lx.find_rule('DATA_RECEIVED')
            print('Addr: ', addr, ' DATA: ', new_data)
            c.send(status.encode())
        elif data == 'LIST_BKTS':
            response = crud.list_buckets()
            c.send(response.encode())
        elif data == 'CREATE_BUCKET':
            status = crud.create_bucket()
            if status:
                response = rule
            c.send(response.encode())
        elif data == 'DELETE_BUCKET':
            c.send(rule.encode())
            id_bucket = c.recv(1024).decode()
            status = crud.delete_bucket(id_bucket)
            if status:
                response = rule
                print('Addr: ', addr, ' DATA: ', status)
            else:
                response = 'Error, the folder doesn`t exists or may contains files.'
                print('Addr: ', addr, ' DATA: Error couldn`t delete bucket ', id_bucket)

            c.send(response.encode())
        else:
            c.send(rule.encode())

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
