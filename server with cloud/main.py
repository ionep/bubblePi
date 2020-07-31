from server import *
import traceback
import logging
if __name__=='__main__':
	try:
		receiver=Receiver()
		receiver.startCommunication()
	#except KeyboardInterrupt:
	#	pass 
	except Exception as e:
		print e.message;
		logging.error(traceback.format_exc());
	finally:
		logging.error(traceback.format_exc());
		print "Interrupted"
		GPIO.cleanup()

