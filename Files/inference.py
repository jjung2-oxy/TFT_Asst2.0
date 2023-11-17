import cv2
import Files.inference as inference
import supervision as sv
import os
from datetime import datetime
from dotenv import load_dotenv

import pyautogui
from pynput import keyboard, mouse

from roboflow import Roboflow

load_dotenv()
rf = Roboflow(api_key=os.environ.get("ROBOFLOW_API_KEY"))
project = rf.workspace().project("firstsecondset")
model = project.version(4).model

# infer on a local image

cursor_position = (0, 0)

# Define the path to the adjacent folder where you want to save the screenshot
adjacent_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots')

# Create the adjacent folder if it doesn't exist
if not os.path.exists(adjacent_folder_path):
    os.makedirs(adjacent_folder_path)

def on_press(key):
    global cursor_position
    try:
        if key.char == 'p':
            
            now = datetime.now()
            timestamp_str = now.strftime("%Y%m%d_%H%M%S")
            screenshot_file_path = os.path.join(adjacent_folder_path, f'screenshot_{timestamp_str}.png')

            width = 1440#2560/2 + 320
            height = 720 #1440 / 2 

            # x, y = cursor_position
            x = 560
            y = 0

            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            screenshot.save(screenshot_file_path)
            print(f'Screenshot saved at {screenshot_file_path}')

            print("running inference...")
            
            print(model.predict(screenshot_file_path, confidence=40, overlap=30).json())

        # If 'Q' is pressed, stop the keyboard and mouse listeners
        elif key.char == 'z':
            keyboard_listener.stop()
            mouse_listener.stop()
            
    except AttributeError:
        pass

# Setup the listener for the keyboard
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

# Setup the listener for the mouse, this is to keep the script running
mouse_listener = mouse.Listener()
mouse_listener.start()

# Wait for the listeners to stop
keyboard_listener.join()
mouse_listener.join()



