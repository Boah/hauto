'''
Created on 24.05.2016

@author: mirko
'''

import logging

class SchedulerData(object):
    
    def __init__(self):
        self.dayOfWeek  = []
        self.hour       = None
        self.minute     = None
        self.once       = False
        self.lightID    = None
        self.targetState = 'off'
        self.sensorQuery = None
        self.jobs        = []
        self.active     = False # just for displaying in Web
        
    def __str__(self):
        msg=str(self.lightID)+"=" + str(self.targetState)
        msg += " DayOfWeek="
        for day in self.dayOfWeek:
            msg+=str(day)+"/"
        msg+=" Hour=" + str(self.hour)
        msg+=" Minute=" + str(self.minute)
        msg+=" Once=" + str(self.once)
        msg+=" sensor=" + str(self.sensorQuery)
        msg+=" active=" + str(self.active)
        
        return msg
        
class SchedulerDataContainer(object):
    '''
    I am Borg
    '''
    
    __shared_state = {}
    schedulerDataList = []
    
    def __init__(self):
        self.__dict__ = self.__shared_state
        
    def __str__(self):
        msg = ""
        for entry in self.schedulerDataList:
            msg += str(entry) + '\n'
        if msg == "":
            msg = 'empty'
        return msg
    
    def checkSchedulerData(self, schedulerData):
        if schedulerData is None:
            return False
        try:
            h = int(schedulerData.hour)
            if h > 23 or h < 0:
                return False
        except:
            return False
        try:
            m = int(schedulerData.minute)
            if m > 59 or m < 0:
                return False
        except:
            return False
        if (schedulerData.hour is None or schedulerData.minute is None
            or schedulerData.lightID is None):
            return False
        if len(schedulerData.dayOfWeek) == 0:
            schedulerData.once = True
        elif schedulerData.once == True:
            logging.warn("Days and once are specified")
        return True
    
    def toFile(self, fileName):
        try:
            with open(fileName, 'w') as file:
                file.write(self.__str__())
        except:
            logging.warn("Could not write Backup File " + str(fileName))
            
    def fromFile(self, fileName):
        try:
            with open(fileName, 'r') as file:
                input_ = file.read()
        except:
            logging.warn("Could not read from File " + str(fileName))
            return False
        inputList = input_.splitlines()
        for line in inputList:
            schedulerData = SchedulerData()
            cmdList = line.split()
            for idx, cmd in enumerate(cmdList):
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
                        if cmdPart[1].lower() == 'true':
                            schedulerData.active = True
                        else:
                            schedulerData.active = False
                    if cmdPart[0].lower() == 'sensor':
                        schedulerData.sensorQuery = cmdPart[1]
                    if cmdPart[0].lower() == 'dayofweek' or cmdPart[0].lower() == 'dow':
                        schedulerData.dayOfWeek = cmdPart[1].split('/')
                        if None in schedulerData.dayOfWeek:
                            schedulerData.dayOfWeek.remove(None)
            if len(schedulerData.dayOfWeek) == 0:
                schedulerData.once = True
            if self.checkSchedulerData(schedulerData):
                self.schedulerDataList.append(schedulerData)
            else:
                logging.warn("Could not add line " + str(idx) + " from File " + str(fileName))
        return True
