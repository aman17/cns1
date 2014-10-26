import sys
from PyQt4 import QtGui, QtCore, uic
from Queue import *
from threading import Thread
import cv2
import cv2.cv as cv
import pickle
import socket
import struct	
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot

cap = cv2.VideoCapture(-1) 
cap.set(3,160)
cap.set(4,120)

q = Queue()
frameQueue = Queue()

class CameraCapture(QtCore.QThread):
	def __init__(self):
		QtCore.QThread.__init__(self)
 	def run(self):
 		while True:
 			ret, frame = cap.read()
			#print "aman",frame
			(retval,buf) = cv2.imencode(".jpg",frame)
			ser = pickle.dumps(buf)
	 		self.emit(QtCore.SIGNAL('captureNow'),ser)
	 		c = cv2.waitKey(1) & 0xFF
	 		if c==ord('q'):
	 			break
 		return
		'''for i in range(6):
			time.sleep(0.3) # artificial time delay
			self.emit( QtCore.SIGNAL('anysignal'), "from work thread " + str(i) )
  		return'''
 

class TestApp(QtGui.QMainWindow):
	def __init__(self):
		print "check check"
		QtGui.QMainWindow.__init__(self)
		self.ui = uic.loadUi('mainWindow.ui')
		self.ui.show()
		print "loaded..."
		self.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.buttonFn)
		self.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), self.buttonFn_2)

	def runCap(self,text):
		'''ret, frame = cap.read()
		print "aman",frame
		(retval,buf) = cv2.imencode(".jpg",frame)
		ser = pickle.dumps(buf)'''
		#print text
		self.sock.sendto(text, (self.MCAST_GRP, self.MCAST_PORT))
		#cv2.imshow('showint',frame)

	def buttonFn(self):
		self.capture = CameraCapture()
		self.connect(self.capture,QtCore.SIGNAL('captureNow'),self.runCap)
		
 		self.MCAST_GRP = '224.1.1.1'
		self.MCAST_PORT = 5007
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		print "socket created.."
		self.capture.start()
	'''try:
		t1 = Thread(target =startServer,args=(q,))
		t1.start()
		#thread.start_new_thread(startServer,("thread1",))
		print "aman"
		#return t1
	except:
		print "Error unable to start thread"
	print "Checking when does it comes here... :)"
	if not frameQueue.empty():
			print frameQueue.get()'''
	def buttonFn_2():
		q.put(0)
		print "entered 0 in q...."

'''def startServer(in_q):
	frameSig = showSomething()
	frameSig.gotFrame.connect(showFrame)
	MCAST_GRP = '224.1.1.1'
	MCAST_PORT = 5007
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
	val = in_q.empty()
	while val:
		#ret, frame = cap.read()
		#cam = cv.CaptureFromCAM(-1)
		#feed = cv.QueryFrame(cam)
		#frameSig.emmiter(feed)
		#cv.WaitKey(-1)
		#frameQueue.put(frame)
		#print "frame:   ", frame
		#cv2.imshow('clientSending',frame)
		#c = cv2.waitKey(1) & 0xFF
		(retval,buf) = cv2.imencode(".jpg",frame)
		ser = pickle.dumps(buf)
		frameQueue.put(ser)
		frameSig.emmiter(ser)
		#sock.sendto(ser, (MCAST_GRP, MCAST_PORT))
		#if c == ord('q'):
			#break
		val = in_q.empty()
		if val == False:
			read = in_q.get()
			if read ==  0:
				break
	cap.release()
	cv2.destroyAllWindows()
'''

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	win = TestApp()
	sys.exit(app.exec_())
#sock.sendto("robot", (MCAST_GRP, MCAST_PORT))
