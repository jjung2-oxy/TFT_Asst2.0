import Files.OCR as OCR 
from Files.screen_coords import *
import Files.champs_list as file

def main():
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




