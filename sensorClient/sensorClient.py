'''
Created on 17.05.2016

@author: mirko
'''

import socket


class LightSensorClient(object):
    def __init__(self):
        self.HOST = '192.168.0.11'     # The remote host
        self.PORT = 45454              # The same port as used by the server
    
    def getLightValueFromServer(self, host=None, port=None):
        if port == None:
            port = self.PORT
            
        if host == None:
            host = self.host
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host, port))
        except Exception as ex:
            raise ex
        data = s.recv(1024)
        s.close()
        return float(data.decode("utf-8"))

    def is_valid_ipv4_address(self, address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_aton(address)
            except socket.error:
                return False
            return address.count('.') == 3
        except socket.error:  # not a valid address
            return False
    
        return True