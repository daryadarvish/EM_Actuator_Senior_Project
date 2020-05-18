# -*- coding: utf-8 -*-
"""

@author: Darya Darvish
"""

from machine import I2C
import pyb, utime, time

x_data = const(0x32)
y_data = const(0x34)
z_data = const(0x36)
bw_rate = const(0x2c)
data_format = const(0x31)
power_control = const(0x2d)
accel_address = const(0x53)


class Accelerometer:
    ''' This class implements and initializes an accelerometer
        using I2C communication protocol'''
    
    def __init__ (self, pin_1, pin_2):
        self.scl = pyb.Pin(pin_1, mode=pyb.Pin.AF_OD, af=pyb.Pin.AF4_I2C1, pull=pyb.Pin.PULL_UP)
        self.sda = pyb.Pin(pin_2, mode=pyb.Pin.AF_OD, af=pyb.Pin.AF4_I2C1, pull=pyb.Pin.PULL_UP)
        self.i2c = I2C(scl=self.scl, sda=self.sda, freq=400000)
        self.i2c.writeto_mem(accel_address, power_control, b'\x00')
        self.i2c.writeto_mem(accel_address, power_control, b'\x08')
        self.i2c.writeto_mem(accel_address, data_format, b'\x09')
        self.range = 2
        self.i2c.writeto_mem(accel_address, bw_rate, b'\x00')
        self.i2c.writeto_mem(accel_address, bw_rate, b'\x0a')
        self.data = bytearray(6)
        self.time = utime.ticks_ms()
        self.offset = [0, 0, 0]
        self.get_offset()

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
        for i in range(3):
            value = (self.data[2*i + 1] << 8) | self.data[2*i]
            data_xyz.append(self.get_acceleration(value) - self.offset[i])
        data_xyz.append(utime.ticks_ms() - self.time)
        return data_xyz

    def get_acceleration(self, value):
        """this function return the correct acceleration based on current range
        """
        if self.range == 2:
            temp = (value & 0x3FF)/1.0
            if value & 0x400:
                temp -= 1024
            temp = temp*2/1024
        elif self.range == 4:
            temp = (value & 0x7FF)/1.0
            if value & 0x800:
                temp -= 2048
            temp = temp*4/2048
        elif self.range == 8:
            temp = (value & 0xFFF)/1.0
            if value & 0x1000:
                temp -= 4096
            temp = temp*8/4096
        elif self.range == 16:
            temp = (value & 0x1FFF)/1.0
            if value & 0x2000:
                temp -= 8192
            temp = temp*16/8192
        return temp
    
    def set_range(self, new_range):
        """this function changes the acceleration range, +/- 2g, 4g, 8g, 16g
        """
        self.range = new_range
        if new_range == 2:
            self.i2c.writeto_mem(accel_address, data_format, b'\x00')
            self.get_offset()
        elif new_range == 4:
            self.i2c.writeto_mem(accel_address, data_format, b'\x01')
            self.get_offset()
        elif new_range == 8:
            self.i2c.writeto_mem(accel_address, data_format, b'\x02')
            self.get_offset()
        elif new_range == 16:
            self.i2c.writeto_mem(accel_address, data_format, b'\x03')
            self.get_offset()
        else:
            print("range can be 2, 4, 8, or 16")
