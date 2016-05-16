'''
Created on 16.05.2016

@author: mirko
'''

from subprocess import call

class Trigger(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.triggerPath = "/home/mirko/smarthome/raspberry-remote/send"
        
    def trigger(self, light, cmd):
        call([self.triggerPath, str(light)+" "+str(cmd)])
    
    