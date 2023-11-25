import pyautogui
import time
from ultralytics import YOLO
import glob
import os

model = YOLO(r"Files/weights/DEPLOY.pt")

def predict(imagepath):
    result = model.predict(imagepath, task='detect', mode='predict', verbose=False, conf=0.25, imgsz=800, save_txt=True)
    champ_list = result[0].names
    unit_ids = result[0].boxes.cls
    return champ_list, unit_ids

def delete_screenshot(filename):
    if os.path.isfile(filename):
        os.remove(filename)
        print(f"Deleted screenshot: {filename}")
    else:
        print(f"File {filename} does not exist.")

def screenshot():
    # Define the starting point coordinates and the size of the screenshot
    start_x = 560
    start_y = 0
    width = 1440
    height = 720

    # Take a screenshot with the specified dimensions
    screenshot = pyautogui.screenshot(region=(start_x, start_y, width, height))

    # Provide a name for the screenshot with the current timestamp

    filename = "screenshot.png"
    # Save the screenshot
    screenshot.save(filename)
    return filename


def print_champions(champ_list, units):
    for i in units:
        if i in champ_list:
            print(f"{i} = {champ_list[i]}")

filename = screenshot()
champ_list, unit_ids = predict(f"{filename}")
print_champions(champ_list, unit_ids)
delete_screenshot(filename)


    
