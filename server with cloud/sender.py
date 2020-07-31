from dbtest import *
import urllib
import urllib2
import datetime

count=0;
id=5;
db=Database();
while(count!=10):
	query="""SELECT * FROM consumption WHERE sent='False'""";
	num,data=db.query(query);
	if(num>0):
		for d in data:
					url="http://192.168.1.101/kec-project/public/interface";
					json={
							'id':id,
							'date':d['date'],
							'volume':d['volume']
					}
					# make a string with the request type in it:
					method = "GET";
					handler = urllib2.HTTPHandler()
					opener = urllib2.build_opener(handler)
					data = urllib.urlencode(json)
					url=url+"?"+data;
					request = urllib2.Request(url, data=data)
					request.add_header("Content-Type",'application/json')
					request.get_method = lambda: method
					try:
						connection = opener.open(request)
					except urllib2.HTTPError,e:
						connection = e
													
					# check. Substitute with appropriate HTTP code.
					if connection.code == 200:
						result = connection.read()
					else:
						# handle the error case. connection.read() will still contain data
						# if any was returned, but it probably won't be of any use
						result="false";
													
					if(result=="true"):
						did=d['id'];
						query="""UPDATE consumption SET sent='True' WHERE id=%s"""%(did);
						db.insert(query);
						print("Updated 1 record");
						count=0;
					else:
						print result;
						print("Error in server side");
						count=count+1;
	else:
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
		num,data=db.query(query);
		if(num==0):
			query="""INSERT INTO consumption(date,volume,sent) VALUES(%s,'0','False')"""%(cdate);
			db.insert(query);
			count=0;
			continue;
		else:
			break;

