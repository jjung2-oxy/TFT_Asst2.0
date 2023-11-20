import json
import os

def yolo_to_coco(input_directory, output_path, image_width, image_height, categories):
    coco_format = {
        "licenses": [{"name": "", "id": 0, "url": ""}],
        "info": {
            "contributor": "",
            "date_created": "",
            "description": "",
            "url": "",
            "version": "",
            "year": ""
        },
        "categories": categories,
        "images": [],
        "annotations": []
    }

    annotation_id = 1
    image_id = 1

    for filename in os.listdir(input_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_directory, filename)
            coco_image = {
                "id": image_id,
                "width": image_width,
                "height": image_height,
                "file_name": filename.replace('.txt', '.jpg'),  # Adjust based on your image file format
                "license": 0,
                "flickr_url": "",
                "coco_url": "",
                "date_captured": 0
            }
            coco_format["images"].append(coco_image)

            with open(file_path, 'r') as file:
                for line in file:
                    class_id, x_center, y_center, width, height = map(float, line.split())
                    x_min = (x_center - width / 2) * image_width
                    y_min = (y_center - height / 2) * image_height
                    width *= image_width
                    height *= image_height

                    annotation = {
                        "id": annotation_id,
                        "image_id": image_id,
                        "category_id": int(class_id) + 1,  # Adjust if needed
                        "segmentation": [],
                        "area": width * height,
                        "bbox": [x_min, y_min, width, height],
                        "iscrowd": 0,
                        "attributes": {"occluded": False, "rotation": 0.0}
                    }
                    coco_format["annotations"].append(annotation)
                    annotation_id += 1

            image_id += 1

    with open(output_path, 'w') as out_file:
        json.dump(coco_format, out_file, indent=4)

# Example usage
input_directory = '/Users/jordanjung/Desktop/TFTbot2.0/unlabeled_data/YOLO_LABELS/'
output_path = '/Users/jordanjung/Desktop/TFTbot2.0/unlabeled_data/instances_default.json'
image_width = 1440  # Replace with your actual image width
image_height = 720  # Replace with your actual image height

# Categories from your example JSON
categories = [
    {"id": 1, "name": "Cassiopeia", "supercategory": ""}
    # ... (Add all categories as per your example JSON)
]

yolo_to_coco(input_directory, output_path, image_width, image_height, categories)
