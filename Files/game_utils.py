"""Some utilities needed for the game and game funcitons to run."""
import cv2
import pytesseract
import random
import os
import re
from PIL import Image
import numpy as np
import screen_coords as sc

if os.getlogin() == 'Jorda':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Jorda\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def get_text_from_image(img):
    """Return the text in the image."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255,
                                 cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    if len(contours) == 0:
        return ""
    im2 = img.copy()
    
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)

    # Drawing a rectangle on copied image
    # rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Cropping the text block for giving input to OCR
    cropped = im2[y:y + h, x:x + w]

    # Apply OCR on the cropped image
    text = pytesseract.image_to_string(cropped)
    text = text[0:-1]
    return pytesseract.image_to_string(cropped,
                                       config='--psm 7 -c '
                                       'tessedit_char_whitelist=""').strip()


def get_num_positions_from_image(img):
    """Return the locations of the bounding boxes around text in the image"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255,
                                 cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    if len(contours) == 0:
        return ""
    im2 = img.copy()
    num_positions = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        # rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)
        text = text[0:-1]
        text = pytesseract.image_to_string(cropped,
                                        config='--psm 7 -c '
                                        'tessedit_char_whitelist=""').strip()
        if re.match(r"^\d{1,2}$"):
            # contour represents a 1 or 2 digit number, so is valid
            num_positions.append((x,y,w,h))
    return num_positions
def save_image(path, img, name=''):
    """Save an image to the desired path  with a random name."""
    
    name += str(random.randint(1, 100000000)) + '.jpg'
    path = os.path.join(path, name)
    cv2.imwrite(path, img)

def find_arrow(img, arrow_img):
    img_resized = img.resize((2560, 1440), Image.ANTIALIAS)

    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    arrow_gray = cv2.cvtColor(arrow_img, cv2.COLOR_BGR2GRAY)

    w, h = arrow_gray.shape[::-1]

    res = cv2.matchTemplate(img_gray, arrow_gray, cv2.TM_CCOEFF_NORMED)

    threshold = 0.8

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        height = max_loc[1] + h/2
        
        player_heights = [sc.FIRST_PLACE_HEIGHT + i*sc.PLAYER_HEIGHT_SPACING for i in range(8)]
        
        closest_index = min(range(8), key=lambda i: abs(player_heights[i] - height))

        return closest_index + 1

    else:
        return 0

