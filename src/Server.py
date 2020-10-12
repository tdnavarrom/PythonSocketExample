# imporing required modules
import socket
import datetime
import Lexer as lx

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

        else:
            c.send(rule.encode())

if __name__ == '__main__':

    # initializing socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname()
    port = 12345

    # binding port and host
    s.bind(('', port))

    # waiting for a client to connect
    s.listen(5)

    while True:
       # accept connection
       c, addr = s.accept()
       print('Connected to :', addr[0], ':', addr[1])
       new_thread = Thread(target=threaded, args=(c,addr, ))
       new_thread.start()

    s.close()
