import cv2
import cv2.cv as cv
import pickle
import socket
import struct
cap = cv2.VideoCapture(-1) 
cap.set(3,160)
cap.set(4,120)

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
while True:
	ret, frame = cap.read()
	cv2.imshow('clientSending',frame)
	c = cv2.waitKey(1) & 0xFF
	(retval,buf) = cv2.imencode(".jpg",frame)
	ser = pickle.dumps(buf)
	sock.sendto(ser, (MCAST_GRP, MCAST_PORT))
	if c == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()
#sock.sendto("robot", (MCAST_GRP, MCAST_PORT))
