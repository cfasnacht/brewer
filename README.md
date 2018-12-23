# Brewer
A brewing temperatur controller:  
Reads the temperatur from the sensors, turns on/off the heating element to reach the target temperatur

Based on this links I built a simple brewing machine:

https://opensource.com/article/17/7/brewing-beer-python-and-raspberry-pi

http://web.craftbeerpi.com/hardware/

Because I found craftbeerpi to complex for my prototype I wrote a python script to control the temperatures.

## Example usage

```
# will hold the temperatur of 67 °C for 10 mintes
./brewer.py -t 67 -d 10
```

## Configuration
```
#GPIO PIN of the heating element:
GPIO_HEAT = 12
#Temperatur offset:
TEMP_OFFSET = 1.0
#add adtional temp sensor:
temp_sensors.append("/sys/bus/w1/devices/xxxxxx/w1_slave")
```
