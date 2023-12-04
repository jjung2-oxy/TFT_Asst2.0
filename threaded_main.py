import argparse
import Files.OCR as OCR 
import Files.image_inference as image_inference
from Files.screen_coords import *
import Files.champs_list as file
import time
import sys
from pynput.keyboard import Listener, KeyCode, Controller, Key
import threading

overlay_app = None

def set_overlay_app(app):
    global overlay_app
    overlay_app = app

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-skp', '--simulate-keys', action='store_true', 
                        help='Enable simulation of key presses')
    args = parser.parse_args()

    if args.simulate_keys:
        print("Simulating keyboard input...\n\n\n")

    listener_thread = threading.Thread(target=start_listener, daemon=True)
    listener_thread.start()
    listener_thread.join()  

def shopToOCR():
    try:
        print("Capturing screenshot for OCR...")
        screenshot = OCR.capture(())
        print("Processing screenshot...")
        return processOCR(screenshot)
    except Exception as e:
        print(f"Error in shopToOCR: {e}")
        return []

def processOCR(screenshot):
    text_list = []
    time.sleep(1)  
    try:
        for i in range(5):
            bbox = (
                CHAMP_TEXT_LEFT + (i * CHAMP_SPACING), 
                CHAMP_TEXT_TOP, 
                CHAMP_TEXT_RIGHT + (i * CHAMP_SPACING), 
                CHAMP_TEXT_BOTTOM)
            target_string = OCR.ocr(bbox, screenshot)
            closest = file.find_closest(target_string, file.set9_champs)
            text_list.append(closest)
        return text_list
    except Exception as e:
        print(f"Error in processOCR: {e}")
        return []

def boardToModel():
    keyboard = Controller() 
    SimulatePressedKeys = False  # Consider making this a parameter or a configurable setting.

    try:
        print("Capturing screenshots for board modeling...")
        screenshots = []
        for index in range(8):
            if SimulatePressedKeys: 
                keyboard.press('q')
                keyboard.release('q')
            time.sleep(1)  # Consider if this sleep is necessary or if it can be optimized.
            screenshot = OCR.capture(())
            screenshots.append(screenshot)
            print(f"Captured screenshot #{index + 1}")

        print("Processing screenshots...")
        champions = image_inference.process_screenshots(screenshots)
        if not champions:
            print("No champions processed or an error occurred.")
            updateOverlay()
            return

        tally = {champion: champions.count(champion) for champion in set(champions)}
        champPool = file.champPool
        champion_info = file.champion_info
        print("Done processing screenshots")
        getStats(tally, champion_info, champPool)
        updateOverlay()

    except Exception as e:
        print(f"Error in boardToModel: {e}")

def on_press(key):
    try:
        if key == KeyCode.from_char('\\'):
            print("Backslash key pressed!")
            text_list = shopToOCR()
            print(text_list)
        elif key == KeyCode.from_char(']'):
            print("']' key pressed!")
            boardToModel()
        elif key == KeyCode.from_char('['):
            print("Exiting program.")
            sys.exit(0)
    except Exception as e:
        print(f"Error in on_press: {e}")

def start_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()

def getStats(tally, champion_info, champPool):
    for name, count in tally.items():
        if name in champion_info:
            champ_cost = champion_info[name]["cost"]
            remaining_champs = champPool[f'{champ_cost}_cost'] - count
            print(f"There are {remaining_champs} {name}'s left out of {champPool[f'{champ_cost}_cost']} ({champ_cost} cost)")
        else:
            pass  # Consider handling the case where the name is not in champion_info.

def updateOverlay():
    global overlay_app  # Ensure this is the instance of your overlay app
    string_list = ["String 1", "String 2", "String 3"]
    overlay_app.custom_window.update_signal.emit(string_list)