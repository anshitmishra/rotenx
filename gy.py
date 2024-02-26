from mpu6050 import mpu6050
import time
import math

# MPU6050 object
mpu = mpu6050(0x68)  # Use 0x69 if your MPU6050 has that address

# Constants for gesture recognition
SHAKE_THRESHOLD = 1.5  # Adjust as needed
SHAKE_DURATION = 0.5  # Adjust as needed
SAMPLE_RATE = 0.01  # Adjust as needed

def get_acceleration():
    accel_data = mpu.get_accel_data()
    return accel_data['x'], accel_data['y'], accel_data['z']

def calculate_magnitude(accel_x, accel_y, accel_z):
    return math.sqrt(accel_x**2 + accel_y**2 + accel_z**2)

def detect_shake(magnitude):
    return magnitude > SHAKE_THRESHOLD

def main():
    start_time = time.time()

    while True:
        accel_x, accel_y, accel_z = get_acceleration()
        magnitude = calculate_magnitude(accel_x, accel_y, accel_z)

        if detect_shake(magnitude):
            print("Shake detected!")

            # Add your gesture handling code here

            # Wait for a short duration to avoid multiple detections
            time.sleep(SHAKE_DURATION)

        time.sleep(SAMPLE_RATE)

if __name__ == "__main__":
    main()
