#!/usr/bin/env python3

from mpu6050 import mpu6050
import time
import os
import math

sensor = mpu6050(0x68)

# ---------------- CONFIG ----------------

SHAKE_THRESHOLD = 4.5        # g change
ROTATE_FAST = 180.0          # deg/s
ROTATE_SLOW = 80.0           # deg/s
COOLDOWN = 0.8
LOOP_DELAY = 0.05

# ----------------------------------------

last_action = 0
last_mag = 0

def cooldown_ok():
    global last_action
    if time.time() - last_action > COOLDOWN:
        last_action = time.time()
        return True
    return False

# ---- Music control ----

def cmd(c):
    os.system("mpc " + c)

def volume_up():
    cmd("volume +5")
    print("Volume +")

def volume_down():
    cmd("volume -5")
    print("Volume -")

def next_track():
    cmd("next")
    print("Next")

def prev_track():
    cmd("prev")
    print("Previous")

def toggle():
    cmd("toggle")
    print("Play/Pause")

# ---- Motion processing ----

def accel_magnitude(a):
    return math.sqrt(a['x']**2 + a['y']**2 + a['z']**2)

def max_rotation(g):
    return max(abs(g['x']), abs(g['y']), abs(g['z']))

# ---- Main loop ----

print("Orientation-independent music box running")

while True:
    try:
        accel = sensor.get_accel_data()
        gyro = sensor.get_gyro_data()

        mag = accel_magnitude(accel)
        delta = abs(mag - last_mag)
        last_mag = mag

        rot = max_rotation(gyro)

        if cooldown_ok():

            # Shake → Play / Pause
            if delta > SHAKE_THRESHOLD:
                toggle()

            # Fast rotation → Skip
            elif rot > ROTATE_FAST:
                if gyro['z'] > 0:
                    next_track()
                else:
                    prev_track()

            # Slow rotation → Volume
            elif rot > ROTATE_SLOW:
                if gyro['z'] > 0:
                    volume_up()
                else:
                    volume_down()

        time.sleep(LOOP_DELAY)

    except KeyboardInterrupt:
        print("\nStopped")
        break
