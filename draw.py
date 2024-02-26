import matplotlib.pyplot as plt

def plot_sensor_locations():
    fig, ax = plt.subplots()

    # Define sensor locations for each finger
    fingers = {
        'Thumb': (0, 0),
        'Index Finger': (0, 1),
        'Middle Finger': (0, 2),
        'Ring Finger': (0, 3),
        'Little Finger (Pinky)': (0, 4)
    }

    # Plotting sensors
    for finger, location in fingers.items():
        ax.plot(location[0], location[1], marker='o', markersize=8, label=finger)

    # Adding labels and grid
    ax.set_title('EMG Sensor Locations for Finger Tracking')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.grid(True)

    # Display legend
    ax.legend()

    # Show the plot
    plt.show()

# Call the function to plot sensor locations
plot_sensor_locations()
