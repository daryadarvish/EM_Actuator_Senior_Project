"""
This program prompts the user to enter number of cycles and frequency.
It then writes data to a microcontroller via serial communication and
plots the data send back to it.

@author: Darya Darvish
"""

import csv
import serial, time
from matplotlib import pyplot

ser = serial.Serial("/dev/tty.usbmodem1412", 115200, timeout = 1)
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
    time_list = []
    done = False
    while True:
        if done:
            break
        readline = ser.read_all().decode().splitlines()
        for line in readline:
            if "Done" in line:
                done = True
                break
            accel_data = (str(line)).split()
            if "Data: " in line and len(accel_data) == 5:
                accel_data = (str(line)).split()
                x_list.append(float(accel_data[1]))
                y_list.append(float(accel_data[2]))
                z_list.append(float(accel_data[3]))
                time_list.append(float(accel_data[4]))
    initial_time = time_list[0]
    time_list = [abs(x - initial_time) for x in time_list]
    #print(time_list)
    pyplot.plot(time_list, x_list, label='x axis')
    pyplot.plot(time_list, y_list, label='y axis')
    pyplot.plot(time_list, z_list, label='z axis')
    pyplot.legend(loc="upper right")
    pyplot.xlabel("Time (ms)")
    pyplot.ylabel("Acceleration (g)")
    pyplot.title("Acceleration vs Time")
    pyplot.show()
    pyplot.clf()
    ser.flush()
    with open(file_name, 'w', newline='') as my_file:
        writer = csv.writer(my_file)
        writer.writerow(["x-accel (g)", "y-accel (g)", "z-accel (g)", "time (ms)"])
        for i in range(0, len(time_list)):
            writer.writerow([x_list[i], y_list[i], z_list[i], time_list[i]]) 
ser.close()
