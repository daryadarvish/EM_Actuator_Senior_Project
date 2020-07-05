# -*- coding: utf-8 -*-
"""

@author: Darya Darvish
"""

from machine import I2C
import pyb, utime, time

reg_me = const(0x0F)
x_data = const(0x28)
y_data = const(0x2A)
z_data = const(0x2C)
REG_CTRL0 = const(0x1E)
REG_CTRL1 = const(0x20)
REG_CTRL2 = const(0x21)
REG_CTRL4 = const(0x23)
REG_CTRL5 = const(0x24)
accel_address = const(0x18)


class Accelerometer:
    ''' This class implements and initializes an accelerometer
        using I2C communication protocol'''
    
    def __init__ (self, pin_1, pin_2):
        #self.scl = pyb.Pin(pin_1, mode=pyb.Pin.AF_OD, af=pyb.Pin.AF4_I2C1)
        #self.sda = pyb.Pin(pin_2, mode=pyb.Pin.AF_OD, af=pyb.Pin.AF4_I2C1)
        self.scl = pyb.Pin(pin_1, mode=pyb.Pin.AF_OD, af=pyb.Pin.AF4_I2C1, pull=pyb.Pin.PULL_UP)
        self.sda = pyb.Pin(pin_2, mode=pyb.Pin.AF_OD, af=pyb.Pin.AF4_I2C1, pull=pyb.Pin.PULL_UP)
        self.i2c = I2C(scl=self.scl, sda=self.sda, freq=400000)
        print(self.scl.af_list())
        print(self.sda.af_list())
        print(self.i2c.scan())
        self.i2c.writeto_mem(accel_address, REG_CTRL0, b'\x90')
        self.i2c.writeto_mem(accel_address, REG_CTRL2, b'\x80')
        x = self.i2c.readfrom_mem(accel_address, REG_CTRL2, 1)
        print(x)
        print(x == b'\x80')
        #set data rate and axis enables 
        self.i2c.writeto_mem(accel_address, REG_CTRL1, b'\x77')
        #self.i2c.writeto_mem(accel_address, _REG_CTRL4, b'\x08')
        device_id = self.i2c.readfrom_mem(accel_address, reg_me, 2)
        print(device_id)
        if device_id != b'33':
            print('Failed to find LIS3DH!')
        
        self.range = 2
        self.time = utime.ticks_ms()
        self.offset = [0, 0, 0]
        self.set_range(self.range)
        self.data = bytearray(6)
        

    def get_offset(self):
        ''' This class implements averages accelerometer readings
            at rest in order to compute a mesurement offset'''
        offset = [0, 0, 0]
        offset_init = []
        for i in range(10):
            offset_init.append(self.read_data())
            utime.sleep_ms(20)
        for i in range(10):
            offset[0] += offset_init[i][0]
            offset[1] += offset_init[i][1]
            offset[2] += offset_init[i][2]
        self.offset = [x/10 for x in offset]
        

    def read_data(self):
        """this function reads the acceleromter and return x, y, and z data + time
        """
        self.data = self.i2c.readfrom_mem(accel_address, x_data, 6)
        data_xyz = []
        print(self.data)
        for i in range(3):
            value = ((self.data[2*i + 1] << 8) | self.data[2*i])
            data_xyz.append(self.twos_comp(value) - self.offset[i])
        data_xyz.append(utime.ticks_ms() - self.time)
        return data_xyz

    def twos_comp(self, x):
        """this function return the correct acceleration based on current range
        """
        if (0x8000 & x): 
            x = - (0x010000 - x)
        return x*(self.range/32767)
    
    def set_range(self, new_range):
        """this function changes the acceleration range, +/- 2g, 4g, 8g, 16g
        """
        self.range = new_range
        if new_range == 2:
            self.i2c.writeto_mem(accel_address, REG_CTRL4, b'\x00')
            #self.get_offset()
        elif new_range == 4:
            self.i2c.writeto_mem(accel_address, REG_CTRL4, b'\x10')
            #self.get_offset()
        elif new_range == 8:
            self.i2c.writeto_mem(accel_address, REG_CTRL4, b'\x20')
            #self.get_offset()
        elif new_range == 16:
            self.i2c.writeto_mem(accel_address, REG_CTRL4, b'\x30')
            #self.get_offset()
        else:
            print("range can be 2, 4, 8, or 16")
