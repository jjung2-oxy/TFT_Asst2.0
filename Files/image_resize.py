from PIL import Image
import PIL

def round_up_to_multiple(value, multiple):
    return ((value + multiple - 1) // multiple) * multiple

def resize_image(input_path, output_path, max_size=800, height_multiple=32):
    with Image.open(input_path) as img:
        # Calculate the target width (fixed at max_size)
        new_width = max_size

        # Calculate the new height based on the aspect ratio, then round it up
        new_height = round_up_to_multiple(int(img.size[1] * (new_width / img.size[0])), height_multiple)

        # Resize the image
        resized_img = img.resize((new_width, new_height), PIL.Image.Resampling.LANCZOS)

        # Save the resized image
        resized_img.save(output_path)


# Example usage
input_image_path = "/Users/jordanjung/Desktop/TFTbot2.0/Files/train_images/blank.jpg"  # Replace with your image path
output_image_path = "/Users/jordanjung/Desktop/TFTbot2.0/Files/train_images/blank_resized.jpg" # Replace with desired output path
resize_image(input_image_path, output_image_path)
