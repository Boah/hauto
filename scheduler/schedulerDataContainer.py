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
        
class SchedulerDataContainer(object):
    '''
    I am Borg
    '''
    
    __shared_state = {}
    schedulerDataList = []
    
    def __init__(self):
        self.__dict__ = self.__shared_state
    
