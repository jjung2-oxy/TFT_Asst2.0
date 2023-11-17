import Files.OCR as OCR 

def main():
    # Define the bounding box (left, top, right, bottom)
    # Capture and OCR
    # Show the annotated image
    bbox = (100, 0, 400, 400) 
    annotated_image = OCR.capture_and_ocr(bbox)
    annotated_image.show()
