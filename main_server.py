import socket
import threading
import SocketServer
import loginCheck
import pickle
import json

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        if data=="login":
        	self.request.sendall("requesting login data")
        	usr = self.request.recv(1024)
        	self.request.sendall("ack")
        	pwd = self.request.recv(1024)
        	a = loginCheck.login(usr,pwd)
        	login_val = a[2]
        	print login_val
        	if(login_val==2):
        		print "student"
        	self.request.sendall(pickle
        		.dumps(a))



class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
	# Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 5566
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    print "ip: ",ip
    print "port: ",port

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name
    while(1):
    	inp = raw_input('1.Send client\n2.shutdown server')

    	if inp == "1":
    		client(ip, port, "Hello World")
    	if inp == "2":
			server.shutdown()
			break	
		
		
