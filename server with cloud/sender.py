from dbtest import *
import urllib
import urllib2

count=0;
id=1;
db=Database();
while(count!=10):
	query="""SELECT * FROM consumption WHERE sent='False'""";
	num,data=db.query(query);
	if(num>0):
		for d in data:
					url="http://localhost/test.php";
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
		break;
