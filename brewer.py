#!/usr/bin/python3

import argparse
from argparse import RawTextHelpFormatter
import os
import RPi.GPIO as GPIO
import subprocess
import sys
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

parser = argparse.ArgumentParser(
        description="A brewing temperatur controller. \n\
Reads the temperatur from the sensors, turns on/off the heating element to reach the target temperatur.",
        formatter_class=RawTextHelpFormatter)
parser.add_argument("-d", "--duration", help="time to hold the temp in minutes")
parser.add_argument("-t", "--temp", help="target temp")
args = parser.parse_args()

#GPIO PIN of the heating element
GPIO_HEAT = 12
#Temp offset
TEMP_OFFSET = 1.0
temp_sensors = []
temp_sensors.append("/sys/bus/w1/devices/28-02129245142c/w1_slave")
temp_sensors.append("/sys/bus/w1/devices/28-021292453eba/w1_slave")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_HEAT, GPIO.OUT)

#duration in seconds
if args.duration:
    duration = 60 * int(args.duration)
else:
    duration = 60 * 60 * 24

try:
    start_time = time.monotonic()

    while True:
        avg_temp = 0
        i = 0
        print("\r", end='')
        for sensor in temp_sensors:
            sensor_file = open(sensor)
            output = sensor_file.read()
            sensor_file.close()
            secondline = output.split("\n")[1]
            temp = float(secondline.split("t=")[1]) / 1000 + TEMP_OFFSET
            avg_temp = avg_temp + temp
            print("t{0}: {1}\t".format(i, str(temp)), end='')
            i += i + 1
        
        avg_temp = avg_temp / len(temp_sensors)
        print("avg: {0}".format(str(avg_temp)), end='')

        if args.temp:
            print("\t target temp: {0}".format(args.temp), end='')
            if(round(float(args.temp),1) > round(avg_temp,1)):
                GPIO.output(GPIO_HEAT, GPIO.HIGH)
            else:
                GPIO.output(GPIO_HEAT, GPIO.LOW)

        if GPIO.input(GPIO_HEAT):
            print("\t HEATER:" + "\033[1;31;402m" + u"\u25CF" + "\033[0m", end='')
        else:
            print("\t HEATER:" + u"\u25CF", end='')
        print("\t " + str(subprocess.getoutput("date").strip()), end='')

        if args.duration:
            seconds_elapsed = time.monotonic() - start_time
            print("\t ", "Minutes left: ", int(args.duration) - int(seconds_elapsed/60), end='')
            if (time.monotonic() - start_time) > duration:
                print("\nTime is up")
                break
        sys.stdout.flush()

        time.sleep(5)
except KeyboardInterrupt:
    print("\nKeyboard interupt!")
finally:
    GPIO.output(GPIO_HEAT, GPIO.LOW)
