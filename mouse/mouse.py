import serial
import pyautogui
import time

# Disable fail-safe feature
pyautogui.FAILSAFE = False

ser = serial.Serial('COM3', 9600)  # Change 'COMx' to the appropriate port

# Define the screen dimensions
screen_width, screen_height = pyautogui.size()

# Initialize previous sensor values
prev_move_x, prev_move_y = 0, 0

# Initialize velocity and decay parameters
velocity_x, velocity_y = 0, 0
decay_factor = 0.8  # Reduced decay factor
smoothing_factor = 0.2  # Smoothing factor for decay

# Adjust these values based on your experimentation
sensitivity = 0.09

full_scale_range_g = 2.0
max_adc_value = 65535

# Calculate max_value based on full-scale range
max_value = full_scale_range_g * max_adc_value / 2.0


# mouse click


while True:
    data = ser.readline().decode('utf-8').rstrip().split(',')
    
    # Process data and perform mouse movements
    try:
        move_x = int(data[0])  # Adjust the index based on your data
        move_y = int(data[1])  # Adjust the index based on your data
        click = int(data[6])
        # doubleclick = int(data[3])

        print(click," ")
        # Get the current mouse position
        current_x, current_y = pyautogui.position()


        # if doubleclick > 150:
        #     pyautogui.click(current_x , current_y )
        #     print("click")

        if click > 40:
        # Check if there is a change in sensor values
            if move_x < screen_width or move_y < screen_height:
                if move_x != prev_move_x or move_y != prev_move_y:
                    # Normalize values to the range [-1, 1]
                    normalized_x = move_x / max_value
                    normalized_y = move_y / max_value

                    # Scale the normalized values
                    move_x = normalized_x * sensitivity * screen_width
                    move_y = normalized_y * sensitivity * screen_height

                    
                    # Update velocity based on the change in position
                    velocity_x = smoothing_factor * velocity_x + (1 - smoothing_factor) * (move_x - prev_move_x)
                    velocity_y = smoothing_factor * velocity_y + (1 - smoothing_factor) * (move_y - prev_move_y)

                    # Move the mouse cursor with smooth acceleration and deceleration
                    pyautogui.moveTo(
                        current_x + move_x, current_y + move_y,
                        duration=0.1, tween=pyautogui.easeInOutQuad
                    )

                    # Update previous sensor values
                    prev_move_x, prev_move_y = move_x, move_y
                else:
                    # Apply decay factor to gradually slow down the cursor
                    velocity_x *= decay_factor
                    velocity_y *= decay_factor

                    # Move the cursor with the decayed velocity
                    pyautogui.move(velocity_x, velocity_y)
                    print(velocity_x, velocity_y)

                    # Introduce a small delay to control the update rate``
            else:
                # pass
                velocity_x = 0
                velocity_y = 0
        else:
            prev_move_x, prev_move_y = 0, 0
    except ValueError:
        print("Invalid data received")
