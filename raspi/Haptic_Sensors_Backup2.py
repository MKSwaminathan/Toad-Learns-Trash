import time
import RPi.GPIO as io
import socket
import asyncio
import sys

def LED_Off(angle):
    print("resetting angle: ", angle)
    for p in range(4):
        io.output(4*angle+p,0)

def LED_On(angle):
    print("setting angle: ", angle)
    for p in range(4):
        io.output(4*angle+p,1)

def LED_Duty(angle, stren):
    if(stren is -1 or angle is -1):
        return

    print("LED_Duty begun")
    on_time = 0.2
    off_time = 2 - (0.2*stren)
    print(on_time)
    print(off_time)
    LED_On(angle)
    time.sleep(on_time)
    LED_Off(angle)
    time.sleep(off_time)

def init_port(port):
    io.setmode(io.BCM)
    io.setup(port,io.OUT)
    io.output(port,0)

msg_r =  [
    ["START","0","0","EOM"],
    ["START","0","1","EOM"], 
    ["START","0","2","EOM"],
    ["START","0","3","EOM"],
    ["START","0","4","EOM"],
    ["START","0","5","EOM"],
    ["START","0","6","EOM"], 
    ["START","0","7","EOM"], 
    ["START","0","8","EOM"], 
    ["START","0","9","EOM"]
]

def msg_cycle():
    print("cycling message")
    print("index = %d" % msg_cycle.index)
    s_msg = msg_r[msg_cycle.index]
    msg_cycle.index = (msg_cycle.index + 1) % len(msg_r)
    return s_msg
msg_cycle.index = 0

#async def test():
#    print("Testing")
#    while True:
#        msg = await msg_cycle()
#        if len(msg) is not 0:
#            if angle is not int(msg[1]) or stren is not int(msg[2]):
#                angle = int(msg[1])
#                stren = int(msg[2])
#                
#                has_changed = True
#                
#                await asyncio.sleep(0.1)
#                
#        await LED_Duty(angle,stren)

#async def Haptic():
#    print("Haptic On")
#    my_duty = None
#    while True:
#        r_msg = s.recv(13).decode()
#        msg = r_msg.split()
#        await asyncio.sleep(0)
#        if len(msg) is 4:
#            if msg[0] == 'START' and msg[3] == 'EOM':
#                if angle is not int(msg[1]) or stren is not int(msg[2]):
#                    angle = int(msg[1])
#                    stren = int(msg[2])
#
#                    has_changed = True
#
#                    await asyncio.sleep(0.1)
#        if not my_duty and (angle is not -1 or stren is not -1):
#            my_duty = asyncio.ensure_future(LED_Duty(angle,stren))
#        elif has_changed and my_duty:
#            has_changed = False
#            if not my_duty.cancelled():
#                my_duty.cancel()
#            else: 
#                my_duty = None
            

# MAIN FUNCTION
n_ports = 20

print('Haptic Sensors Initialization')

for p in range(n_ports):
    print("init port: ", p)
    init_port(p)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'Meenakshis-MacBook-Pro.local'
port = int(input("Enter Port Number")) 

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
print("Past while loop")
count = 0

#loop = asyncio.get_event_loop()
#try:
#    asyncio.ensure_future(Haptic())
#    loop.run_until_complete(Haptic())
#finally:
#    loop.run_until_complete(loop.shutdown_asyncgens())
#    loop.close()
#
#if(not run_test.cancelled()):
#    print("Test is still running")

angle = -1
stren = -1
print("Entering new while loop")
while True:
    r_msg = s.recv(15).decode()
    msg = r_msg.split()
    
    print(msg)

    #t0 = time.time()
    #while (time.time() - t0 < 1):
    #   a = 5 
    #msg = msg_cycle()

    if len(msg) is 4: 
        if msg[0] == 'START' and msg[3] == 'EOM':
            print(count,"\n")
            print(msg[0])
            print("Angle: ", msg[1])
            print("Strength: ", msg[2])
            print(msg[3])

            #s_msg = "RECEIVED"
            #s.send(s_msg.encode())
            
            if angle is not int(msg[1]) or stren is not int(msg[2]):
                angle = int(msg[1])
                stren = int(msg[2])
                
                has_changed = True
                
                time.sleep(0.1)

    LED_Duty(angle,stren)

