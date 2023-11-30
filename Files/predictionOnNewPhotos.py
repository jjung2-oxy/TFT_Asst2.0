import cv2
import os
import numpy as np
from image_inference import predict  # Replace with actual import if necessary

def draw_detections(image, detections, class_names):
    for detection in detections:
        # Extract bounding box coordinates and class index
        x1, y1, x2, y2, conf, cls_conf, cls_id = detection
        label = str(class_names[int(cls_id)])

        # Draw bounding box and label on the image
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(image, label, (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

def process_image(image_path):
    champ_list, unit_ids, boxes = predict(image_path)
    image = cv2.imread(image_path)

    if boxes.numel() == 4:  # Check if boxes tensor has exactly 4 elements
        x1, y1, x2, y2 = boxes
        # Assuming the first class index in unit_ids is the correct one for this box
        cls_id = unit_ids[0] if len(unit_ids) > 0 else -1
        label = champ_list[int(cls_id)] if cls_id in champ_list else "Unknown"

        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(image, label, (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def process_directory(directory):
    """
    Process all images in the given directory.
    """
    for filename in os.listdir(directory)[:1]:
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            process_image(filepath)

# Example usage
process_directory('./screenshots/')