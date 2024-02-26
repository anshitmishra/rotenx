import serial
import time
import joblib
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

            loaded_model = joblib.load("random_forest_model.joblib")

            # Assuming 'new_data' is your new dataset with columns 'EMG_A0' and 'EMG_A1'
            new_predictions = loaded_model.predict([[analog_value_a0, analog_value_a1]])
            print(f"Analog A0: {analog_value_a0}, Analog A1: {analog_value_a1}")
            print(new_predictions)
        # Pause to avoid high CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    ser.close()  # Close the serial connection on Ctrl+C
    print("Serial connection closed.")
