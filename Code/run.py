"""
This program prompts the user to enter number of cycles and frequency.
It then writes data to a microcontroller via serial communication and
plots the data send back to it.

@author: Darya Darvish
"""

import csv
import serial, time
from matplotlib import pyplot

#ser = serial.Serial("/dev/tty.usbmodem1412", 115200, timeout = 1)
ser = serial.Serial("/dev/tty.usbmodem1422", 115200, timeout = 1)
ser.bytesize = serial.EIGHTBITS

while True:
    ser.flushInput()
    ser.flushOutput()
    file_name = input("\nEnter the output file name: ")
    try:
        num_cycles = int(input("Enter the number of cycles (1-10): "))
    except ValueError:
        print("Enter a number");
        continue
    if num_cycles < 1 or num_cycles > 10:
        print("Enter a number between 1 and 10, inclusive")
        continue
    try:
        frequency = float(input("Enter frequency (Hz): "))
    except ValueError:
        print("Enter a number");
        continue
    ser.write(b'\x03')
    ser.write(b'\x04')
    time.sleep(2)
    ser.flushInput()
    ser.flushOutput()
    ser.write((str(num_cycles) + "\r\n").encode())
    time.sleep(1)
    ser.write((str(frequency) + "\r\n").encode())
    x_list = []
    y_list = []
    z_list = []
    temperature_list = []
    gyro_x_list = []
    gyro_y_list = []
    gyro_z_list = []
    time_list = []
    #time_1_list = []
    #v1_list = []
    #v2_list = []
    #v3_list = []
    done = False
    while True:
        if done:
            break
        readline = ser.read_all().decode().splitlines()
        for line in readline:
            if "Done" in line:
                done = True
                break
            data = (str(line)).split()
            if "Data: " in line and len(data) == 9:
                accel_data = (str(line)).split()
                x_list.append(float(accel_data[1]))
                y_list.append(float(accel_data[2]))
                z_list.append(float(accel_data[3]))
                temperature_list.append(float(accel_data[4]))
                gyro_x_list.append(float(accel_data[5]))
                gyro_y_list.append(float(accel_data[6]))
                gyro_z_list.append(float(accel_data[7]))
                time_list.append(float(accel_data[8]))
            if "Scope: " in line and len(data) == 5:
                scope_data = (str(line)).split()
                time_1_list.append(float(scope_data[1]))
                v1_list.append(float(scope_data[2]))
                v2_list.append(float(scope_data[3]))
                v3_list.append(float(scope_data[4]))
            if "Data: " in line and len(data) == 5:
                accel_data = (str(line)).split()
                x_list.append(float(accel_data[1]))
                y_list.append(float(accel_data[2]))
                z_list.append(float(accel_data[3]))
                time_list.append(float(accel_data[4]))
    initial_time = time_list[0]
    time_list = [abs(x - initial_time) for x in time_list]
    pyplot.plot(time_list, x_list, label='x accel (g)')
    pyplot.plot(time_list, y_list, label='y accel (g)')
    pyplot.plot(time_list, z_list, label='z accel (g)')
    pyplot.plot(time_list, temperature_list, label='temperature (C)')
    pyplot.plot(time_list, gyro_x_list, label='x gyro (deg/s)')
    pyplot.plot(time_list, gyro_y_list, label='y gyro (deg/s)')
    pyplot.plot(time_list, gyro_z_list, label='z gyro (deg/s)')
    pyplot.legend(loc="upper right")
    pyplot.xlabel("Time (ms)")
    pyplot.ylabel("Data")
    pyplot.title("Data vs Time")
    pyplot.show()
    pyplot.clf()
    """
    pyplot.plot(time_1_list, v1_list, label='v1')
    pyplot.plot(time_1_list, v2_list, label='v2')
    pyplot.plot(time_1_list, v3_list, label='v3')
    pyplot.legend(loc="upper right")
    pyplot.xlabel("Time (ms)")
    pyplot.ylabel("Voltage (V)")
    pyplot.title("Voltage vs Time")
    pyplot.show()
    pyplot.clf()
    """
    """
    with open(file_name, 'w', newline='') as my_file:
        writer = csv.writer(my_file)
        writer.writerow(["x-accel (g)", "y-accel (g)", "z-accel (g)", "time (ms)"])
        for i in range(0, len(time_list)):
            writer.writerow([x_list[i], y_list[i], z_list[i], time_list[i]]) 
    with open(file_name, 'w', newline='') as my_file:
        writer = csv.writer(my_file)
        writer.writerow(["v1 (V)", "v2 (V)", "v3 (V)", "time (ms)"])
        for i in range(0, len(time_list)):
            writer.writerow([v1_list[i], v2_list[i], v3_list[i], time_1_list[i]])
    """
    ser.flush()
    
ser.close()
