import socket
import struct
import pickle
import cv2
import cv2.cv as cv

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
	c = cv2.waitKey(1) & 0xFF
	d = sock.recvfrom(65536)
	data = d[0]
	addr = d[1]
	print addr
	buf = pickle.loads(data)
	#print buf
	frame = cv2.imdecode(buf,0)
	#print frame
	cv2.imshow('serverRecieving',frame)
	if c==ord('q'):
		break
sock.close()
