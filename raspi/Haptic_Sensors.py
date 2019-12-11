import time
import RPi.GPIO as io
import socket
from multiprocessing import Process, Value, Array

def LED_Off(angle):
    print("resetting angle: ", angle)
    for p in range(4):
        io.output(4*angle+p,0)

def LED_On(angle):
    print("setting angle: ", angle)
    for p in range(4):
        io.output(4*angle+p,1)

def LED_Duty():
    has_read = False
    while True:
        print("LED_Duty time")
        if stren.value is -1 or angle.value is -1:
            time.sleep(0)
            continue

        ang = angle.value
        stg = stren.value

        print(ang)
        print(stg)

        print("LED_Duty begun")
        on_time = 0.1
        off_time = 1 - (0.1*stg)
        print(on_time)
        print(off_time)
        print("Enter loop")

        has_changed.value = False

        #while has_changed.value is False:# and has_read is False:
        #    LED_On(ang)
        #    time.sleep(on_time)
        #    LED_Off(ang)
        #    time.sleep(off_time)
        LED_On(ang)
        time.sleep(on_time)
        LED_Off(ang)
        time.sleep(off_time)
        print("Leave loop")

def Read_MSG(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'Meenakshis-MacBook-Pro.local'
    
    print("Connecting")
    while True:
        try:
            s.connect((host, port))
            print("Connected to ", host)
            break
        except KeyboardInterrupt:
            quit()
        except:
            print("Not Connected")
    
    while True:
        print("new while loop")
        r_msg = s.recv(15).decode()
        msg = r_msg.split()
        
        print(msg)
    
    
        if len(msg) is 4: 
            if msg[0] == 'START' and msg[3] == 'EOM':
                #print(msg[0])
                #print("Angle: ", msg[1])
                #print("Strength: ", msg[2])
                #print(msg[3])
    
                #s_msg = "RECEIVED"
                #s.send(s_msg.encode())
                
                if angle is not int(msg[1]) or stren is not int(msg[2]):
                    angle.value = int(msg[1])
                    stren.value = int(msg[2])
                    
                    has_changed.value = True
                    
                    time.sleep(0.1)


def init_port(port):
    io.setmode(io.BCM)
    io.setup(port,io.OUT)
    io.output(port,0)

if __name__ == "__main__":

    n_ports = 20
    
    print('Haptic Sensors Initialization')
    
    for p in range(n_ports):
        print("init port: ", p)
        init_port(p)
    
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #host = 'Meenakshis-MacBook-Pro.local'
    #port = int(input("Enter Port Number")) 
    #
    #print("Connecting")
    #while True:
    #    try:
    #        s.connect((host, port))
    #        print("Connected to ", host)
    #        break
    #    except KeyboardInterrupt:
    #        quit()
    #    except:
    #        print("Not Connected")
    #print("Past while loop")
    
    port = int(input("Enter Port Number: "))

    angle = Value('i', -1)
    stren = Value('i', -1)
    has_changed = Value('b', False)
    
    Process(target=Read_MSG, args=(port,)).start()
    Process(target=LED_Duty).start()

#while True:
#    r_msg = s.recv(15).decode()
#    msg = r_msg.split()
#    
#    print(msg)
#
#    #t0 = time.time()
#    #while (time.time() - t0 < 1):
#    #   a = 5 
#    #msg = msg_cycle()
#
#    if len(msg) is 4: 
#        if msg[0] == 'START' and msg[3] == 'EOM':
#            print(count,"\n")
#            print(msg[0])
#            print("Angle: ", msg[1])
#            print("Strength: ", msg[2])
#            print(msg[3])
#
#            #s_msg = "RECEIVED"
#            #s.send(s_msg.encode())
#            
#            if angle is not int(msg[1]) or stren is not int(msg[2]):
#                angle = int(msg[1])
#                stren = int(msg[2])
#                
#                has_changed = True
#                
#                time.sleep(0.1)
#
#    LED_Duty(angle,stren)

