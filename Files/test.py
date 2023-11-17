from PIL import ImageGrab
from roboflow import Roboflow
import os
import pyautogui

from dotenv import load_dotenv

load_dotenv()
rf = Roboflow(api_key=os.environ.get("ROBOFLOW_API_KEY"))
project = rf.workspace().project("firstsecondset")
model = project.version(3).model

xt = 3600/2560 
yt = 2338/1440

def capture_screenshot(filename='temp.png'):
    # Capture the screen
    # bounding_box = {'top': 0, 'left': 560, 'width': 1440, 'height': 720}
    # bounding_box = (0, int(x*560), int(x*1440), int(x*720))       (int(x*560), 0, int(x*1440)+int(x*560), int(x*720))
    # screenshot = ImageGrab.grab((0, 0, 3024, 1964-720))

    x = int(560 * xt)
    y = 0
    width = int(1440 * xt)
    height = int(720 * yt)

    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save("./test.png")
    
    
    # screenshot.resize((800, 400))
    # Save the screenshot
    screenshot.save(filename)
    return filename


def delete_png(filename):
    # Check if the file exists
    if os.path.exists(filename):
        # Delete the file
        os.remove(filename)
        print(f"The file {filename} has been deleted.")
    else:
        print(f"The file {filename} does not exist.")

def inference():
    image_path = capture_screenshot()
    # infer on a local image
    print(model.predict(image_path, confidence=40, overlap=30).json())
    delete_png(image_path)

capture_screenshot()