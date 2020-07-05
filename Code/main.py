# -*- coding: utf-8 -*-
"""
This program starts and stops the actuator a given amount of time
and at a certain frequency.  It writes data using serial communication
and is responsible for creating instances of accelerometer and solenoid class.

@author: Darya Darvish
"""

import pyb
import solenoid
import accelerometer_MPU6050
import scope
import time, utime

def print_data(item):
    print("Data: {0:.3f} {1:.3f} {2:.3f} {3:.3f} {4:.3f} {5:.3f} {6:.3f} {7:d}".\
          format(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))
    

if __name__ == "__main__":
    actuator = solenoid.Solenoid(pyb.Pin.board.PA8)
    accel = accelerometer_MPU6050.Accelerometer(pyb.Pin.board.PB8,\
        pyb.Pin.board.PB9)
    tim = pyb.Timer(2)
    oscope = scope.Scope(pyb.Pin.board.PA0, pyb.Pin.board.PC1, pyb.Pin.board.PC0)
    while(True):
        cycles = input()
        frequency = input()
        period = 1000.0/(float(frequency)*2.0)
        #oscope.set_timer(tim)
        for i in range(0, int(cycles)):
            end_time = utime.ticks_ms() + period
            count = 0
            actuator.start()

            while utime.ticks_ms() < end_time:
                if count < 100:
                    print_data(accel.read_data())
                count += 1
            end_time = utime.ticks_ms() + period
            count = 0
            actuator.stop()
            
            while utime.ticks_ms() < end_time:
                if count < 100:
                    print_data(accel.read_data())
                count += 1
        #oscope.resetTimer(tim)
        #oscope.getScope()
        #oscope.resetData()
        print("Done")

