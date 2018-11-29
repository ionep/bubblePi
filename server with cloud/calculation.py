import RPi.GPIO as GPIO
import datetime
import time
from dbtest import *

class Calculator:
	motor=16;
	area=3.1415*15*15;
	db=Database();
	
	def __init__(self):
		GPIO.setmode(GPIO.BCM);
		GPIO.setwarnings(False);
		GPIO.setup(self.motor,GPIO.OUT);
		GPIO.output(self.motor,True);

	def calculate(self, lower, upper, conn, sensor):
		started=False;
		setflag=False;
		initialValue=0;
		finalValue=0;
		while True:
			time.sleep(1);
			lower=int(lower);
			
			upper.encode('ascii','ignore');
			upper=str(upper);
			#convert to integer
			s=list(upper);
			f=0;
			for i in s:
				if(i!='.'):
					f=f*10+int(i);
				else:
					break;
			upper=f;
						
			if(lower<=25 and not(started)):
				if(upper>22):
					started=True;
					if(not(setflag)):
						initialValue=upper;
						setflag=True;
					print("Motor on");
					GPIO.output(self.motor,False);
					conn.sendall(str.encode("DATA"));
					data=conn.recv(1024); #buffer size 1024
					data=data.decode('utf8');
					#split data into 2 parts, first being command
					dataMessage= data.split(' ',1);
					upper=dataMessage[1];
					print("Upper:"+upper+"cm");
					lower=sensor.readData();
					continue;
				else:
					GPIO.output(self.motor,True);
					break;
			elif(lower<=25 and started):
				if(upper>21):
					print("Motor on");
					GPIO.output(self.motor,False);
					conn.sendall(str.encode("DATA"));
					data=conn.recv(1024); #buffer size 1024
					data=data.decode('utf8');
					#split data into 2 parts, first being command
					dataMessage= data.split(' ',1);
					upper=dataMessage[1];
					print("Upper:"+upper+"cm");
					lower=sensor.readData();
					continue;
				else:
					if(setflag):
						setflag=False;
						finalValue=upper;
						diff=initialValue-finalValue;
						diff=str(diff);
						#convert to integer
						stmp=list(diff);
						ftmp=0;
						for i in stmp:
							if(i!='.'):
								ftmp=ftmp*10+int(i);
							else:
								break;
						diff=ftmp;
						vol=self.area*diff/1000;
						print("Volume:"+str(vol));
						d=datetime.datetime.now();
						if(d.month<10):
							mm='0'+str(d.month);
						else:
							mm=str(d.month);
						if(d.day<10):
							dd='0'+str(d.day);
						else:
							dd=str(d.day);
						cdate=str(d.year)+mm+dd;
						query="""SELECT * FROM consumption WHERE date=%s"""%(cdate);
						num,data=self.db.query(query);
						if(num>0):
							d=data[0];
							newvol=vol+float(d['volume']);
							query="""UPDATE consumption SET volume=%s WHERE date=%s"""%(newvol,cdate);
						else:
							query="""INSERT INTO consumption(date,volume,sent) VALUES(%s,%s,'False')"""%(cdate,vol);
						self.db.insert(query);
						
					GPIO.output(self.motor,True);
					break;
			else:
				if(setflag):
					setflag=False;
					finalValue=upper;
					diff=initialValue-finalValue;
					diff=str(diff);
					#convert to integer
					stmp=list(diff);
					ftmp=0;
					for i in stmp:
						if(i!='.'):
							ftmp=ftmp*10+int(i);
						else:
							break;
					diff=ftmp;
					vol=self.area*diff/1000;
					print("Volume:"+str(vol));
					d=datetime.datetime.now();
					if(d.month<10):
						mm='0'+str(d.month);
					else:
						mm=str(d.month);
					if(d.day<10):
						dd='0'+str(d.day);
					else:
						dd=str(d.day);
					cdate=str(d.year)+mm+dd;
					query="""SELECT * FROM consumption WHERE date=%s"""%(cdate);
					num,data=self.db.query(query);
					if(num>0):
						d=data[0];
						newvol=vol+float(d['volume']);
						query="""UPDATE consumption SET volume=%s WHERE date=%s"""%(newvol,cdate);
					else:
						query="""INSERT INTO consumption(date,volume,sent) VALUES(%s,%s,'False')"""%(cdate,vol);
					self.db.insert(query);
				print("Nothing to do");
				GPIO.output(self.motor,True);
				break;
	
