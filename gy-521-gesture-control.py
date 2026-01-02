import mpu6050
import time
import spotycon

# Config
ROTATION_THRESHOLD = 50
SHAKE_THRESHOLD = 15.0   # g-force change to detect shake

# Create a new Mpu6050 object
mpu = mpu6050.mpu6050(0x68)

def get_x_angle(accel_data):
    # Calculate the angle of the X axis in degrees
    from math import atan2, degrees, sqrt
    x = accel_data['x']
    y = accel_data['y']
    z = accel_data['z']
    angle = degrees(atan2(x, sqrt(y**2 + z**2)))
    return angle

def get_y_angle(accel_data):
    # Calculate the angle of the X axis in degrees
    from math import atan2, degrees, sqrt
    x = accel_data['x']
    y = accel_data['y']
    z = accel_data['z']
    angle = degrees(atan2(y, sqrt(x**2 + z**2)))
    return angle

def detect_shake(threshold=SHAKE_THRESHOLD, window_time=0.4, sample_rate=0.02):
    # Function to detect shake
    """
    Detects a shake by sampling acceleration magnitude in a rolling window.
    Returns True if a sudden spike is detected in the window.
    threshold: minimum g-force change to consider as shake
    window_time: total time window to sample (seconds)
    sample_rate: time between samples (seconds)
    """
    import math
    import collections
    num_samples = int(window_time / sample_rate)
    magnitudes = collections.deque(maxlen=num_samples)
    for _ in range(num_samples):
        accel = mpu.get_accel_data()
        magnitude = math.sqrt(accel['x']**2 + accel['y']**2 + accel['z']**2)
        magnitudes.append(magnitude)
        time.sleep(sample_rate)
    # Subtract gravity (1g) to focus on dynamic acceleration
    dynamic_mags = [abs(mag - 9.8) for mag in magnitudes]
    print("Dynamic magnitudes:", dynamic_mags)
    # Detect if any value exceeds threshold
    for mag in dynamic_mags:
        if mag > threshold:
            return True
    return False

def main():
    import datetime
    last_x_state = None
    last_y_state = None
    while True:
        accel = mpu.get_accel_data()
        x_angle = get_x_angle(accel)
        y_angle = get_y_angle(accel)    
        shake_detected = detect_shake()

        # Log raw accelerometer data and calculated angle
        print(f"[{datetime.datetime.now()}] Accel: x={accel['x']:.2f}, y={accel['y']:.2f}, z={accel['z']:.2f} | X-Angle: {x_angle:.2f}, Y-Angle: {y_angle:.2f}")

        if shake_detected:
            print(f"[{datetime.datetime.now()}] Shake Detected!!!")
            spotycon.btn_toggleplay()
        elif x_angle >= ROTATION_THRESHOLD and (last_x_state != "back"):
            print(f"[{datetime.datetime.now()}] State change: Moved +{ROTATION_THRESHOLD} degrees (back)")
            last_x_state = "back"
             # Increase volume as long as state is forward
            while True:
                spotycon.btn_volUp()
                time.sleep(0.5)
                accel = mpu.get_accel_data()
                x_angle = get_x_angle(accel)
                if x_angle < ROTATION_THRESHOLD:
                    break
            time.sleep(0.2)
        elif x_angle <= -ROTATION_THRESHOLD and (last_x_state != "forward"):
            print(f"[{datetime.datetime.now()}] State change: Moved -{ROTATION_THRESHOLD} degrees (forward)")
            last_x_state = "forward"
            # Decrease volume as long as state is forward
            while True:
                spotycon.btn_volDown()
                time.sleep(0.5)
                accel = mpu.get_accel_data()
                x_angle = get_x_angle(accel)
                if x_angle > -ROTATION_THRESHOLD:
                    break
            time.sleep(0.2)
        elif -ROTATION_THRESHOLD < x_angle < ROTATION_THRESHOLD and last_x_state is not None:
            print(f"[{datetime.datetime.now()}] State reset: Returned to neutral position")
            last_x_state = None
            time.sleep(0.8)
        elif y_angle >= ROTATION_THRESHOLD and (last_y_state != "left"):
            print(f"[{datetime.datetime.now()}] State change: Moved +{ROTATION_THRESHOLD} degrees (left)")
            last_y_state = "left"
            spotycon.btn_trackprev()
            time.sleep(0.8)
        elif y_angle <= -ROTATION_THRESHOLD and (last_y_state != "right"):
            print(f"[{datetime.datetime.now()}] State change: Moved -{ROTATION_THRESHOLD} degrees (right)")
            last_y_state = "right"
            spotycon.btn_tracknext()
            time.sleep(0.8)
        elif -ROTATION_THRESHOLD < y_angle < ROTATION_THRESHOLD and last_y_state is not None:
            print(f"[{datetime.datetime.now()}] State reset: Returned to neutral position")
            last_y_state = None
            time.sleep(0.8)

        time.sleep(0.1)

if __name__ == "__main__":
    main()
