'''
Created on 19.05.2016

@author: mirko
'''

import schedule
import logging
import threading
import time
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
        self.active     = False # just for displaying in Web
    

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
        self.triggerJob(light, targetState, sensor)
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
    
    def run_continuously(self, interval=1):
        """Continuously run, while executing pending jobs at each elapsed
        time interval.
        @return cease_continuous_run: threading.Event which can be set to
        cease continuous run.
        Please note that it is *intended behavior that run_continuously()
        does not run missed jobs*. For example, if you've registered a job
        that should run every minute and you set a continuous run interval
        of one hour then your job won't be run 60 times at each interval but
        only once.
        """
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run
        
if __name__ == '__main__':
    FORMAT = '%(asctime)s %(module)s:%(funcName)s:%(lineno)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    dat = SchedulerData()
    dat.hour = 0
    dat.minute = 00
    dat.once = True
    dat.lightID = 'SZ1'
    dat.targetState = 'on'
    dat.sensorQuery = 'sz'
    
    dat1 = SchedulerData()
    dat1.hour = 0
    dat1.minute = 01
    dat1.once = True
    dat1.lightID = 'SZ1'
    dat1.targetState = 'off'
    dat1.sensorQuery = 'sz'

    scheduler = Scheduler()
    scheduler.addTrigger(dat)
    scheduler.addTrigger(dat1)
    
    schedulerEventLoop = scheduler.run_continuously(60)
    
    time.sleep(300)
    
    schedList = scheduler.getSchedulerData()
    
    scheduler.deleteTriggerByJob(schedList[0].job)
    scheduler.deleteTriggerByID(0)
    pass
    