import socket
import time
import RPi.GPIO as io


def init_port():
    io.setmode(io.BCM)
    io.setup(4,io.OUT)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'Meenakshis-MacBook-Pro.local'
port = 12345

s.connect((host, port))

init_port()

while True:

    s_msg = s.recv(1024).decode()
    print(s_msg)
    if s_msg == 'blink':
        for i in range (0,5):
            io.output(4,0)
            time.sleep(0.30)
            io.output(4,1)
            time.sleep(0.30)
    
    msg = 'Tell me to blink'
    s.send(msg.encode())
    #s.close()
    
    
