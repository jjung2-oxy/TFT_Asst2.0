
from ultralytics import YOLO


'''
# Save the original stdout so we can restore it later
original_stdout = sys.stdout

# Create a string buffer to capture the output
captured_output = io.StringIO()

# Redirect stdout to the string buffer
sys.stdout = captured_output
'''

model = YOLO("/Users/jordanjung/Desktop/TFTbot2.0/Files/weights/best.pt")
result = model.predict("/Users/jordanjung/Desktop/TFTbot2.0/Files/train_images/blank.jpg", task='detect', mode='predict', verbose=False, conf=0.25, imgsz=800)

unit_ids = result[0].boxes.cls
champ_list = result[0].names

# Here's a Python code snippet that converts the string representation of a PyTorch tensor
# to a list of integers:
integers = unit_ids.int().tolist()

for i in integers:
    if i in champ_list:
        print(f"{i} = {champ_list[i]}")
    

'''
# Reset stdout to its original state
sys.stdout = original_stdout

# Now the output is stored in `captured_output` and you can use it.
output_text = captured_output.getvalue()

# Don't forget to close the StringIO object
captured_output.close()

# Now you can print it or use it as you wish
print("Output:\n", output_text, "\n")
'''

