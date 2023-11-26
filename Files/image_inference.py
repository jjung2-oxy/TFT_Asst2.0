from ultralytics import YOLO
import torch
import os
import time
import tempfile

# Initialize the YOLO model
model = YOLO(r"Files/weights/DEPLOY.pt")

def crop_image(img, name):
    """
    Crop the given image and save it to the specified filename.
    """
    start_x = 560
    start_y = 0
    width = 1440
    height = 720
    crop_box = (start_x, start_y, start_x + width, start_y + height)
    cropped_img = img.crop(crop_box)
    cropped_img.save(name)
    return name

def predict(imagepath):
    """
    Run prediction on the image at the given path and return the results.
    """
    try:
        result = model.predict(imagepath, task='detect', mode='predict', verbose=False, conf=0.25, imgsz=800)
        champ_list = result[0].names
        unit_ids = result[0].boxes.cls
        return (champ_list, unit_ids)
    except Exception as e:
        print(f"Error during prediction: {e}")
        return ([], [])

def print_champions(champ_list, unit_ids):
    """
    Print the champions based on the unit IDs.
    """
    temp = []
    if isinstance(unit_ids, torch.Tensor):
        unit_ids = unit_ids.tolist()

    for unit_id in unit_ids:
        if unit_id in champ_list:
            temp.append(champ_list[unit_id])
        return temp

def process_screenshots(screenshots):
    try:
        temp = []
        for index, screenshot in enumerate(screenshots, start=1):
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False, mode='w+b') as tmpfile:
                screenshot.save(tmpfile, format='PNG')
                tmpfile_name = tmpfile.name
            # Ensure that the file is closed before proceeding
            cropped_filename = crop_image(screenshot, tmpfile_name)
            result = predict(cropped_filename)
            temp2 = print_champions(result[0], result[1])
            os.remove(tmpfile_name)
            print(f"Processed screenshot #{index}")
            for x in temp2:
                temp.append(x)
        return temp
    except Exception as e:
        print(f"Error in process_screenshots: {e}")


# Note: Implement the OCR.capture() and other related functions as needed.
