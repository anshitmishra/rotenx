import pandas as pd
import matplotlib.pyplot as plt

# Read data from Excel file
excel_file = 'emg_data.xlsx'  # Replace with your Excel file name
df = pd.read_excel(excel_file)

# Plotting the graph
plt.figure(figsize=(10, 6))

# Example: Plotting 'EMG_A0' and 'EMG_A1' columns against 'Timestamp'
plt.plot(df['Timestamp'], df['EMG_A0'], label='EMG_A0')
plt.plot(df['Timestamp'], df['EMG_A1'], label='EMG_A1')

plt.title('EMG Data Over Time')
plt.xlabel('Timestamp')
plt.ylabel('EMG Value')
plt.legend()
plt.grid(True)
plt.show()
