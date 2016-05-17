'''
Created on 16.05.2016

@author: mirko
'''

from subprocess import call
import logging

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
        try:
            call([self.triggerPath, "10101", str(light), str(cmd)])
        except:
            logging.info("Tried to set light " + str(light) + " to " + str(cmd) + " failed")

if __name__ == '__main__':
    pass