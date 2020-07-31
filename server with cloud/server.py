import socket
from ultraSonic import *
from calculation import *
import array
import RPi.GPIO as GPIO

class Receiver:
	
	host='';
	#any port that is unused
	#1-1024 are reserved
	port=12345;
	
	sensor=ultraSound();
	
	calculator=Calculator();
	
	dataNo=10;
	
	s='';
	
	warningLed=19;
	
	
	def __init__(self):
		self.s=self.setupServer();
		GPIO.setmode(GPIO.BCM);
		GPIO.setwarnings(False);
		GPIO.setup(self.warningLed,GPIO.OUT);
		
	def setupServer(self):
	    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
	    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
	    print("Socket Created");
	    try:
	        s.bind((self.host,self.port))
	        print("Socket bind complete");
	    except socket.error as msg:
	        print(msg);
	    return s;
	
	def setupConnection(self):
		#number of allowed connection
	    s=self.s;
	    s.listen(1);
	    conn, address= s.accept();
	    print("Connected to: "+address[0]+":"+str(address[1]));
	    return conn;
	    
	def processData(self,data,conn):
	     #lower=self.sensor.readData();
	     larray=0;
	     checkArray=array.array('d',[]);
	     i=0;
	     #print("s1");
	     while i<self.dataNo:
			 sData=self.sensor.readData();
			 #print("s2");
			 checkArray.insert(i,sData);
			 if(i>=2):
				 if(abs(checkArray[i-2]-checkArray[i-1])>1.5 or abs(checkArray[i-1]-checkArray[i])>1.5 or
				 abs(checkArray[i]-checkArray[i-2])>1.5):
					 larray-=checkArray[i-1];
					 larray-=checkArray[i-2];
					 i=i-2;
					 #print("s3");
					 time.sleep(0.1);
					 continue;
			 larray+=checkArray[i];
			 #print("s4");
			 time.sleep(0.3);
			 i=i+1;
	     lower=larray/self.dataNo;
	     print("Upper:"+data+"cm");
	     print("Lower:"+str(lower)+"cm");
	     upper=data;
	     if(lower>70 or lower<=19):
			 GPIO.output(self.warningLed,True);
	     else:
			 GPIO.output(self.warningLed,False);
	     self.calculator.calculate(lower,upper,conn,self.sensor);
	
	def dataTransfer(self,conn):
	    #data transmission to a particular connected client
	    while True:
	        data=conn.recv(1024); #buffer size 1024
	        data=data.decode('utf8');
	        #split data into 2 parts, first being command
	        dataMessage= data.split(' ',1);
	        command=dataMessage[0];
	        if(command == "DATA"):
	            if(dataMessage[1]!='start'):
					self.processData(dataMessage[1],conn);
	            reply="DATA";
	        else:
	            reply="ERROR";
	            print("Invalid Command");
	
	        #send command to client
	        conn.sendall(str(reply).encode("utf8"));
	        #print("Request has been made: "+reply);
	    conn.close();
	    
	def startCommunication(self):
		while True:
		    try:
		        conn=self.setupConnection();
		        self.dataTransfer(conn);
		    except:
		        self.s.close();
		        break;
	

	
