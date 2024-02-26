import pyttsx3

import serial
import pyautogui
import time

# Disable fail-safe feature
pyautogui.FAILSAFE = False

ser = serial.Serial('COM3', 9600)  # Change 'COMx' to the appropriate port

# mouse click
# Text to be converted to speech
text = "Hello, how are you today?"

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 150)  # Speed of speech

# Convert the text to speech and play it
lo = True

while lo:
    data = ser.readline().decode('utf-8').rstrip().split(',')
    click = int(data[6])
    print(click)
    if click > 200:
        engine.say(text)
        engine.runAndWait()
        lo = False

