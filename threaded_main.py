import Files.OCR as OCR 
from Files.screen_coords import *

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
        text_list.append(OCR.ocr(bbox, screenshot))
        
    print(text_list)
