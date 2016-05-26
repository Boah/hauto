'''
Created on 17.05.2016

@author: mirko
'''

import socket
import sys
import logging
from lightStatusStore.lightStatusStore import LightStatusStore

class SocketInterface(object):
    def __init__(self):
        self.PORT = 45455
        self.statusStore = LightStatusStore()

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
            input_ = clientsocket.recv(1024)
            output = self.parseInput(input_)
            clientsocket.sendall(output)
            clientsocket.close()
            if output == 'exit':
                sys.exit(0)
            
    def parseInput(self, input_):
        inputData = input_.decode("utf-8")
        if (inputData.lower() == "getstat" or inputData.lower() == "getstatus"):
            outdata = self.statusStore.getStatusAsString()
            return outdata

        return None
    
if __name__ == '__main__':
    FORMAT = '%(asctime)s %(module)s:%(funcName)s:%(lineno)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    sinf = SocketInterface()
    sinf.startLightServer()