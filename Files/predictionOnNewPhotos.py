import os
from image_inference import predict  # Replace with the correct import based on your project structure

def process_directory(directory):
    # Iterate over all files in the given directory
    for filename in os.listdir(directory):
        # Construct the full file path
        filepath = os.path.join(directory, filename)

        # Check if it's a file (and not a directory)
        if os.path.isfile(filepath):
            # Run the prediction function on the image
            # Adjust the call according to how your predict function is defined
            result = predict(filepath)
            print(f"Results for {filename}: {result[1]}")

def main():
    screenshots_directory = "./screenshots/"  # Replace with the correct path
    process_directory(screenshots_directory)

if __name__ == "__main__":
    main()
