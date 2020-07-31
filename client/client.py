import socket
import time
from ultraSonic import *
import array

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
		darray=0;
		checkArray=array.array('d',[]);
		i=0;
		while i<20:
			checkArray.insert(i,sensor.readData());
			if(i>=2):
				if(abs(checkArray[i-2]-checkArray[i-1])>5 or abs(checkArray[i-1]-checkArray[i])>5 or
				abs(checkArray[i]-checkArray[i-2])>5):
					darray-=checkArray[i-1];
					darray-=checkArray[i-2];
					i=i-2;
					continue;
			darray+=checkArray[i];
			time.sleep(0.1);
			i=i+1;
		data=darray/20;
		print("Upper:"+str(data)+" cm");
		if(reply == 'DATA'):
			s.send(str.encode("DATA "+str(data)));
		else:
			break;
    
