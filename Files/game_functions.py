"""Functions needed for the game to work."""
from window import Window
from game_utils import get_text_from_image, save_image, get_num_positions_from_image, find_arrow_height
import pyautogui
import os
import time
import cv2
# import Utils.grabChampImages as gci
import numpy as np
import screen_coords as sc
import re
from PIL import Image


def trPoint(x: int, y: int, window: Window) -> tuple:
    """Take a point coded for 2560x1440 and returns the transformed value."""
    base_width = 2560
    base_height = 1440

    new_y = y/base_height * window.height + window.y
    new_x = x/base_width * window.width + window.x

    return (int(new_x), int(new_y))


def trX(x: int, window: Window) -> int:
    """Transform an X coordinate to the current window."""
    base_width = 2560
    new_x = x/base_width * window.width + window.x

    return int(new_x)


def trY(y: int, window: Window) -> int:
    """Transform a Y coordinate to the current window."""
    base_height = 1440
    new_y = y/base_height * window.height + window.y
    return int(new_y)


def get_round(window: Window) -> str:
    """Return the current round."""
    
    top = trY(sc.ROUND_NUM_TOP, window)
    bottom = trY(sc.ROUND_NUM_BOT, window)
    left = trX(sc.ROUND_NUM_LEFT, window)
    right = trX(sc.ROUND_NUM_RIGHT, window)
    photo = False
    #Make sure the extra screen shots don't mess up normal tft
    # grab the screen shot
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    # try first location
    cropped_image = image[top:bottom, left:right]
    roundstr = get_text_from_image(cropped_image)
    if photo:
        save_image(os.path.join(os.getcwd(), 'RoundImages'), cropped_image)
    if re.match(r"(\s*[0-9]-[0-9]\s*)", roundstr):
        # print('Current round: ' + roundstr)
        return roundstr
    # try second location
    left = trX(sc.ROUND_NUM_START_LEFT, window)
    right = trX(sc.ROUND_NUM_START_RIGHT, window)
    cropped_image = image[top:bottom, left:right]
    roundstr = get_text_from_image(cropped_image)
    if photo:
        save_image(os.path.join(os.getcwd(), 'RoundImages'), cropped_image)
    if re.match(r"(\s*[0-9]-[0-9]\s*)", roundstr):
        # print('Current round: ' + roundstr)
        return roundstr

    left = trX(sc.ROUND_NUM_HYPERROLL_1_LEFT, window)
    right = trX(sc.ROUND_NUM_HYPERROLL_1_RIGHT, window)
    cropped_image = image[top:bottom, left:right]
    roundstr = get_text_from_image(cropped_image)
    if photo:
        save_image(os.path.join(os.getcwd(), 'RoundImages'), cropped_image)
    if re.match(r"(\s*[0-9]-[0-9]\s*)", roundstr):
        # print('Current round: ' + roundstr)
        return roundstr

    left = trX(sc.ROUND_NUM_HYPERROLL_2_LEFT, window)
    right = trX(sc.ROUND_NUM_HYPERROLL_2_RIGHT, window)
    cropped_image = image[top:bottom, left:right]
    roundstr = get_text_from_image(cropped_image)
    if photo:
        save_image(os.path.join(os.getcwd(), 'RoundImages'), cropped_image)
    if re.match(r"(\s*[0-9]-[0-9]\s*)", roundstr):
        # print('Current round: ' + roundstr)
        return roundstr
    left = trX(sc.ROUND_NUM_HYPERROLL_3_LEFT, window)
    right = trX(sc.ROUND_NUM_HYPERROLL_3_RIGHT, window)
    cropped_image = image[top:bottom, left:right]
    roundstr = get_text_from_image(cropped_image)
    if photo:
        save_image(os.path.join(os.getcwd(), 'RoundImages'), cropped_image)
    if re.match(r"(\s*[0-9]-[0-9]\s*)", roundstr):
        # print('Current round: ' + roundstr)
        return roundstr
    return ""

