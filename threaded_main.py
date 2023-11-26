import Files.OCR as OCR 
import Files.image_inference as image_inference
from Files.screen_coords import *
import Files.champs_list as file
import time
import sys
from pynput.keyboard import Listener, KeyCode, Controller, Key
import threading

def main():
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
    time.sleep(2)
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

    ''' THIS IS WHERE YOU TURN ON AND OFF KEYPRESSES'''

    SimulatePressedKeys = False
    try:
        print("Capturing screenshots for board modeling...")
        screenshots = []
        for index in range(8):
            if SimulatePressedKeys: 
                keyboard.press('q')
                keyboard.release('q')
            time.sleep(1)
            screenshot = OCR.capture(())
            screenshots.append(screenshot)
            print(f"Captured screenshot #{index + 1}")
        print("Processing screenshots...")
        champions = image_inference.process_screenshots(screenshots)
        tally = {}

        # Iterate over the list and count each occurrence
        for champion in champions:
            if champion in tally:
                tally[champion] += 1
            else:
                tally[champion] = 1


        champPool = file.champPool
        champion_info = file.champion_info
        print("Done processing screenshots")
        if SimulatePressedKeys:
            keyboard.press('q')
            keyboard.release('q')

        for name, count in tally.items():
            if name in champion_info:
                champ_cost = champion_info[name]["cost"]
                remaining_champs = champPool[f'{champ_cost}_cost'] - count
                print(f"There are {remaining_champs} {name}'s left out of {champPool[f'{champ_cost}_cost']} ({champ_cost} cost)")
            else:
                pass
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

if __name__ == "__main__":
    main()
