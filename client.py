import sys
import socket
from Queue import *
import thread
import cv2
import cv2.cv as cv
import pickle
from PyQt4 import QtGui, QtCore, uic
from threading import Thread
q = Queue()
msg = Queue()
class TestApp(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui = uic.loadUi('mainwindow.ui')
		self.ui.show()
		self.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), buttonFn)
		self.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), buttonFn_2)

def buttonFn():
	try:
		#thread.start_new_thread(startServer,(q,))
		t1 = Thread(target =startServer,args=(q,))
		t1.start()
		print "aman"
	except:
		print "Error unable to start thread"
def buttonFn_2():
	q.put(0)
	print "entered 0 in q...."
def startServer(in_q):
	TCP_IP = '127.0.0.1'
	TCP_PORT = 5025
	BUFFER_SIZE = 1024
	MESSAGE = "Hello, World!"	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	while(1):
		print "empty: ",q.empty()
		if q.empty():
			#self.ui = uic.loadUi('chatWindow.ui',)
			ch = raw_input("enter:")
			s.send(ch)
		else:
			read = q.get()
			if read==0:
				break
	print "closing..."
	s.close()
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	win = TestApp()
	sys.exit(app.exec_())
