# -*- coding: utf-8 -*-
"""
This program starts and stops the actuator a given amount of time
and at a certain frequency.  It writes data using serial communication
and is responsible for creating instances of accelerometer and solenoid class.

@author: Darya Darvish
"""

import pyb
import solenoid
import accelerometer
import time, utime

if __name__ == "__main__":
    actuator = solenoid.Solenoid(pyb.Pin.board.PA8)
    accel = accelerometer.Accelerometer(pyb.Pin.board.PB8,\
        pyb.Pin.board.PB9)

    while(True):
        cycles = input()
        frequency = input()
        period = 1000.0/(float(frequency)*2.0)
        
        for i in range(0, int(cycles)):
            end_time = utime.ticks_ms() + period
            count = 0
            actuator.start()
            
            while utime.ticks_ms() < end_time:
                if count < 100:
                    item = accel.read_data()
                    print("Data: {0:.3f} {1:.3f} {2:.3f} {3:d}".format(item[0], item[1], item[2], item[3]))
                count += 1
                
            end_time = utime.ticks_ms() + period
            count = 0
            actuator.stop()
            
            while utime.ticks_ms() < end_time:
                if count < 100:
                    item = accel.read_data()
                    print("Data: {0:.3f} {1:.3f} {2:.3f} {3:d}".format(item[0], item[1], item[2], item[3]))
                count += 1

        print("Done")
