import serial
import time
import keyboard
from openpyxl import Workbook
from datetime import datetime

def input_label():
    label = input("Enter label for the current session: ")
    return label

# Replace 'COM3' with the correct serial port for your Arduino
arduino_port = 'COM3'
baud_rate = 9600

ser = serial.Serial(arduino_port, baud_rate, timeout=1)

label = input_label()  # Ask for the label before starting

# Create Excel workbook and sheet
workbook = Workbook()
sheet = workbook.active
sheet.append(["Timestamp", "Label", "AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ", "EMG_A0", "EMG_A1"])

excel_file_path = 'emg_mpu_dataC.xlsx'

try:
    while True:
        if keyboard.is_pressed(' '):
            # Read EMG and MPU6050 sensor values from Arduino
            sensor_values = ser.readline().decode('utf-8').strip().split(',')

            # Check if the list is not empty and has at least five elements
            if sensor_values and len(sensor_values) >= 5:
                # Convert to integers
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                data_line = ser.readline().decode().strip().split(',')
                acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, emg_a0, emg_a1 = map(float, data_line)

                print(f"Timestamp: {timestamp}\tLabel: {label}\tAccX: {acc_x}\tAccY: {acc_y}\tAccZ: {acc_z}\tGyroX: {gyro_x}\tGyroY: {gyro_y}\tGyroZ: {gyro_z}\tEMG A0: {emg_a0}\tEMG A1: {emg_a1}")

                sheet.append([timestamp, label, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, emg_a0, emg_a1])
                workbook.save(excel_file_path)
                print("Data recorded and appended to 'emg_mpu_data.xlsx'.")

        # Pause to avoid high CPU usage
        time.sleep(0.01)

except KeyboardInterrupt:
    ser.close()  # Close the serial connection on Ctrl+C
    print("Serial connection closed.")
