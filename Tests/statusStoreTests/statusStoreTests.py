'''
Created on 26.05.2016

@author: mirko
'''
import unittest

from lightStatusStore.lightStatusStore import LightStatusStore

class Test(unittest.TestCase):


    def setUp(self):
        statusStore = LightStatusStore()
        statusStore.setStatus("WZ1", 'off')
        statusStore.setStatus("WZ2", 'off')
        statusStore.setStatus("SZ1", 'off')
        pass


    def tearDown(self):
        pass


    def testGetStatusAsString(self):
        statusStore = LightStatusStore()
        
        self.assertEqual(statusStore.getStatusAsString(), 'WZ1=off, WZ2=off, SZ1=off')
        statusStore.setStatus("SZ1", 'on')
        self.assertEqual(statusStore.getStatusAsString(), 'WZ1=off, WZ2=off, SZ1=on')
        statusStore.setStatus("WZ1", 'on')
        self.assertEqual(statusStore.getStatusAsString(), 'WZ1=on, WZ2=off, SZ1=on')
        statusStore.setStatus("WZ2", 'on')
        self.assertEqual(statusStore.getStatusAsString(), 'WZ1=on, WZ2=on, SZ1=on')

    def testGetStatus(self):
        statusStore = LightStatusStore()
        ret = statusStore.getStatus()
        self.assertEqual(ret[0][0], 'WZ1')
        self.assertEqual(ret[0][1], 'off')
        self.assertEqual(ret[1][0], 'WZ2')
        self.assertEqual(ret[1][1], 'off')
        self.assertEqual(ret[2][0], 'SZ1')
        self.assertEqual(ret[2][1], 'off')
        
        statusStore.setStatus("SZ1", 'on')
        ret = statusStore.getStatus()
        self.assertEqual(ret[0][0], 'WZ1')
        self.assertEqual(ret[0][1], 'off')
        self.assertEqual(ret[1][0], 'WZ2')
        self.assertEqual(ret[1][1], 'off')
        self.assertEqual(ret[2][0], 'SZ1')
        self.assertEqual(ret[2][1], 'on')
        
        statusStore.setStatus("WZ2", 'on')
        ret = statusStore.getStatus()
        self.assertEqual(ret[0][0], 'WZ1')
        self.assertEqual(ret[0][1], 'off')
        self.assertEqual(ret[1][0], 'WZ2')
        self.assertEqual(ret[1][1], 'on')
        self.assertEqual(ret[2][0], 'SZ1')
        self.assertEqual(ret[2][1], 'on')
        
        statusStore.setStatus("WZ1", 'on')
        ret = statusStore.getStatus()
        self.assertEqual(ret[0][0], 'WZ1')
        self.assertEqual(ret[0][1], 'on')
        self.assertEqual(ret[1][0], 'WZ2')
        self.assertEqual(ret[1][1], 'on')
        self.assertEqual(ret[2][0], 'SZ1')
        self.assertEqual(ret[2][1], 'on')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()