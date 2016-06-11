'''
Created on 24.05.2016

@author: mirko
'''

import logging

class SchedulerData(object):
    
    def __init__(self):
        self.dayOfWeek = []
        self.hour = None
        self.minute = None
        self.once = False
        self.lightID = None
        self.targetState = 'off'
        self.sensorQuery = None
        self.jobs = []
        self.active = False  # just for displaying in Web
        
    def __str__(self):
        msg = str(self.lightID) + "=" + str(self.targetState)
        msg += " DayOfWeek="
        for day in self.dayOfWeek:
            if isinstance(day, str):
                if day.lower() == 'mo' or day.lower() == 'tu' or day.lower() == 'we'or day.lower() == 'th' or day.lower() == 'fr' or day.lower() == 'sa' or day.lower() == 'su':
                    msg += str(day) + "/"
        msg += " Hour=" + str(self.hour)
        msg += " Minute=" + str(self.minute)
        if self.once or len(self.dayOfWeek) == 0:
            msg += " Once=True"
        else:
            msg += " Once=False"
        msg += " sensor=" + str(self.sensorQuery)
        msg += " active=" + str(self.active)
        
        return msg
    
    def fromString(self, string):
        cmdList = string.split()
        for cmd in cmdList:
            if "=" in cmd:
                cmdPart = cmd.split("=")
                if cmdPart[0].lower() == 'wz1' or cmdPart[0].lower() == 'wz2' or cmdPart[0].lower() == 'sz1':
                    self.lightID = cmdPart[0]
                    self.targetState = cmdPart[1]
                if cmdPart[0].lower() == 'hour':
                    self.hour = cmdPart[1]
                if cmdPart[0].lower() == 'minute':
                    self.minute = cmdPart[1]
                if cmdPart[0].lower() == 'active':
                    if cmdPart[1].lower() == 'true':
                        self.active = True
                    else:
                        self.active = False
                if cmdPart[0].lower() == 'sensor':
                    if cmdPart[1].lower() != 'none':
                        self.sensorQuery = cmdPart[1]
                if cmdPart[0].lower() == 'dayofweek' or cmdPart[0].lower() == 'dow':
                    self.dayOfWeek = cmdPart[1].split('/')
                    for entry in self.dayOfWeek:
                        if not isinstance(entry, str):
                            self.dayOfWeek.remove(entry)
        
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
            logging.warning("Days and once are specified")
        return True
    
    def toFile(self, fileName='/var/log/schedData'):
        try:
            with open(fileName, 'w') as file:
                file.write(self.__str__())
        except:
            logging.warning("Could not write Backup File " + str(fileName))
            
    def fromFile(self, fileName='/var/log/schedData'):
        try:
            with open(fileName, 'r') as file:
                input_ = file.read()
        except:
            logging.warning("Could not read from File " + str(fileName))
            return False
        inputList = input_.splitlines()
        for idx, line in enumerate(inputList):
            schedulerData = SchedulerData()
            schedulerData.fromString(line)
            if len(schedulerData.dayOfWeek) == 0:
                schedulerData.once = True
            if self.checkSchedulerData(schedulerData):
                self.schedulerDataList.append(schedulerData)
            else:
                logging.warn("Could not add line " + str(idx) + " from File " + str(fileName))
        return True
