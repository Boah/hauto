'''
Created on 17.05.2016

@author: mirko
'''

import socket

class SocketInterface(object):
    def __init__(self):
        self.PORT = 45455

    def startLightServer(self):
        #create an INET, STREAMing socket
        serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        #bind the socket to a public host,
        # and a well-known port
        serversocket.bind(('localhost', self.PORT))
        #become a server socket
        serversocket.listen(5)
        
        while 1:
            #accept connections from outside
            (clientsocket, address) = serversocket.accept()
            
            clientsocket.close()