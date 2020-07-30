# -*- coding: utf-8 -*-
"""

@author: Darya Darvish
"""

from machine import I2C
import pyb, utime, time
from ustruct import unpack


sample_rate = const(0x19)
lpf_reg = const(0x1A)
gyro_config = (0x1B)
accel_config = (0x1C)
x_data = const(0x3B)
y_data = const(0x3D)
z_data = const(0x3F)
temp_data = const(0x41)
gyro_x_data = const(0x43)
gyro_y_data = const(0x45)
gyro_z_data = const(0x47)
pwr_manage_1 = const(0x6B)
pwr_manage_2 = const(0x6C)
accel_address = const(0x68)



class Accelerometer:
    ''' This class implements and initializes an accelerometer
        using I2C communication protocol'''
    
    def __init__ (self, pin_1, pin_2):
        self.scl = pyb.Pin(pin_1, mode=pyb.Pin.AF_OD, af=pyb.Pin.AF4_I2C1, pull=pyb.Pin.PULL_UP)
        self.sda = pyb.Pin(pin_2, mode=pyb.Pin.AF_OD, af=pyb.Pin.AF4_I2C1, pull=pyb.Pin.PULL_UP)
        self.i2c = I2C(scl=self.scl, sda=self.sda, freq=400000)
        print(self.i2c.scan())
        self.accel_range = 2
        #set clock source to x axis gyro
        self.i2c.writeto_mem(accel_address, pwr_manage_1, b'\x01')
        #wakeup all sensors
        self.i2c.writeto_mem(accel_address, pwr_manage_2, b'\x00')
        #set sample rate
        self.i2c.writeto_mem(accel_address, sample_rate, b'\x20')
        #set lpf
        self.i2c.writeto_mem(accel_address, lpf_reg, b'\x01')
        #set accel_range
        self.i2c.writeto_mem(accel_address, accel_config, b'\x00')
        #set gyro_range
        self.i2c.writeto_mem(accel_address, gyro_config, b'\x00')
        self.accel_range = 2
        self.gyro_range = 250
        self.data = bytearray(14)
        self.time = utime.ticks_ms()
        self.offset = [0, 0, 0, 0, 0, 0, 0]
        #self.get_offset()

    def get_offset(self):
        ''' This class implements averages accelerometer readings
            at rest in order to compute a mesurement offset'''
        offset_init = []
        for i in range(10):
            offset_init.append(self.read_data())
            utime.sleep_ms(20)
        for i in range(10):
            self.offset[0] += offset_init[i][0]
            self.offset[1] += offset_init[i][1]
            self.offset[2] += offset_init[i][2]
            self.offset[3] += offset_init[i][3]
            self.offset[4] += offset_init[i][4]
            self.offset[5] += offset_init[i][5]
            self.offset[6] += offset_init[i][6]
        self.offset = [x/10 for x in offset]
        

    def read_data(self):
        """this function reads the acceleromter and return x, y, and z data + time
        """
        self.i2c.readfrom_mem_into(accel_address, x_data, self.data)
        data = list(unpack('>hhhhhhh', self.data))
        for i in range (3):
            data[i] = data[i]*(self.accel_range/32767)
        data[3] = 36.53+(data[3]/340)
        for i in range (4,7):
            data[i] = data[i]*(self.gyro_range/32767)
        return data + [utime.ticks_ms()]
    
    def set_range(self, new_range):
        #this function changes the acceleration range, +/- 2g, 4g, 8g, 16g
    
        self.accel_range = new_range
        if new_range == 2:
            self.i2c.writeto_mem(accel_address, accel_format, b'\x00')
            #self.get_offset()
        elif new_range == 4:
            self.i2c.writeto_mem(accel_address, accel_format, b'\x08')
            #self.get_offset()
        elif new_range == 8:
            self.i2c.writeto_mem(accel_address, accel_format, b'\x10')
            #self.get_offset()
        elif new_range == 16:
            self.i2c.writeto_mem(accel_address, accel_format, b'\x18')
            #self.get_offset()
        else:
            print("range can be 2, 4, 8, or 16")

