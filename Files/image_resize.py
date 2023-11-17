from PIL import Image

def resize_image(input_path, output_path, max_size=800):
    with Image.open(input_path) as img:
        # Calculate the target size maintaining the aspect ratio
        ratio = min(max_size / img.size[0], max_size / img.size[1])
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))

        # Resize the image
        resized_img = img.resize(new_size, Image.ANTIALIAS)

        # Save the resized image
        resized_img.save(output_path)

# Example usage
input_image_path = 'path/to/your/image.jpg'  # Replace with your image path
output_image_path = 'path/to/your/resized_image.jpg'  # Replace with desired output path
resize_image(input_image_path, output_image_path)
