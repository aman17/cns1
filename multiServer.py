import sys
from PyQt4 import QtGui, QtCore, uic
from Queue import *
from threading import Thread
import cv2
import cv2.cv as cv
import pickle
import socket
import struct
import numpy as np
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot

cap = cv2.VideoCapture(-1) 
#cap = cv2.VideoCapture('output.avi')
cap.set(3,160)
cap.set(4,120)
# Define the codec and create VideoWriter object
#fourcc = cv.CV_FOURCC('X','V','I','D')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (160,120))

q = Queue()
class RecvThreadTcp(QtCore.QThread):
	def __init__(self, tcp):
		QtCore.QThread.__init__(self)
		self.tcp = tcp
 	def run(self):
 		self.tcp.listen(1)
 		self.conn, self.addr = self.tcp.accept()
 		read = self.conn.recv(1024)
 		print read
 		self.conn.send("ack")
 		if read=="live":
 			self.emit(QtCore.SIGNAL('StartSending'))
 		return

class CameraCapture(QtCore.QThread):
	def __init__(self):
		QtCore.QThread.__init__(self)
 	def run(self):
 		while True:
 			ret, frame = cap.read()
 			print frame
 			if ret:
	 			#out.write(frame)
				#print "aman",frame
				(retval,buf) = cv2.imencode(".jpg",frame)
				ser = pickle.dumps(buf)
	 			self.emit(QtCore.SIGNAL('captureNow'),ser)
	 			c = cv2.waitKey(50) & 0xFF
	 			if c==ord('q'):
	 				break
	 		else:
	 			print "break"
	 			break
	 	print "oner"
 		return
class TestApp(QtGui.QMainWindow):
	def __init__(self):
		print "check check"
		QtGui.QMainWindow.__init__(self)
		self.ui = uic.loadUi('mainWindow.ui')
		self.ui.show()
		print "loaded..."
		self.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.buttonFn)
		self.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), self.buttonFn_2)


		self.MCAST_GRP = '224.1.1.1'
		self.MCAST_PORT = 5009
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)


		self.TCP_IP = '127.0.0.1'
		self.TCP_PORT = 5051
		self.BUFFER_SIZE_TCP = 20
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((self.TCP_IP, self.TCP_PORT))
		self.rcv = RecvThreadTcp(self.s)
		self.connect(self.rcv,QtCore.SIGNAL('StartSending'),self.buttonFn)
		self.rcv.start()
	def runCap(self,text):
		#print text
		buff = pickle.loads(text)
		
		frame = cv2.imdecode(buff,0)
		#print frame
		cv2.imshow('serverSending',frame)
			
		self.sock.sendto(text, (self.MCAST_GRP, self.MCAST_PORT))
		#cv2.imshow('showint',frame)

	def buttonFn(self):
		self.capture = CameraCapture()
		self.connect(self.capture,QtCore.SIGNAL('captureNow'),self.runCap)
		
 		'''self.MCAST_GRP = '224.1.1.1'
		self.MCAST_PORT = 5007
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)'''

		print "socket created.."
		self.capture.start()
	def buttonFn_2(self):
		cap.release()
		#out.release()
		q.put(0)
		print "entered 0 in q...."
def main():
	app = QtGui.QApplication(sys.argv)
	win = TestApp()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
