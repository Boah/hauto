'''
Created on 17.05.2016

@author: mirko
'''

import socket
import sys
import logging
from lightStatusStore.lightStatusStore import LightStatusStore
from scheduler.schedulerDataContainer import SchedulerDataContainer
from trigger.trigger import Trigger

class LightCommand(object):
    def __init__(self):
        self.light = None
        self.cmd = None
        self.sensor = None

class SocketInterface(object):
    def __init__(self):
        self.PORT = 45455
        self.__ackString = 'ACK'
        self.statusStore = LightStatusStore()
        self.schedulerContainer = SchedulerDataContainer()
        self.trigger = Trigger()

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
        if (inputData.lower() == "getsched" or inputData.lower() == "getschedule"):
            outdata = str(self.schedulerContainer)
            return outdata
        if (inputData.lower().startswith("triggerlight")):
            #TriggerLightCommand: triggerLight SZ1=on sensor=kitchen
            lightCmd = self.__parseLightCommand(inputData)
            if lightCmd.sensor:
                self.trigger.triggerLightWithSensor(lightCmd.light, lightCmd.cmd, lightCmd.sensor)
            else:
                self.trigger.triggerLightWithoutSensor(lightCmd.light, lightCmd.cmd)
            return self.__ackString
        if (inputData.lower() == "exit"):
            logging.info("Got Exit Signal via Socket")
            return "exit"
        
        return None
    
    def __parseLightCommand(self, cmd):
        lightCmd = LightCommand()
        cmdList = cmd.split()
        for cmdPart in cmdList:
            if not cmdPart.lower().startswith("triggerlight"):
                if "=" in cmdPart:
                    cmdPartSpec = cmdPart.split("=")
                    if len(cmdPartSpec) != 2:
                        logging.error("Command not recognized")
                        break
                    if cmdPartSpec[0].lower() == "wz1" or cmdPartSpec[0].lower() == "wz2" or cmdPartSpec[0].lower() == "sz1":
                        lightCmd.light = cmdPartSpec[0]
                        lightCmd.cmd = cmdPartSpec[1]
                    if cmdPartSpec[0].lower() == "sensor":
                        lightCmd.sensor = cmdPartSpec[1]
        return lightCmd
    
if __name__ == '__main__':
    FORMAT = '%(asctime)s %(module)s:%(funcName)s:%(lineno)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    sinf = SocketInterface()
    sinf.startLightServer()