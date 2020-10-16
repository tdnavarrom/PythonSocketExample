import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server = socket.gethostname()
port = 12345

# connect to host
s.connect((server, port))

# recv message and decode here 1024 is buffer size.
print("Connected to: ", server, "!!!")

connected = True

while connected:
    rule = input("SEND RULE: ")
    s.send(rule.encode())

    response = s.recv(1024).decode()
    if rule == 'QUIT':
        print(response)
        connected = False
    elif rule == 'DATA_SEND':
        data = input("INPUT DATA TO SEND: ")
        s.send(data.encode())
        new_response = s.recv(1024).decode()
        print(new_response)
    elif rule == 'DELETE_BUCKET':
        data = input("INPUT ID OF BUCKET: ")
        s.send(data.encode())
        new_response = s.recv(1024).decode()
        print(new_response)
    else:
        print(response)


print("Exiting Connection to server: ", server)
