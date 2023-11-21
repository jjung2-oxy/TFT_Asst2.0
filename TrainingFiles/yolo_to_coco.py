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
input_directory = r"/Users/jordanjung/Desktop/TFTbot2.0/runs/detect/predict/labels/"
output_path = r"/Users/jordanjung/Desktop/TFTbot2.0/TrainingFiles/instances_default.json"
image_width = 1440  # Replace with your actual image width
image_height = 720  # Replace with your actual image height

# Categories from your example JSON
category_names = {
    0: 'Ahri', 1: 'Akali K-DA', 2: 'Akali True-DMG', 3: 'Amumu', 4: 'Annie', 5: 'Aphelios', 6: 'Bard', 
    7: 'Blitzcrank', 8: 'Caitlyn', 9: 'Cassiopeia', 10: 'Corki', 11: 'Ekko', 12: 'Evelynn', 13: 'Ezreal', 
    14: 'Garen', 15: 'Gnar', 16: 'Gragas', 17: 'Illaoi', 18: 'Jax', 19: 'Jhin', 20: 'Jinx', 21: "K'Sante", 
    22: "Kai'Sa", 23: 'Katarina', 24: 'Kayle', 25: 'Kayn', 26: 'Kennen', 27: 'Lillia', 28: 'Lucian', 
    29: 'Lulu', 30: 'Lux', 31: 'Miss Fortune', 32: 'Mordekaiser', 33: 'Nami', 34: 'Neeko', 35: 'Olaf', 
    36: 'Pantheon', 37: 'Poppy', 38: 'Qiyana', 39: 'Riven', 40: 'Samira', 41: 'Senna', 42: 'Seraphine', 
    43: 'Sett', 44: 'Sona', 45: 'Tahm Kench', 46: 'Taric', 47: 'Thresh', 48: 'Twisted Fate', 49: 'Twitch', 
    50: 'Urgot', 51: 'Vex', 52: 'Vi', 53: 'Viego', 54: 'Yasuo', 55: 'Yone', 56: 'Yorick', 57: 'Zac', 
    58: 'Zed', 59: 'Ziggs'
}

categories = [{"id": idx + 1, "name": name, "supercategory": ""} for idx, name in category_names.items()]

yolo_to_coco(input_directory, output_path, image_width, image_height, categories)
