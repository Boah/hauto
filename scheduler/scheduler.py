'''
Created on 19.05.2016

@author: mirko
'''

import schedule
import logging
from trigger.trigger import Trigger

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
    

class Scheduler(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__schedulerList = []
        self.__trigger = Trigger(None)
        
    def triggerJob(self, light, targetState, sensor):
        if not sensor:
            self.__trigger.triggerLightWithSensor(light, self.__cmdToInt(targetState), sensor)
        else:
            self.__trigger.triggerLightWithoutSensor(light, self.__cmdToInt(targetState))
    
    def triggerOneTimeJob(self, light, targetState, sensor):
        self.triggerJob(targetState)
        return schedule.CancelJob
    
    def addTrigger(self, schedulerData):
        # Day of Week is ignored (Can't do it on the Webinterface anyway)
        if schedulerData.once:
            job = schedule.every().day.at(str(schedulerData.hour)+":"+str(schedulerData.minute)).do(self.triggerOneTimeJob, schedulerData.lightID, schedulerData.targetState, schedulerData.sensorQuery)
            schedulerData.job = job
            self.__schedulerList.append(schedulerData)
            return job
            
        if 'monday' in schedulerData.dayOfWeek:
            pass
        
    def deleteTriggerByJob(self, job):
        schedule.cancel_job(job)
        for schedulerData in self.__schedulerList:
            if job == schedulerData.job:
                self.__schedulerList.remove(schedulerData)
        
    def deleteTriggerByID(self, index):
        schedule.cancel_job(self.__schedulerList[index].job)
        del self.__schedulerList[index]
        
    def createTrigger(self, schedulerData):
        trigger = Trigger(schedulerData.sensorQuery)
        self.__triggerList.append((trigger, schedulerData))
        return trigger
    
    def __cmdToInt(self, cmd):
        if cmd.lower() == 'on':
            return 1
        if cmd.lower() == 'off':
            return 0
        
    def getSchedulerData(self):
        return self.__schedulerList
        
if __name__ == '__main__':
    FORMAT = '%(asctime)s %(module)s:%(funcName)s:%(lineno)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    dat = SchedulerData()
    dat.hour = 9
    dat.minute = 30
    dat.once = True
    dat.lightID = 'SZ1'
    dat.targetState = 'on'
    dat.sensorQuery = 'sz'
    
    dat1 = SchedulerData()
    dat1.hour = 9
    dat1.minute = 45
    dat1.once = True
    dat1.lightID = 'SZ1'
    dat1.targetState = 'off'
    dat1.sensorQuery = 'sz'

    scheduler = Scheduler()
    scheduler.addTrigger(dat)
    scheduler.addTrigger(dat1)
    
    schedList = scheduler.getSchedulerData()
    
    scheduler.deleteTriggerByJob(schedList[0].job)
    scheduler.deleteTriggerByID(0)
    pass
    