import time
import RPi.GPIO as io


def init_port(port):
    io.setmode(io.BCM)
    io.setup(port,io.OUT)
    io.output(port,0)

n_ports = 20
for p in range(n_ports):
    print('init port: ',p)
    init_port(p)

# while True:
#     #io.output(1,1)
#     for p in range(n_ports):
#         print('running port: ',p)
#         io.output(p,1)
#         time.sleep(0.5)
#         io.output(p,0)
#         time.sleep(0.5) 
#         #io.output(p,1)
#         #time.sleep(0.5)
#         #io.output(p,0)
#         #time.sleep(0.5) 
