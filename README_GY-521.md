### Soldering/Wiring Diagram

Below is a wiring diagram for connecting the GY-521 (MPU6050) to the Raspberry Pi:

![GY-521 to Raspberry Pi Wiring](https://hackster.imgix.net/uploads/attachments/1645602/rpi-with-mpu_480x480.png?auto=compress%2Cformat&w=740&h=555&fit=max)

Ensure all connections are secure and the module is properly soldered if required.
## GY-521 (MPU6050) Setup Guide for Raspberry Pi

This guide will help you set up the GY-521 (MPU6050) accelerometer and gyroscope sensor with your Raspberry Pi and start reading sensor data using Python.

### 1. Enable I2C on the Raspberry Pi

1. Open a terminal and run:
	```
	sudo raspi-config
	```
2. Go to **Interfacing Options** > **I2C** and enable it.
3. Reboot the Raspberry Pi when prompted, or run:
	```
	sudo reboot
	```

### 2. Connect the GY-521 Module

Wire the GY-521 to the Raspberry Pi GPIO pins as follows:

| GY-521 Pin | Raspberry Pi Pin |
|------------|-----------------|
| VCC        | 3.3V (Pin 1)    |
| GND        | GND (Pin 6)     |
| SDA        | SDA1 (Pin 3)    |
| SCL        | SCL1 (Pin 5)    |

Ensure the module is pre-soldered if required.

### 3. Install Required Libraries

Run the following commands to install the necessary packages:
```
sudo apt install python3-smbus
pip install mpu6050-raspberrypi
```

### 4. Test the Sensor

You can use a sample script to read data from the sensor. Example code can be found here: https://github.com/shillehbean/youtube-p2/blob/main/mpu6050_test.py

---
For more details, see the [Instructables tutorial](https://www.instructables.com/How-to-Use-the-MPU6050-With-the-Raspberry-Pi-4/).
