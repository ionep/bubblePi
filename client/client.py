import socket
import time
from ultraSonic import *

host='192.168.1.102'; #put ip of server here
port=12345;

sensor=ultraSound();

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
    
    while True:
        try:
            s.connect((host,port));
            time.sleep(1);
            break;
        except:
            continue;
    s.send(str.encode("DATA start"));
    print("connected");
    #start connection
    while True:
        reply= s.recv(1024);
        reply= reply.decode('utf-8');
        data=sensor.readData();
        if(reply == 'DATA'):
            s.send(str.encode("DATA "+str(data)));
        else:
            break;

