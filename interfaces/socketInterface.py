'''
Created on 17.05.2016

@author: mirko
'''

import socket
import sys
import logging
import time
from lightStatusStore.lightStatusStore import LightStatusStore
from scheduler.schedulerDataContainer import SchedulerData
from scheduler.schedulerDataContainer import SchedulerDataContainer
from scheduler.scheduler import Scheduler
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
        self.__nackString = 'ERROR'
        self.statusStore = LightStatusStore()
        self.schedulerContainer = SchedulerDataContainer()
        self.trigger = Trigger()
        self.scheduler = Scheduler()
    
    def startLightServer(self):
        #create an INET, STREAMing socket
        serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        #bind the socket to a public host,
        # and a well-known port
        #serversocket.bind(('localhost', self.PORT))
        try:
            serversocket.bind((socket.gethostname(), self.PORT))
        except:
            logging.warn("Could not bind at Port: " + str(self.PORT) + ". Waiting 60s...")
            time.sleep(60)
            try:
                serversocket.bind((socket.gethostname(), self.PORT))
            except:
                logging.warn("Could not bind at Port: " + str(self.PORT) + ". Waiting 60s...")
                time.sleep(60)
                try:
                    serversocket.bind((socket.gethostname(), self.PORT))
                except:
                    logging.error("Could not bind at Port: " + str(self.PORT))
                    sys.exit(1)
        logging.info("Binding at Port " + str(self.PORT) + " succeeded.")
        #become a server socket
        serversocket.listen(5)
        
        while 1:
            #accept connections from outside
            (clientsocket, address) = serversocket.accept()
            input_ = clientsocket.recv(1024)
            output = self.parseInput(input_)
            if output:
                clientsocket.sendall(output.encode())
            else:
                clientsocket.sendall(self.__nackString.encode())
            clientsocket.close()
            if output == 'exit':
                sys.exit(0)
            
    def parseInput(self, input_):
        if not isinstance(input_, str):
            inputData = input_.decode('utf-8')
        else:
            inputData = input_
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
                if (self.trigger.triggerLightWithSensor(lightCmd.light, lightCmd.cmd, lightCmd.sensor)):
                    return self.__ackString
                else:
                    return self.__nackString
            else:
                if(self.trigger.triggerLightWithoutSensor(lightCmd.light, lightCmd.cmd)):
                    return self.__ackString
                else:
                    return self.__nackString
            return self.__nackString
        if (inputData.lower().startswith("addse") or inputData.lower().startswith("addscheduleentry")):
            return self.__parseAddScheduleEntryCommand(inputData)
        if (inputData.lower().startswith("changese") or inputData.lower().startswith("changescheduleentry")):
            return self.__parseChangeScheduleEntryCommand(inputData)
        if (inputData.lower().startswith("deletese") or inputData.lower().startswith("deletescheduleentry")):
            return self.__parseDeleteScheduleEntryCommand(inputData)
        if (inputData.lower().startswith("remove") or inputData.lower().startswith("delete")):
            cmd = inputData.split(" ")
            try:
                entry = int(cmd[1])
            except:
                return self.__nackString
            if self.scheduler.deleteTriggerByID(entry):
                return self.__ackString
            else:
                return self.__nackString
        if (inputData.lower() == "exit"):
            logging.info("Got Exit Signal via Socket")
            return "exit"
        
        return self.__nackString
    
    def __parseAddScheduleEntryCommand(self, inputData):
        schedulerData = SchedulerData()
        cmdList = inputData.split()
        for cmd in cmdList:
            if not cmd.lower().startswith("adds"):
                if "=" in cmd:
                    cmdPart = cmd.split("=")
                    if cmdPart[0].lower() == 'wz1' or cmdPart[0].lower() == 'wz2' or cmdPart[0].lower() == 'sz1':
                        schedulerData.lightID = cmdPart[0]
                        schedulerData.targetState = cmdPart[1]
                    if cmdPart[0].lower() == 'hour':
                        schedulerData.hour = cmdPart[1]
                    if cmdPart[0].lower() == 'minute':
                        schedulerData.minute = cmdPart[1]
                    if cmdPart[0].lower() == 'active':
                        schedulerData.active = cmdPart[1]
                    if cmdPart[0].lower() == 'sensor':
                        schedulerData.sensorQuery = cmdPart[1]
                    if cmdPart[0].lower() == 'dayofweek' or cmdPart[0].lower() == 'dow':
                        schedulerData.dayOfWeek = cmdPart[1].split('/')
        if len(schedulerData.dayOfWeek) == 0:
            schedulerData.once = True
        if self.scheduler.addTrigger(schedulerData):
            return self.__ackString
        else:
            return self.__nackString
    
    def __parseChangeScheduleEntryCommand(self, inputData):
        # changeScheduleEntry: entry=1 WZ1=off Hour=8 Minute=15 active=True sensor=sz
        schedulerData = SchedulerData()
        cmdList = inputData.split()
        for cmd in cmdList:
            if not cmd.lower().startswith("changes"):
                if "=" in cmd:
                    cmdPart = cmd.split("=")
                    if cmdPart[0].lower() == 'wz1' or cmdPart[0].lower() == 'wz2' or cmdPart[0].lower() == 'sz1':
                        schedulerData.lightID = cmdPart[0]
                        schedulerData.targetState = cmdPart[1]
                    if cmdPart[0].lower() == 'hour':
                        schedulerData.hour = cmdPart[1]
                    if cmdPart[0].lower() == 'minute':
                        schedulerData.minute = cmdPart[1]
                    if cmdPart[0].lower() == 'active':
                        schedulerData.active = cmdPart[1]
                    if cmdPart[0].lower() == 'sensor':
                        schedulerData.sensorQuery = cmdPart[1]
                    if cmdPart[0].lower() == 'dayofweek' or cmdPart[0].lower() == 'dow':
                        schedulerData.dayOfWeek = cmdPart[1].split('/')
                    if cmdPart[0].lower() == 'entry':
                        entry = int(cmdPart[1])
        if len(schedulerData.dayOfWeek) == 0:
            schedulerData.once = True
        if(self.scheduler.replaceTriggerByID(entry, schedulerData)):
            return self.__ackString
        else:
            return self.__nackString
        
    def __parseDeleteScheduleEntryCommand(self, inputData):
        # deleteScheduleEntry: entry=1
        cmdList = inputData.split()
        for cmd in cmdList:
            if not cmd.lower().startswith("changes"):
                if "=" in cmd:
                    cmdPart = cmd.split("=")
                    if cmdPart[0].lower() == 'entry':
                        entry = int(cmdPart[1])
        if(self.scheduler.deleteTriggerByID(entry)):
            return self.__ackString
        else:
            return self.__nackString
    
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