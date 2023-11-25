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
input_directory = r"C:\Users\Jorda\OneDrive\Desktop\TFTbot2.0\TrainingFiles\labels"
output_path = r"C:\Users\Jorda\OneDrive\Desktop\TFTbot2.0\TrainingFiles\instances_default.json"
image_width = 1440  # Replace with your actual image width
image_height = 720  # Replace with your actual image height

# Categories from your example JSON
category_names = {
    0: 'Ahri', 1: "Akali K/DA", 2: 'Akali True-DMG', 3: 'Amumu', 4: 'Annie', 5: 'Aphelios', 
    6: 'Bard', 7: 'Blitzcrank', 8: 'Caitlyn', 9: 'Cassiopeia', 10: 'Corki', 11: 'Ekko', 
    12: 'Evelynn', 13: 'Ezreal', 14: 'Garen', 15: 'Gnar', 16: 'Gragas', 17: 'Illaoi', 
    18: 'Jax', 19: 'Jhin', 20: 'Jinx', 21: "K'Sante", 22: "Kai'Sa", 23: 'Karthus', 
    24: 'Katarina', 25: 'Kayle', 26: 'Kayn', 27: 'Kennen', 28: 'Lillia', 29: 'Lucian', 
    30: 'Lulu', 31: 'Lux', 32: 'Miss Fortune', 33: 'Mordekaiser', 34: 'Nami', 35: 'Neeko', 
    36: 'Olaf', 37: 'Pantheon', 38: 'Poppy', 39: 'Qiyana', 40: 'Riven', 41: 'Samira', 
    42: 'Senna', 43: 'Seraphine', 44: 'Sett', 45: 'Sona', 46: 'Tahm Kench', 47: 'Taric', 
    48: 'Thresh', 49: 'Training Dummy', 50: 'Twisted Fate', 51: 'Twitch', 52: 'Urgot', 
    53: 'Vex', 54: 'Vi', 55: 'Viego', 56: 'Yasuo', 57: 'Yone', 58: 'Yorick', 59: 'Zac', 
    60: 'Zed', 61: 'Ziggs'
}

categories = [{"id": idx + 1, "name": name, "supercategory": ""} for idx, name in category_names.items()]


yolo_to_coco(input_directory, output_path, image_width, image_height, categories)
