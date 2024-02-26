import serial
import time
import pandas as pd
import keyboard  # Import the keyboard library

# Replace 'COM3' with the correct serial port for your Arduino
ser = serial.Serial('COM3', 9600, timeout=1)

# Create a DataFrame to store the EMG data
columns = ['Timestamp', 'EMG_A0', 'EMG_A1', 'Label']
emg_data = pd.DataFrame(columns=columns)

label = None

def input_label():
    global label
    label = input("Enter label for the current session: ")

try:
    input_label()  # Ask for the label before starting

    while True:
        # Check for key press
        if keyboard.is_pressed(' '):

            # Read EMG sensor values from Arduino
            emg_values = ser.readline().decode('utf-8').strip().split(',')

            # Check if the list is not empty and has at least two elements
            if emg_values and len(emg_values) >= 2:
                # Convert to integers and update the DataFrame
                timestamp = time.time()
                emg_value_a0 = int(emg_values[0])
                emg_value_a1 = int(emg_values[1])

                new_data = pd.DataFrame({
                    'Timestamp': [timestamp],
                    'EMG_A0': [emg_value_a0],
                    'EMG_A1': [emg_value_a1],
                    'Label': [label]
                })

                # Try to read the existing data from the Excel file (if it exists)
                try:
                    existing_data = pd.read_excel('emg_data.xlsx')
                    # Append the new data to the existing data
                    updated_data = pd.concat([existing_data, new_data], ignore_index=True)
                except FileNotFoundError:
                    # If the file doesn't exist, create a new DataFrame with the new data
                    updated_data = new_data

                # Save the updated DataFrame to the Excel file
                updated_data.to_excel('emg_data.xlsx', index=False)
                print("Data recorded and appended to 'emg_data.xlsx'.")

        # Pause to avoid high CPU usage
        time.sleep(0.01)

except KeyboardInterrupt:
    ser.close()  # Close the serial connection on Ctrl+C
    print("Serial connection closed.")

# Ask for a label before saving the data
input_label()
