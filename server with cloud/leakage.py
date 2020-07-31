from dbtest import *
import datetime


class Leakage:
	
	db=Database();
	def __init__(self,data):
		startTime=45;
		stopTime=39;
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
		if(d.minute==startTime):
			query="""SELECT * FROM leakage WHERE datetime=%s"""%(cdate);
			num,dbData=self.db.query(query);
			if(num<=0):
				query="""INSERT INTO leakage(initial,datetime) VALUES(%s,%s)"""%(data,cdate);
				self.db.insert(query);
		elif(True):#elif(d.minute==stopTime):
			query="""SELECT * FROM leakage WHERE datetime=%s"""%(cdate);
			num,dbData=self.db.query(query);
			if(num>0):
				
				query="""UPDATE leakage SET final=%s WHERE sn=%s"""%(data,dbData[0]['sn']);
				self.db.insert(query);
				
			#check for leakage
			query="""SELECT * FROM leakage WHERE leakage='test' ORDER BY datetime DESC""";
			num,dbData=self.db.query(query);
			if(num>0):
				count=0;
				leakcount=0;
				
				diff1=0;
				diff2=0;
				for row in range(len(dbData)):
					if(dbData[row]['leakage']=='test'):
						diff2=diff1;
						diff1=abs(dbData[row]['initial']-dbData[row]['final']);
						if(diff1>=1 and abs(diff2-diff1)<=1):
							leakcount+=1;
							print("Leakage");
						count+=1;
				print(str(leakcount));
				if(leakcount>6):
					for row in range(len(dbData)):
						query="""UPDATE leakage SET leakage='true' WHERE sn=%s"""%(dbData[row]['sn']);
						self.db.insert(query);
						#led or buzzer or speaker
				else:
					#register older data than 7 days to not leaking
					if(count>7):
						i=0;
						for row in range(len(dbData)):
							#not to register data within 7 days
							if(i<6):
								i+=1;
								continue;
							else:
								query="""UPDATE leakage SET leakage='false' WHERE sn=%s"""%(dbData[row]['sn']);
								print("No leakage");
								self.db.insert(query);
							
				

leakage=Leakage(12);
