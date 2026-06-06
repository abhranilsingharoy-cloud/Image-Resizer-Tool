# Image Resizer Tool 🖼️

A fast, lightweight, and robust Python utility designed for batch processing and resizing of images. Built with `Pillow`, this tool automates the tedious task of scaling images to a uniform target resolution while preserving aspect ratios and handling various image formats effortlessly. 

Ideal for web developers preparing thumbnails, data scientists managing image datasets, or anyone needing quick bulk image resizing.

## ✨ Features

- **Batch Processing**: Automatically iterates through all valid images in a designated source folder.
- **Smart Aspect Ratio Maintenance**: Defaults to preserving original image proportions while fitting them within the target boundaries, preventing unwanted distortion.
- **Format Compatibility**: Handles mode conversions (e.g., `RGBA` to `RGB`) seamlessly, preventing errors when saving PNGs or other formats with alpha channels to JPEG.
- **Robust Error Handling**: Skips invalid or corrupt files and gracefully logs errors without halting the entire batch process.
- **Command-Line Interface (CLI)**: Easily configurable via CLI arguments without modifying the source code.

## 🛠️ Requirements

- **Python 3.8+**
- **Pillow >= 10.0.0** (The core library for image manipulation)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/abhranilsingharoy-cloud/Image-Resizer-Tool.git
   cd Image-Resizer-Tool
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### 1. Directory Structure

By default, the script looks for an `input_images` directory. You can use the provided script to generate some test images if needed.

```text
.
├── image_resizer.py
├── generate_test_images.py  <-- Run this to create dummy images for testing
├── requirements.txt
├── input_images/            <-- Place your original images here (JPG, PNG, etc.)
└── resized_images/          <-- The tool will create this and save output here
```

### 2. Running the Tool

You can run the script with its default settings (Input: `input_images`, Output: `resized_images`, Target Size: `800x600`, maintaining aspect ratio):

```bash
python image_resizer.py
```

### 3. Advanced Configuration (CLI Arguments)

The tool supports various arguments for custom workflows:

```bash
python image_resizer.py --source "my_photos" --output "thumbnails" --width 1024 --height 768
```

| Argument | Description | Default |
|----------|-------------|---------|
| `--source` | Source directory containing the original images. | `input_images` |
| `--output` | Target directory to save the resized images. | `resized_images` |
| `--width` | Target maximum width in pixels. | `800` |
| `--height`| Target maximum height in pixels. | `600` |
| `--force` | Force the image to exact width and height (ignores aspect ratio). | `False` |

## 🧪 Testing

To test the script before using it on your own files, generate sample images by running:
```bash
python generate_test_images.py
```
This creates 5 colored test images in the `input_images` folder. You can then run `python image_resizer.py` to see the results in `resized_images`.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.
