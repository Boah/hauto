'''
Created on 27.05.2016

@author: mirko
'''
import unittest

from scheduler.schedulerDataContainer import SchedulerData,\
    SchedulerDataContainer

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testSchedulerData(self):
        data = SchedulerData()
        data.hour=9
        data.minute=30
        data.once = False
        data.lightID="SZ1"
        data.targetState = 'on'
        data.sensorQuery="kitchen"
        data.active = True
        self.assertEqual(str(data), "SZ1=on DayOfWeek= Hour=9 Minute=30 Once=True sensor=kitchen active=True")
        
        data.once = False
        data.dayOfWeek.append('Mo')
        data.dayOfWeek.append('Tu')
        data.dayOfWeek.append('We')
        data.dayOfWeek.append('Th')
        data.dayOfWeek.append('Fr')
        data.dayOfWeek.append('Sa')
        data.dayOfWeek.append('Su')
        self.assertEqual(str(data), "SZ1=on DayOfWeek=Mo/Tu/We/Th/Fr/Sa/Su/ Hour=9 Minute=30 Once=False sensor=kitchen active=True")
        
        data.sensorQuery=None
        self.assertEqual(str(data), "SZ1=on DayOfWeek=Mo/Tu/We/Th/Fr/Sa/Su/ Hour=9 Minute=30 Once=False sensor=None active=True")
        
    def testSchedulerDataContainer(self):
        container = SchedulerDataContainer()
        data = SchedulerData()
        data.hour=9
        data.minute=30
        data.once = False
        data.lightID="SZ1"
        data.targetState = 'on'
        data.sensorQuery=None
        data.active = True
        container.schedulerDataList.append(data)
        self.assertEqual(str(container), "SZ1=on DayOfWeek= Hour=9 Minute=30 Once=True sensor=None active=True\n")
        
        data1 = SchedulerData()
        data1.hour=9
        data1.minute=30
        data1.once = False
        data1.lightID="SZ1"
        data1.targetState = 'on'
        data1.sensorQuery='kitchen'
        data1.active = True
        data1.dayOfWeek.append('Mo')
        data1.dayOfWeek.append('Tu')
        data1.dayOfWeek.append('We')
        data1.dayOfWeek.append('Th')
        data1.dayOfWeek.append('Fr')
        data1.dayOfWeek.append('Sa')
        data1.dayOfWeek.append('Su')
        container.schedulerDataList.append(data1)
        
        self.assertEqual(str(container), 
                         "SZ1=on DayOfWeek= Hour=9 Minute=30 Once=True sensor=None active=True\nSZ1=on DayOfWeek=Mo/Tu/We/Th/Fr/Sa/Su/ Hour=9 Minute=30 Once=False sensor=kitchen active=True\n"
                         )
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()