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
class liveConnect(QtCore.QThread):
	def __init__(self,sockt,tcp):
		QtCore.QThread.__init__(self)
		self.sockt = sockt
		self.tcp = tcp
 	def run(self):
 		self.tcp.send("live")
 		self.tcp.recv(1024)
 		while True:
 			c = cv2.waitKey(1) & 0xFF
			d = self.sockt.recvfrom(65536)
			data = d[0]
			addr = d[1]
			print addr
			self.emit(QtCore.SIGNAL('display'),data)
			#buf = pickle.loads(data)
			#print buf
			#frame = cv2.imdecode(buf,0)
			#print frame
			#cv2.imshow('serverRecieving',frame)
			if c==ord('q'):
				break
	 	print "oner"
 		return


'''class archiveThread(QtCore.QThread):
	def __init__(self,sockt,tcp):
		QtCore.QThread.__init__(self)
			self.sockt = sockt
		self.tcp = tcp
 	def run(self):
 		return'''


class TestApp(QtGui.QMainWindow):
	def __init__(self):
		print "check check"
		QtGui.QMainWindow.__init__(self)
		self.ui = uic.loadUi('mainwindow.ui')
		self.ui.show()
		print "loaded..."
		self.connect(self.ui.btnLive, QtCore.SIGNAL("clicked()"), self.live)
		self.connect(self.ui.btnArchives, QtCore.SIGNAL("clicked()"), self.archive)
		#self.connect(self.ui.btnArchives, QtCore.SIGNAL("clicked()"), self.buttonFn_2)
		
		self.MCAST_GRP = '224.1.1.1'
		self.MCAST_PORT = 5009
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('', self.MCAST_PORT))
		mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

		self.TCP_IP = '127.0.0.1'
		self.TCP_PORT = 5051
		self.BUFFER_SIZE_TCP = 20
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.TCP_IP, self.TCP_PORT))

	def disp(self, dat):
		buf = pickle.loads(dat)
		#print buf
		frame = cv2.imdecode(buf,0)
		cv2.imshow('ClientRecieving',frame)
		#print frame

	def archive(self):
		print "aman"

	def live(self):
		self.lc = liveConnect(self.sock,self.s)
		self.connect(self.lc,QtCore.SIGNAL('display'),self.disp)
		self.lc.start()

def main():
	app = QtGui.QApplication(sys.argv)
	win = TestApp()
	sys.exit(app.exec_())
if __name__ == "__main__":
	main()
