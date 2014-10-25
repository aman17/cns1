import sys
import socket
import thread
from PyQt4 import QtGui, QtCore, uic
from Queue import *
from threading import Thread
import cv2
import cv2.cv as cv
import pickle
q = Queue()
print "Queue created.."
class TestApp(QtGui.QMainWindow):
	def __init__(self):
		print "check check"
		QtGui.QMainWindow.__init__(self)
		self.ui = uic.loadUi('mainWindow.ui')
		self.ui.show()
		print "loaded..."
		self.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), buttonFn)
		self.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), buttonFn_2)
 		
def buttonFn():
	try:
		t1 = Thread(target =startServer,args=(q,))
		t1.start()
		#thread.start_new_thread(startServer,("thread1",))
		print "aman"
		#return t1
	except:
		print "Error unable to start thread"
	print "Checking when does it comes here... :)"
def buttonFn_2():
		q.put(0)
		print "entered 0 in q...."

def startServer(in_q):
	TCP_IP = '127.0.0.1'
	TCP_PORT = 5025
	BUFFER_SIZE = 20  # Normally 1024, but we want fast response
	print "hello"
	print "Checking for empty: ", in_q.empty()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)
	print "listening"
	conn, addr = s.accept()
	print 'Connection address:', addr
	print "Checking for empty: after", in_q.empty()
	while 1:
		print "empty: ", in_q.empty()
		if in_q.empty():
			data = conn.recv(BUFFER_SIZE)
        	if data:
				print "received data:",data
				win.ui.label.setText(data)
				#win.ui.setWindowTitle(data)	
		else:
			read = in_q.get()
			if read==0:
				break
		print "inside while..."
	    #check = in_q.empty()
        #print "printing q.empty",check
        
	print "Closing Connection..."
	conn.close()
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	win = TestApp()
	sys.exit(app.exec_())
