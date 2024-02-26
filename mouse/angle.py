import serial
import time
import math

# Replace 'COMx' with the actual port your Arduino is connected to
ser = serial.Serial('COM3', 9600, timeout=1)

# Constants for integration and complementary filter
ACCEL_SCALE = 16384.0
GYRO_SCALE = 131.0
ALPHA = 0.98
DT = 0.1  # Adjust this value based on your desired sampling rate

def read_data():
    # Read accelerometer and gyroscope data from Arduino over serial
    data = ser.readline().decode('utf-8').strip()
    if data:
        accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = map(float, data.split(','))
        return accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z
    else:
        return None

def complementary_filter(accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, dt, alpha):
    # Calculate tilt angles using accelerometer data
    roll_acc = math.atan2(accel_y, math.sqrt(accel_x**2 + accel_z**2)) * 180 / math.pi
    pitch_acc = math.atan2(-accel_x, math.sqrt(accel_y**2 + accel_z**2)) * 180 / math.pi
    
    # Integrate gyroscope data to get change in angle
    roll_gyro = gyro_x * dt
    pitch_gyro = gyro_y * dt
    
    # Combine accelerometer and gyroscope data using complementary filter
    roll = alpha * (roll_gyro + roll_acc) + (1 - alpha) * roll_acc
    pitch = alpha * (pitch_gyro + pitch_acc) + (1 - alpha) * pitch_acc
    
    return roll, pitch

def integrate_acceleration(accel_x, accel_y, accel_z, dt):
    # Integrate acceleration to get velocity
    vel_x = accel_x * dt
    vel_y = accel_y * dt
    vel_z = accel_z * dt
    
    # Integrate velocity to get position
    pos_x = 0.5 * accel_x * dt**2
    pos_y = 0.5 * accel_y * dt**2
    pos_z = 0.5 * accel_z * dt**2
    
    return pos_x, pos_y, pos_z

def main():
    try:
        while True:
            # Read sensor data from Arduino
            sensor_data = read_data()
            
            if sensor_data:
                accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = sensor_data
                
                # Apply complementary filter to get angles
                roll, pitch = complementary_filter(accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, DT, ALPHA)
                
                # Calculate position change
                pos_x, pos_y, pos_z = integrate_acceleration(accel_x, accel_y, accel_z, DT)
                
                # Print angles and position changes
                print(f"Roll: {roll:.2f} degrees, Pitch: {pitch:.2f} degrees")
                print(f"Change in X: {pos_x:.4f} m, Y: {pos_y:.4f} m, Z: {pos_z:.4f} m")
            
            time.sleep(DT)

    except KeyboardInterrupt:
        pass

    finally:
        ser.close()

if __name__ == "__main__":
    main()
