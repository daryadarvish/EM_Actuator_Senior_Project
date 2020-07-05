#-*- coding: utf-8 -*-
"""
@author: Darya Darvish
"""

import pyb
import time
import micropython

micropython.alloc_emergency_exception_buf(100)

def get_data(oscope):
    oscope.readAll()

class Scope:
    ''' This class implements a solenoid driver'''
    def __init__ (self, pin_gnd=None, pin1=None, pin2=None):
        ''' Reads from analog inputs to '''
        print('Setting up analog inputs for debug')
        self.gnd = pyb.ADC(pin_gnd)
        self.vcc = pyb.ADC(pin1)
        self.vctrl = pyb.ADC(pin2)
        self.time_count = 0
        self.data = []

    def set_timer(self, tim):
        tim.init(freq=75)
        tim.callback(self.interrupt)

    def interrupt(self, tim):
        """ Interrupt subroutine that reads data from the oscilloscope
        """
        #print("\n")
        #self.readAll()
        micropython.schedule(get_data, self)
    
    def resetData(self):
        self.data = []

    def resetTimer(self, tim):
        self.time_count = 0
        tim.deinit()
    
    def readVoltage(self, pin):
        return (3/4095)*(pin.read())

    def readAll(self):
        self.data.append("Scope: {0:d} {1:.3f} {2:.3f} {3:.3f}".format(self.time_count, self.readVoltage(self.gnd),
            self.readVoltage(self.vcc), self.readVoltage(self.vctrl)))
        #    self.readVoltage(self.vcc), self.readVoltage(self.vctrl))
        #print("Scope: {0:d} {1:.3f} {2:.3f} {3:.3f}".format(self.time_count, self.readVoltage(self.gnd),
        #    self.readVoltage(self.vcc), self.readVoltage(self.vctrl)))
        self.time_count += 1

    def getScope(self):
        for item in self.data:
            print(item)
