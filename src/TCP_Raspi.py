import socket
import time

s = socket.socket()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
print (host)
port = 12345
s.bind((host, port))

s.listen(5)
while True:
    client, addr = s.accept()
    print ('Got connection from', addr)
    msg = 'Thank you for connecting'
    client.send(msg.encode())
    while True: 
        client.send('blink'.encode())
        time.sleep(5)


