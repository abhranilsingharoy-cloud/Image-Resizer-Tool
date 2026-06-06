# Image Resizer Tool 🖼️
**Developed by Abhranil Singha Roy**

An advanced, high-performance Python utility designed for professional batch processing and resizing of images. Built with `Pillow` and `concurrent.futures`, this tool automates large-scale image scaling operations using multi-core processing, making it incredibly fast and efficient.

Ideal for web developers preparing thumbnails, data scientists managing massive image datasets, or anyone needing quick, reliable bulk image processing.

## ✨ Advanced Features

- **Blazing Fast Multiprocessing**: Utilizes all available CPU cores (`ProcessPoolExecutor`) to process images concurrently, drastically reducing processing time for large batches.
- **Progress Tracking**: Features a beautiful, real-time progress bar powered by `tqdm`.
- **Smart Aspect Ratio & EXIF Handling**: Automatically reads EXIF data to correct image orientation before resizing. Preserves original proportions by default.
- **Format Conversion**: Convert your entire batch to modern formats like `WEBP`, `JPEG`, or `PNG` on the fly.
- **Comprehensive Logging**: Generates a detailed `resizer.log` file, recording successes, warnings, and skipped files without cluttering your terminal.
- **Robust Error Recovery**: Skips corrupt files and incompatible formats cleanly. Automatically handles RGBA to RGB color space conversions.
- **CLI Configuration**: Fully controllable via command-line arguments.

## 🛠️ Requirements

- **Python 3.8+**
- **Pillow >= 10.0.0** (Core image manipulation)
- **tqdm >= 4.66.0** (Progress bar)

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
├── input_images/            <-- Place your original images here
└── resized_images/          <-- The tool will save output here
```

### 2. Basic Run

Run the script with default settings (Input: `input_images`, Output: `resized_images`, Size: `800x600`, maintaining aspect ratio):

```bash
python image_resizer.py
```

### 3. Advanced Configuration (CLI Arguments)

The tool acts as a powerful CLI. You can specify exact constraints, change output formats, and control image quality.

```bash
python image_resizer.py --source "raw_photos" --output "web_thumbnails" --width 1024 --height 768 --format webp --quality 80
```

| Argument | Description | Default |
|----------|-------------|---------|
| `--source` | Source directory containing the original images. | `input_images` |
| `--output` | Target directory to save the resized images. | `resized_images` |
| `--width` | Target maximum width in pixels. | `800` |
| `--height`| Target maximum height in pixels. | `600` |
| `--force` | Force the image to exact dimensions (ignores aspect ratio). | `False` |
| `--format`| Convert all output images to a specific format (`jpg`, `png`, `webp`).| Original format |
| `--quality`| Set output compression quality for JPEG/WEBP (1-100). | `85` |
| `--workers`| Number of concurrent CPU processes to use. | Optimal CPU Count |

## 🧪 Testing

To test the script's multiprocessing and progress bar:
```bash
python generate_test_images.py
python image_resizer.py --format webp
```
Check `resizer.log` for execution details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.
