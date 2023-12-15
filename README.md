# Team Fight Tactics Assistant Tool

## Overview
The Team Fight Tactics Assistant Tool is an innovative application designed to enhance gameplay strategy in the popular strategy game, Team Fight Tactics (TFT). Utilizing advanced computer vision and machine learning techniques, this tool provides real-time insights into the game's unit pool, helping players make informed strategic decisions.

## Features
- Real-time object detection using YOLO (You Only Look Once) v8 model.
- Text recognition in the game interface using Tesseract OCR.
- User-friendly interface for easy interaction and customization.
- Dynamic PyQt5 overlay for displaying insights directly on the game screen.
- Asynchronous programming for efficient multi-threaded operation.

## Installation

### Prerequisites
- Python 3.x
- Pip package manager

### Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/jjung2-oxy/TFTbot2.0

2. **Navigate to the Project Directory:**
   ```bash
   cd TFTbot2.0

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

### Usage

- **Disclaimer**
  The Team Fight Tactics Window must be set to "Borderless Fullscreen".
  If set to "Fullscreen" the overlay will not be visible.

- **Run the main script to start the tool:**
  ```bash
  python main.py
  
Adjust preferences using the user interface that appears on screen.

### Feature Keybinds:
- Press "\\" to activate the Real-time object detection functionality and display current game statistics.
- Press "d" (also purposefully bound to the in-game shop refresh keybind) to activate the OCR functionality, which causes the overlay to highlight any desired units in red.
