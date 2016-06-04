'''
Created on 19.05.2016

@author: mirko
'''

import schedule
import logging
import threading
import time
from trigger.trigger import Trigger
from .schedulerDataContainer import SchedulerData
from .schedulerDataContainer import SchedulerDataContainer
from trigger.lightDef import cmdToInt

class Scheduler(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__schedulerList = SchedulerDataContainer().schedulerDataList
        self.__trigger = Trigger(None)
        
    def triggerJob(self, schedulerData):
        if not schedulerData.sensorQuery:
            self.__trigger.triggerLightWithSensor(schedulerData.lightID, cmdToInt(schedulerData.targetState), schedulerData.sensorQuery)
        else:
            self.__trigger.triggerLightWithoutSensor(schedulerData.lightID, cmdToInt(schedulerData.targetState))
    
    def triggerOneTimeJob(self, schedulerData):
        self.triggerJob(schedulerData.lightID, schedulerData.targetState, schedulerData.sensorQuery)
        schedulerData.active = False
        return schedule.CancelJob
    
    def addTrigger(self, schedulerData):
        if self.__checkSchedulerData(schedulerData):
            if schedulerData.active:
                self.activateTrigger(schedulerData)
                self.__schedulerList.append(schedulerData)
            else:
                self.__schedulerList.append(schedulerData)
            return True
        else:
            return False

    def __checkSchedulerData(self, schedulerData):
        if schedulerData is None:
            return False
        if (schedulerData.hour is None or schedulerData.minute is None
            or schedulerData.lightID is None):
            return False
        if len(schedulerData.dayOfWeek) == 0:
            schedulerData.once = True
        elif schedulerData.once == True:
            logging.warn("Days and once are specified")
        return True

    def activateTrigger(self, schedulerData):
        
        # Day of Week is ignored (Can't do it on the Webinterface anyway)
        retJobList = []
        if schedulerData.once:
            job = schedule.every().day.at(str(schedulerData.hour)+":"+str(schedulerData.minute)).do(self.triggerOneTimeJob, schedulerData)
            schedulerData.jobs.append(job)
            schedulerData.active = True
            return retJobList.append(job)
            
        if 'Mo' in schedulerData.dayOfWeek:
            job = schedule.every().monday.at(str(schedulerData.hour)+":"+str(schedulerData.minute)).do(self.triggerJob, schedulerData)
            schedulerData.jobs.append(job)
            retJobList.append(job)
            schedulerData.active = True
            pass
        
        if 'Tu' in schedulerData.dayOfWeek:
            job = schedule.every().tuesday.at(str(schedulerData.hour)+":"+str(schedulerData.minute)).do(self.triggerJob, schedulerData)
            schedulerData.jobs.append(job)
            retJobList.append(job)
            schedulerData.active = True
            pass

        if 'We' in schedulerData.dayOfWeek:
            job = schedule.every().wednesday.at(str(schedulerData.hour)+":"+str(schedulerData.minute)).do(self.triggerJob, schedulerData)
            schedulerData.jobs.append(job)
            retJobList.append(job)
            schedulerData.active = True
            pass
        
        if 'Th' in schedulerData.dayOfWeek:
            job = schedule.every().thursday.at(str(schedulerData.hour)+":"+str(schedulerData.minute)).do(self.triggerJob, schedulerData)
            schedulerData.jobs.append(job)
            retJobList.append(job)
            schedulerData.active = True
            pass
        
        if 'Fr' in schedulerData.dayOfWeek:
            job = schedule.every().friday.at(str(schedulerData.hour)+":"+str(schedulerData.minute)).do(self.triggerJob, schedulerData)
            schedulerData.jobs.append(job)
            retJobList.append(job)
            schedulerData.active = True
            pass
        
        if 'Sa' in schedulerData.dayOfWeek:
            job = schedule.every().saturday.at(str(schedulerData.hour)+":"+str(schedulerData.minute)).do(self.triggerJob, schedulerData)
            schedulerData.jobs.append(job)
            retJobList.append(job)
            schedulerData.active = True
            pass
        
        if 'Su' in schedulerData.dayOfWeek:
            job = schedule.every().sunday.at(str(schedulerData.hour)+":"+str(schedulerData.minute)).do(self.triggerJob, schedulerData)
            schedulerData.jobs.append(job)
            retJobList.append(job)
            schedulerData.active = True
            pass
        
        return retJobList
        
    def activateTriggerByID(self, idx):
        sd = self.__schedulerList[idx]
        sd.active = True
        self.activateTrigger(sd)
        
    def deactivateTrigger(self, scheduleData):
        for job in scheduleData.jobs:
            schedule.cancel_job(job)
        scheduleData.active = False
        
    def deleteTriggerByJob(self, job):
        schedule.cancel_job(job)
        for schedulerData in self.__schedulerList:
            if job in schedulerData.jobs:
                if len(schedulerData.jobs) == 1:
                    self.__schedulerList.remove(schedulerData)
                else:
                    schedulerData.jobs.remove(job)
        
    def deleteTriggerByID(self, index):
        if index > len(self.__schedulerList)-1:
            return False
        for job in self.__schedulerList[index].jobs:
            schedule.cancel_job(job)
        del self.__schedulerList[index]
        return True
        
    def replaceTriggerByID(self, index, schedulerData):
        if index > len(self.__schedulerList)-1:
            return False
        for job in self.__schedulerList[index].jobs:
            schedule.cancel_job(job)
        self.__schedulerList[index] = schedulerData
        self.activateTrigger(schedulerData)
        return True
        
    def createTrigger(self, schedulerData):
        trigger = Trigger(schedulerData.sensorQuery)
        self.__triggerList.append((trigger, schedulerData))
        return trigger
        
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
    dat.hour = 23
    dat.minute = 47
    dat.once = True
    dat.lightID = 'SZ1'
    dat.targetState = 'on'
    dat.sensorQuery = 'sz'
    dat.active = True
    
    dat1 = SchedulerData()
    dat1.hour = 23
    dat1.minute = 48
    dat1.once = True
    dat1.lightID = 'SZ1'
    dat1.targetState = 'off'
    dat1.sensorQuery = 'sz'
    dat1.active = True

    scheduler = Scheduler()
    scheduler.addTrigger(dat)
    scheduler.addTrigger(dat1)
    
    schedulerContainer = SchedulerDataContainer()
    
    schedulerEventLoop = scheduler.run_continuously(30)
    
    time.sleep(180)
    
    schedList = scheduler.getSchedulerData()
    
    scheduler.deleteTriggerByJob(schedList[0].job)
    scheduler.deleteTriggerByID(0)
    pass
    