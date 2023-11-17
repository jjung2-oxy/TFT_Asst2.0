import Files.OCR as OCR 
from Files.screen_coords import *
import Files.champs_list as file
import Files.interface as interface
import time

def main():
    time.sleep(10)
    # Define the bounding box (left, top, right, bottom)
    # Capture and OCR
    # Show the annotated image
    screenshot = OCR.capture(())
    text_list = []
    for i in range(5):
        bbox = (
            CHAMP_TEXT_LEFT + (i * CHAMP_SPACING), 
            CHAMP_TEXT_TOP, 
            CHAMP_TEXT_RIGHT + (i * CHAMP_SPACING), 
            CHAMP_TEXT_BOTTOM)
        # Example usage
        string_list = file.set9_champs
        target_string = OCR.ocr(bbox, screenshot)
        closest = file.find_closest(target_string, string_list)
        print(f"The closest string to '{target_string}' is '{closest}'.")
        text_list.append(closest)
        
    print(text_list)
    
    curr_list = interface.get_curr_list()
    for champ in text_list:
        if champ not in curr_list:
            print(f"The champ '{champ}' is not in the desired list.")
        else:
            print(f"The champ '{champ}' is in the desired list.")

    
    



