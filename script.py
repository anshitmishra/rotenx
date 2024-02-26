import serial
import time

# Replace 'COM3' with the correct serial port for your Arduino
ser = serial.Serial('COM3', 9600, timeout=1)

try:
    while True:
        # Read analog values from Arduino
        analog_values = ser.readline().decode('utf-8').strip().split(',')

        # Check if the list is not empty and has at least two elements
        if analog_values and len(analog_values) >= 2:
            analog_value_a0 = int(analog_values[0])
            analog_value_a1 = int(analog_values[1])

            print(f"Analog A0: {analog_value_a0}, Analog A1: {analog_value_a1}")

        # Pause to avoid high CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    ser.close()  # Close the serial connection on Ctrl+C
    print("Serial connection closed.")
