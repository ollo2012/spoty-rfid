import mpu6050
import time
import spotycon

# Config
ROTATION_THRESHOLD = 50
# current_rotation = None
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

def main():
    import datetime
    last_x_state = None
    last_y_state = None
    while True:
        accel = mpu.get_accel_data()
        x_angle = get_x_angle(accel)
        y_angle = get_y_angle(accel)    

        # Log raw accelerometer data and calculated angle
        print(f"[{datetime.datetime.now()}] Accel: x={accel['x']:.2f}, y={accel['y']:.2f}, z={accel['z']:.2f} | X-Angle: {x_angle:.2f}, Y-Angle: {y_angle:.2f}")

        if x_angle >= ROTATION_THRESHOLD and (last_x_state != "back"):
            print(f"[{datetime.datetime.now()}] State change: Moved +{ROTATION_THRESHOLD} degrees (back)")
            last_x_state = "back"
             # Decrease volume as long as state is forward
            while True:
                spotycon.btn_volDown()
                time.sleep(0.2)
                accel = mpu.get_accel_data()
                x_angle = get_x_angle(accel)
                if x_angle > ROTATION_THRESHOLD:
                    break
            time.sleep(0.2)
        elif x_angle <= -ROTATION_THRESHOLD and (last_x_state != "forward"):
            print(f"[{datetime.datetime.now()}] State change: Moved -{ROTATION_THRESHOLD} degrees (forward)")
            last_x_state = "forward"
            # Increase volume as long as state is forward
            while True:
                spotycon.btn_volUp()
                time.sleep(0.2)
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
