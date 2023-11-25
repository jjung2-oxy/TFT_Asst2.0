from ultralytics import YOLO
import OCR as OCR 
import os
import time
import tempfile


model = YOLO(r"Files/weights/DEPLOY.pt")

def crop_image(img, name):
    start_x = 560
    start_y = 0
    width = 1440
    height = 720
    crop_box = (start_x, start_y, start_x + width, start_y + height)
    cropped_img = img.crop(crop_box)
    cropped_img.save(name)
    return name

def predict(imagepath):
    try:
        result = model.predict(imagepath, task='detect', mode='predict', verbose=False, conf=0.25, imgsz=800)
        champ_list = result[0].names
        unit_ids = result[0].boxes.cls
        return (champ_list, unit_ids)
    except Exception as e:
        print(f"Error during prediction: {e}")
        return ([], [])

def delete_screenshot(filename):
    try:
        if os.path.isfile(filename):
            os.remove(filename)
            print(f"Deleted screenshot: {filename}")
        else:
            print(f"File {filename} does not exist.")
    except Exception as e:
        print(f"Error deleting file: {e}")

def print_champions(champ_list, unit_ids):
    for unit_id in unit_ids:
        if unit_id in champ_list:
            print(f"{unit_id} = {champ_list[unit_id]}")

def main(screenshot):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        cropped_filename = crop_image(screenshot, tmpfile.name)
        result = predict(cropped_filename)
        print_champions(result[0], result[1])
        # delete_screenshot(cropped_filename)

screenshot = OCR.capture(())
main(screenshot)