def get_place(window: Window) -> int:
    
    top = trY(sc.PLAYER_HEALTH_TOP, window)
    left = trX(sc.PLAYER_HEALTH_LEFT, window)
    bottom = trY(sc.PLAYER_HEALTH_BOT, window)
    right = trX(sc.PLAYER_HEALTH_RIGHT, window)

    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    if check_combat_data_mode(window, image):
        return 0

    cropped_image = image[top:bottom, left:right]
    save_image(os.path.join(os.getcwd(), "Images"), cropped_image)
    num_rects = get_num_positions_from_image(cropped_image)
    if len(num_rects) != 7:
        print("Found", num_rects, "player rectangles")
        return 0
    # should return 7 rectangles, need to find the gap
    tops = [rect[1] for rect in num_rects]
    bots = [rect[1] + rect[3] for rect in num_rects]
    
    tops.sort()
    bots.sort()
    differences = [tops[i+1] - tops[i] for i in range(len(tops)-1)]
    average_diff = sum(differences) / len(differences)
    
    deviations = [abs(diff - average_diff) for diff in differences]
    tollerance = 10
    if max(deviations) < tollerance:
        # POV player is in either first or last place as all spacing is approximately equal
        if abs(tops[0] - top) < tollerance:
            # Top player lines up with first place, so POV is in last
            return 8
        if abs(bots[-1] - bottom) < tollerance:
            # Bottom player lines up with last place, so POV is in first
            return 1

    big_diff_idx = deviations.index(max(deviations))
    # POV player is in position 1 greater than gap
    return big_diff_idx + 1

def get_arrow(window: Window) -> int:

    top = trY(sc.ARROW_TOP, window)
    left = trX(sc.ARROW_LEFT, window)
    bottom = trY(sc.ARROW_BOTTOM, window)
    right = trX(sc.ARROW_RIGHT, window)

    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    cropped_image = image[top:bottom, left:right]

    arrow_height = find_arrow_height(cropped_image, os.path.join(os.getcwd(), "Files", "./arrow.png"))
    if arrow_height == 0:
        return 0
    
    player_heights = [trY(sc.FIRST_PLACE_HEIGHT - sc.ARROW_TOP + i*sc.PLAYER_HEIGHT_SPACING, window) for i in range(8)]
        
    closest_index = min(range(8), key=lambda i: abs(player_heights[i] - arrow_height))

    return closest_index

def check_combat_data_mode(window: Window, img) -> bool:
    template = cv2.imread(os.path.join(os.getcwd(), "Files", "Combat_data_button_selected.png"))
    img = cv2.resize(img, (2560, 1440), interpolation=cv2.INTER_AREA)
    
    img = img[sc.COMBAT_DATA_BUTTON_TOP:sc.COMBAT_DATA_BUTTON_BOT,
              sc.COMBAT_DATA_BUTTON_LEFT:sc.COMBAT_DATA_BUTTON_RIGHT]

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)


    res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    threshold = 0.98

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        # save_image(os.path.join(os.getcwd(), "Images"), img_gray, "True")
        print("Currently in data mode")
        return True
    else:
        # save_image(os.path.join(os.getcwd(), "Images"), img_gray, "False")
        print("NOT Currently in data mode")
        return False


def update_tk(tk):
    """Update the tk window once."""
    tk.update()
    tk.update_idletasks()


def update_tkQT_loop(tk, wait_time, dPressed, QT=None):
    """Continuously update the tk window for duration of wait_time."""
    for i in range(wait_time*20):
        # break this loop if the d key is pressed
        tk.update()
        tk.update_idletasks()
        if dPressed:
            if QT:
                QT.update()
            break
        time.sleep(.05)


# def get_curr_champs(window: Window, interpreter, labels):
#     """Return the current champs along with which slot they are in."""
#     # yTop, yBottom, xLeft, xRight, xSpacing
#     yTop = trY(sc.CHAMP_TOP, window)
#     yBottom = trY(sc.CHAMP_BOT, window)
#     xLeft = trX(sc.CHAMP_LEFT, window)
#     xRight = trX(sc.CHAMP_RIGHT, window)
#     xSpacing = trX(sc.CHAMP_SPACING, window)

#     images = gci.screenGrabShop(yTop, yBottom, xLeft, xRight, xSpacing)
#     if not os.path.exists(os.path.join(os.getcwd(), 'UnsortedChampImages')):
#             os.mkdir(os.path.join(os.getcwd(), 'UnsortedChampImages'))
#     # now classify the images using tf model
    
#     curr_champs = []
#     for idx, img in enumerate(images):
#         champ_name = gci.predictImage(img, interpreter, labels)
#         curr_champs.append((champ_name, idx))
#         if champ_name == None:
#             continue
#         champ_path = os.path.join(os.getcwd(), 'UnsortedChampImages')
#         save_image(champ_path, img, champ_name)
#     return curr_champs
