import Files.OCR as OCR 
import Files.image_inference as image_inference
from Files.screen_coords import *
import Files.champs_list as file
import Files.interface as interface
import time

global text_list 
text_list = []
def main():
    # take screenshot
    screenshot = OCR.capture(())
    # screenshot type:  <class 'PIL.PngImagePlugin.PngImageFile'>
    shopToOCR(screenshot)
    boardToModel(screenshot)

def boardToModel(screenshot):
     image_inference.main(screenshot)
    
def shopToOCR(screenshot):
    time.sleep(2)
    # Define the bounding box (left, top, right, bottom)
    # Capture and OCR
    # Show the annotated image
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
        text_list.append(closest)
    print(text_list)    

    
def getShop():
        try:
            return text_list
        except:
            return []