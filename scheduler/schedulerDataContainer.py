'''
Created on 24.05.2016

@author: mirko
'''


class SchedulerData(object):
    
    def __init__(self):
        self.dayOfWeek  = []
        self.hour       = None
        self.minute     = None
        self.once       = False
        self.lightID    = None
        self.targetState = 'off'
        self.sensorQuery = None
        self.job        = None
        self.active     = False # just for displaying in Web
        
    def __str__(self):
        msg = ""
        msg += "DayOfWeek="
        for day in self.dayOfWeek:
            msg+=str(day)+" "
        msg+=", Hour=" + str(self.hour)
        msg+=", Minute=" + str(self.minute)
        msg+=", Once=" + str(self.once)
        msg+=", LightID=" + str(self.lightID)
        msg+=", TargetState=" + str(self.targetState)
        msg+=", SensorQuery=" + str(self.sensorQuery)
        msg+=", Active=" + str(self.active)
        
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
        return msg
    
