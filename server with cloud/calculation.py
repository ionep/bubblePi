import RPi.GPIO as GPIO
import datetime
import time
from dbtest import *
import array
from sound import *

class Calculator:
	motor=16;
	buzzer=26;
	#area=3.1415*15*15;
	area=34.0*30;
	dataNo=10;
	lowerMaxDistance=45;
	upperMaxDistance=40;
	upperMotorStop=38;
	db=Database();
	
	def __init__(self):
		GPIO.setmode(GPIO.BCM);
		GPIO.setwarnings(False);
		GPIO.setup(self.motor,GPIO.OUT);
		GPIO.setup(self.buzzer,GPIO.OUT);
		GPIO.output(self.motor,True);

	def calculate(self, lower, upper, conn, sensor):
		started=False;
		setflag=False;
		initialValue=0.0;
		finalValue=0.0;
		vol=0;
		while True:
			time.sleep(1);
			calcLower=lower;
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
						
			if(lower<=44 and not(started)):
				if(upper>=40):
					started=True;
					if(not(setflag)):
						#initialValue=upper;
						initialValue=calcLower;
						setflag=True;
					print("Motor on");
					GPIO.output(self.buzzer,True);
					time.sleep(5);
					GPIO.output(self.buzzer,False);
					GPIO.output(self.motor,False);
					conn.sendall(str.encode("DATA"));
					data=conn.recv(1024); #buffer size 1024
					data=data.decode('utf8');
					#split data into 2 parts, first being command
					dataMessage= data.split(' ',1);
					upper=dataMessage[1];
					print("Upper:"+upper+"cm");
					larray=0;
					checkArray=array.array('d',[]);
					#print("c1");
					i=0;
					while i<self.dataNo:
						checkArray.insert(i,sensor.readData());
						#print("c2");
						if(i>=2):
							if(abs(checkArray[i-2]-checkArray[i-1])>1.5 or abs(checkArray[i-1]-checkArray[i])>1.5 or
							abs(checkArray[i]-checkArray[i-2])>1.5):
								larray-=checkArray[i-1];
								larray-=checkArray[i-2];
								i=i-2;
								#print("c3");
								time.sleep(0.1);
								continue;
						larray+=checkArray[i];
						#print("c4");
						time.sleep(0.3);
						i=i+1;
					lower=larray/self.dataNo;
					print("Lower:"+str(lower)+"cm");
					continue;
				else:
					GPIO.output(self.motor,True);
					break;
			elif(lower<=44 and started):
				if(upper>=39):
					print("Motor on");
					GPIO.output(self.motor,False);
					conn.sendall(str.encode("DATA"));
					data=conn.recv(1024); #buffer size 1024
					data=data.decode('utf8');
					#split data into 2 parts, first being command
					dataMessage= data.split(' ',1);
					upper=dataMessage[1];
					print("Upper:"+upper+"cm");
					larray=0;
					checkArray=array.array('d',[]);
					i=0;
					while i<self.dataNo:
						checkArray.insert(i,sensor.readData());
						if(i>=2):
							if(abs(checkArray[i-2]-checkArray[i-1])>1.5 or abs(checkArray[i-1]-checkArray[i])>1.5 or
							abs(checkArray[i]-checkArray[i-2])>1.5):
								larray-=checkArray[i-1];
								larray-=checkArray[i-2];
								time.sleep(0.1);
								i=i-2;
								continue;
						larray+=checkArray[i];
						#print(str(larray));
						time.sleep(0.3);
						i=i+1;
					lower=larray/self.dataNo;
					print("Lower:"+str(lower)+"cm");
					continue;
				else:
					if(setflag):
						setflag=False;
						#finalValue=upper;
						finalValue=calcLower;
						diff=abs(finalValue-initialValue); #in real time no error but while adding water when motor on into lower
						diff=str(diff);
						#convert to float
						stmp=list(diff);
						ftmp=0;
						decimal=False;
						j=10.0;
						for i in stmp:
							if(not(decimal)):
								if(i!='.'):
									ftmp=ftmp*10+int(i);
								else:
									decimal=True;
							else:
								ftmp=ftmp+(int(i))/j;
								j=j*10;
						diff=ftmp;
						vol=self.area*diff/1000;
						print("Volume:"+str(vol));
						d=datetime.datetime.now();
						if(d.month<10):
							mm='0'+str(d.month);
						else:
							mm=str(d.month);
						#if(d.day<10):
							#dd='0'+str(d.day);
						#else:
							#dd=str(d.day);
						if(d.minute<10):
							dd='0'+str(d.minute);
						else:
							dd=str(d.minute);
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
					print("added");
					break;
			else:
				if(setflag):
					setflag=False;
					#finalValue=upper;
					finalValue=calcLower;
					diff=abs(finalValue-initialValue); #error maybe occur here due to reason above
					diff=str(diff);
					#convert to float
					stmp=list(diff);
					ftmp=0;
					decimal=False;
					j=10.0;
					for i in stmp:
						if(not(decimal)):
							if(i!='.'):
								ftmp=ftmp*10+int(i);
							else:
								decimal=True;
						else:
							ftmp=ftmp+(int(i))/j;
							j=j*10;
					diff=ftmp;
					vol=self.area*diff/1000;
					print("Volume:"+str(vol));
					d=datetime.datetime.now();
					if(d.month<10):
						mm='0'+str(d.month);
					else:
						mm=str(d.month);
					#if(d.day<10):
						#dd='0'+str(d.day);
					#else:
						#dd=str(d.day);
					if(d.minute<10):
						dd='0'+str(d.minute);
					else:
						dd=str(d.minute);
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
				playSound();
				GPIO.output(self.motor,True);
				break;
	
