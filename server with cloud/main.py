from server import *
if __name__=='__main__':
	try:
		receiver=Receiver()
		receiver.startCommunication()
	except KeyboardInterrupt:
		pass 
	finally:
		print "Interrupted"
		GPIO.cleanup()

