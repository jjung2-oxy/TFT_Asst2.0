
from ultralytics import YOLO
import glob
import os

model = YOLO(r"C:\Users\Jorda\OneDrive\Desktop\TFTbot2.0\TrainingFiles\cassbboxV2.pt")

def predict(imagepath):
    result = model.predict(imagepath, task='detect', mode='predict', verbose=False, conf=0.25, imgsz=800, save_txt=True)

def print_champions(integers, champ_list):
    for i in integers:
        if i in champ_list:
            print(f"{i} = {champ_list[i]}")

def predict_on_all_images(model, directory):
    """
    Predict on all images in the specified directory using the given model.
    """
    predictions = {}

    for filename in os.listdir(directory):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Add or remove file extensions as needed
            image_path = os.path.join(directory, filename)
            predict(image_path)

# Directory of the script file
script_directory = os.path.dirname(os.path.realpath(__file__))

# Predict on all images
predictions = predict_on_all_images(model, script_directory)