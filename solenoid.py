# -*- coding: utf-8 -*-
"""

@author: Darya Darvish
"""

import pyb
import time

class Solenoid:
    ''' This class implements a solenoid driver'''
    
    def __init__ (self, pin_1):
        ''' Controls Solenoid by initializing GPIO
        pins and turning the motor off for safety. '''
        #print('Creating a motor driver')
        self.pin1 = pyb.Pin (pin_1, pyb.Pin.OUT)

    def start(self):
        self.pin1.high()

    def stop(self):
        self.pin1.low()
