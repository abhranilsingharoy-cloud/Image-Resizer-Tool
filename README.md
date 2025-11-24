# Image-Resizer-Tool
This Python script provides a simple, automated solution for batch resizing and processing image files using the Pillow library. It is designed to handle large directories of images quickly and efficiently.
🎯 Goal
To automate the scaling of images to a uniform target resolution (default is 800x600 pixels) for use in web applications, thumbnails, or other standardized formats.
🛠️ Requirements
The project relies solely on the following dependencies:
| Dependency | Purpose |
|---|---|
| Python 3.8+ | Runtime environment. |
| Pillow | Core library for image manipulation (resize, format handling). |
Installation
 * Clone the repository:
   git clone [YOUR_REPOSITORY_URL]
cd batch-image-resizer

 * Install dependencies:
   pip install -r requirements.txt

🚀 Usage
1. Structure the Directories
Ensure you have the following folder structure in the same directory as the script:
.
├── image_resizer.py
├── requirements.txt
├── input_images/  <-- Place your original images here (JPG, PNG, etc.)
└── resized_images/ <-- Output folder (will be created if it doesn't exist)

2. Configure Settings
Open image_resizer.py and modify the if __name__ == "__main__": block to set your desired input/output directories and the new size:
    # --- CONFIGURATION ---
    source_dir = "input_images"
    output_dir = "resized_images"
    
    # Target size: (Width, Height) in pixels
    new_size = (800, 600) 

3. Execute the Script
Run the main script from your terminal:
python image_resizer.py

4. Review Output
The script will print the processing status for each file. Once complete, all resized images will be located in the resized_images folder.
⚙️ Key Features
 * Batch Processing: Iterates through all valid images in the source folder.
 * Format Compatibility: Automatically handles mode conversion (e.g., RGBA to RGB) to ensure proper saving, particularly when converting PNGs to JPGs.
 * Error Handling: Skips non-image files and catches exceptions during individual file processing to ensure the batch run completes.
📝 Customization Notes
If you need to maintain the aspect ratio instead of forcing a specific width/height, replace the line inside image_resizer.py:
# Before (Forces dimensions, potentially distorting the image):
resized_img = img.resize(target_size)

# After (Maintains aspect ratio, using 'target_size' as the max boundaries):
img.thumbnail(target_size)
resized_img = img

