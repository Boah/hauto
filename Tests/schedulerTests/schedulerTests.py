'''
Created on 04.06.2016

@author: mirko
'''
import unittest
import schedule
from datetime import date
from scheduler.schedulerDataContainer import SchedulerData
from scheduler.scheduler import Scheduler

class Test(unittest.TestCase):

    scheduler = Scheduler()

    def setUp(self):
        schedule.clear()
        pass


    def tearDown(self):
        pass


    def testActivateOnceTrigger(self):
        sdata = SchedulerData()
        sdata.hour      = 23
        sdata.minute    = 59
        sdata.once      = True
        sdata.lightID   = "SZ1"
        sdata.targetState = "on"
        sdata.active    = True
        self.scheduler.activateTrigger(sdata)
        jobs = schedule.jobs
        self.assertEqual(1, len(jobs))
        self.assertEqual("23:59:00", str(jobs[0].at_time))
        next = jobs[0].next_run
        self.assertEqual(next.hour, 23)
        self.assertEqual(next.minute, 59)
        self.assertEqual(next.second, 0)
        testdate = date.today()

        pass
    
    def testActivateMondayTrigger(self):
        sdata = SchedulerData()
        sdata.hour      = 23
        sdata.minute    = 59
        sdata.once      = False
        sdata.lightID   = "SZ1"
        sdata.targetState = "on"
        sdata.active    = True
        sdata.dayOfWeek.append("Mo")
        self.scheduler.activateTrigger(sdata)
        jobs = schedule.jobs
        self.assertEqual(1, len(jobs))
        testDays = []
        for job in jobs:
            self.assertEqual("23:59:00", str(job.at_time))
            testDays.append(job.start_day)
        self.assertTrue("monday" in testDays)
        pass
    
    def testActivateTuesdayTrigger(self):
        sdata = SchedulerData()
        sdata.hour      = 23
        sdata.minute    = 59
        sdata.once      = False
        sdata.lightID   = "SZ1"
        sdata.targetState = "on"
        sdata.active    = True
        sdata.dayOfWeek.append("Tu")
        self.scheduler.activateTrigger(sdata)
        jobs = schedule.jobs
        self.assertEqual(1, len(jobs))
        testDays = []
        for job in jobs:
            self.assertEqual("23:59:00", str(job.at_time))
            testDays.append(job.start_day)
        self.assertTrue("tuesday" in testDays)
        pass
    
    def testActivateWednesdayTrigger(self):
        sdata = SchedulerData()
        sdata.hour      = 23
        sdata.minute    = 59
        sdata.once      = False
        sdata.lightID   = "SZ1"
        sdata.targetState = "on"
        sdata.active    = True
        sdata.dayOfWeek.append("We")
        self.scheduler.activateTrigger(sdata)
        jobs = schedule.jobs
        self.assertEqual(1, len(jobs))
        testDays = []
        for job in jobs:
            self.assertEqual("23:59:00", str(job.at_time))
            testDays.append(job.start_day)
        self.assertTrue("wednesday" in testDays)
        pass
    
    def testActivateThursdayTrigger(self):
        sdata = SchedulerData()
        sdata.hour      = 23
        sdata.minute    = 59
        sdata.once      = False
        sdata.lightID   = "SZ1"
        sdata.targetState = "on"
        sdata.active    = True
        sdata.dayOfWeek.append("Th")
        self.scheduler.activateTrigger(sdata)
        jobs = schedule.jobs
        self.assertEqual(1, len(jobs))
        testDays = []
        for job in jobs:
            self.assertEqual("23:59:00", str(job.at_time))
            testDays.append(job.start_day)
        self.assertTrue("thursday" in testDays)
        pass
    
    def testActivateFridayTrigger(self):
        sdata = SchedulerData()
        sdata.hour      = 23
        sdata.minute    = 59
        sdata.once      = False
        sdata.lightID   = "SZ1"
        sdata.targetState = "on"
        sdata.active    = True
        sdata.dayOfWeek.append("Fr")
        self.scheduler.activateTrigger(sdata)
        jobs = schedule.jobs
        self.assertEqual(1, len(jobs))
        testDays = []
        for job in jobs:
            self.assertEqual("23:59:00", str(job.at_time))
            testDays.append(job.start_day)
        self.assertTrue("friday" in testDays)
        pass
    
    def testActivateSaturdayTrigger(self):
        sdata = SchedulerData()
        sdata.hour      = 23
        sdata.minute    = 59
        sdata.once      = False
        sdata.lightID   = "SZ1"
        sdata.targetState = "on"
        sdata.active    = True
        sdata.dayOfWeek.append("Sa")
        self.scheduler.activateTrigger(sdata)
        jobs = schedule.jobs
        self.assertEqual(1, len(jobs))
        testDays = []
        for job in jobs:
            self.assertEqual("23:59:00", str(job.at_time))
            testDays.append(job.start_day)
        self.assertTrue("saturday" in testDays)
        pass
    
    def testActivateSundayTrigger(self):
        sdata = SchedulerData()
        sdata.hour      = 23
        sdata.minute    = 59
        sdata.once      = False
        sdata.lightID   = "SZ1"
        sdata.targetState = "on"
        sdata.active    = True
        sdata.dayOfWeek.append("Su")
        self.scheduler.activateTrigger(sdata)
        jobs = schedule.jobs
        self.assertEqual(1, len(jobs))
        testDays = []
        for job in jobs:
            self.assertEqual("23:59:00", str(job.at_time))
            testDays.append(job.start_day)
        self.assertTrue("sunday" in testDays)
        pass
    
    def testActivateSomeDaysTrigger(self):
        sdata = SchedulerData()
        sdata.hour      = 23
        sdata.minute    = 59
        sdata.once      = False
        sdata.lightID   = "SZ1"
        sdata.targetState = "on"
        sdata.active    = True
        sdata.dayOfWeek.append("Mo")
        sdata.dayOfWeek.append("We")
        sdata.dayOfWeek.append("Fr")
        sdata.dayOfWeek.append("Su")
        self.scheduler.activateTrigger(sdata)
        jobs = schedule.jobs
        self.assertEqual(4, len(jobs))
        testDays = []
        for job in jobs:
            self.assertEqual("23:59:00", str(job.at_time))
            testDays.append(job.start_day)
        self.assertTrue("monday" in testDays)
        self.assertTrue("wednesday" in testDays)
        self.assertTrue("friday" in testDays)
        self.assertTrue("sunday" in testDays)
        pass
    
    def testActivateEveryDayTrigger(self):
        sdata = SchedulerData()
        sdata.hour      = 23
        sdata.minute    = 59
        sdata.once      = False
        sdata.lightID   = "SZ1"
        sdata.targetState = "on"
        sdata.active    = True
        sdata.dayOfWeek.append("Mo")
        sdata.dayOfWeek.append("Tu")
        sdata.dayOfWeek.append("We")
        sdata.dayOfWeek.append("Th")
        sdata.dayOfWeek.append("Fr")
        sdata.dayOfWeek.append("Sa")
        sdata.dayOfWeek.append("Su")
        self.scheduler.activateTrigger(sdata)
        jobs = schedule.jobs
        self.assertEqual(7, len(jobs))
        testDays = []
        for job in jobs:
            self.assertEqual("23:59:00", str(job.at_time))
            testDays.append(job.start_day)
        self.assertTrue("monday" in testDays)
        self.assertTrue("tuesday" in testDays)
        self.assertTrue("wednesday" in testDays)
        self.assertTrue("thursday" in testDays)
        self.assertTrue("friday" in testDays)
        self.assertTrue("saturday" in testDays)
        self.assertTrue("sunday" in testDays)
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()