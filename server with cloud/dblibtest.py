from dbtest import *
if __name__ == "__main__":

    db = Database()
    aquery="""SELECT * FROM consumption"""
    num,q=db.query(aquery);
    print(num);
	
    ##CleanUp Operation
    ##del_query = "DELETE FROM basic_python_database"
    ##db.insert(del_query)

    ## Data Insert into the table
    #query = """
		#INSERT INTO consumption
        #(date, volume,sent)
        #VALUES
        #('2018/11/23', '10','false'),
        #('2018/11/24', '19','false')
        #"""

    ## db.query(query)
    #db.insert(query)
    
    #select_query = """
        #SELECT * FROM consumption
        #"""

    #data = db.query(select_query)

    #for d in data:
        #print "id= " + str(d['id'])
        #print "date= " + str(d['date'])
        #print "volume= " + str(d['volume'])
        #print "sent= " + str(d['sent'])
    
