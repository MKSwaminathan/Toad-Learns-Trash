import socket
import time

s = socket.socket()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
print (host)
port = 1111
s.bind((host, port))

s.listen(5)

while True:
    try:
        client, addr = s.accept()
        print ('Got connection from', addr)
        connection_verification = 'Connected to Realsense'
        client.send(connection_verification.encode())
        msgs = ['START 0 9 EOM', 'START 4 1000 EOM']

        toggle = True
        while True:
            msg = msgs[0] if toggle else msgs[1]
            client.send(msg.encode())
            toggle = not toggle
            #verif = client.recv(1024).decode()
            #if (verif == 'RECEIVED'): break
            time.sleep(0.5)
    except:
        next
