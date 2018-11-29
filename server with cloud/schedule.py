from dbtest import *
from urllib import urlencode
import urllib2

count=0;
db=Database();
url="http://localhost/test.php";
while(count!=10):
	query="""SELECT * FROM consumption WHERE sent='False'""";
	num,data=db.query(query);
	if(num>0):
		for d in data:
			json={
				'date':d['date'],
				'volume':d['volume']
			}
			encoded=urlencode(json);
			link=urllib2.urlopen(url,encoded);
			result=link.read();
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
