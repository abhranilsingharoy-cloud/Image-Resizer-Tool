import os
import argparse
from PIL import Image, UnidentifiedImageError
import sys

def resize_images(source_dir, output_dir, new_size, maintain_aspect_ratio=True):
    """
    Resizes all valid images in the source directory and saves them to the output directory.
    
    Args:
        source_dir (str): Path to the folder containing original images.
        output_dir (str): Path to the folder where resized images will be saved.
        new_size (tuple): Target size as (Width, Height) in pixels.
        maintain_aspect_ratio (bool): If True, maintains aspect ratio using thumbnail().
                                      If False, forces the exact dimensions using resize().
    """
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        sys.exit(1)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: '{output_dir}'")

    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff')
    processed_count = 0
    skipped_count = 0
    error_count = 0

    print(f"Starting batch resize process...")
    print(f"Target size: {new_size}")
    print("-" * 30)

    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)

        # Skip subdirectories and non-files
        if not os.path.isfile(file_path):
            continue

        # Skip files with unsupported extensions based on naive check, but let PIL handle the actual validation
        if not filename.lower().endswith(valid_extensions):
            skipped_count += 1
            print(f"Skipped non-image file: {filename}")
            continue

        try:
            with Image.open(file_path) as img:
                # Handle mode conversion (e.g., RGBA to RGB) to avoid issues saving as JPEG
                if img.mode in ('RGBA', 'P', 'LA'):
                    img = img.convert('RGB')

                # Resize image
                if maintain_aspect_ratio:
                    # thumbnail modifies the image in-place but we need to reassign to keep standard naming conventions
                    img.thumbnail(new_size, Image.Resampling.LANCZOS)
                    resized_img = img
                else:
                    resized_img = img.resize(new_size, Image.Resampling.LANCZOS)

                # Define output path
                # Always save as JPEG to unify the output, or we can keep original extension. Let's keep original extension unless it's a problematic conversion
                # We'll just keep the original extension or save as standard format.
                # Actually, let's just keep the original name to be safe
                output_path = os.path.join(output_dir, filename)

                resized_img.save(output_path, quality=85, optimize=True)
                processed_count += 1
                print(f"Successfully processed: {filename}")

        except UnidentifiedImageError:
            skipped_count += 1
            print(f"Skipped invalid image file: {filename}")
        except Exception as e:
            error_count += 1
            print(f"Error processing {filename}: {e}")

    print("-" * 30)
    print("Batch Processing Complete!")
    print(f"Processed: {processed_count}")
    print(f"Skipped:   {skipped_count}")
    print(f"Errors:    {error_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Image Resizer Tool")
    parser.add_argument("--source", type=str, default="input_images", help="Source directory containing images.")
    parser.add_argument("--output", type=str, default="resized_images", help="Output directory for resized images.")
    parser.add_argument("--width", type=int, default=800, help="Target width in pixels.")
    parser.add_argument("--height", type=int, default=600, help="Target height in pixels.")
    parser.add_argument("--force", action="store_true", help="Force resize to exact dimensions, ignoring aspect ratio.")

    args = parser.parse_args()

    # maintain_aspect_ratio is True by default, unless --force is used
    maintain_aspect_ratio = not args.force

    resize_images(
        source_dir=args.source,
        output_dir=args.output,
        new_size=(args.width, args.height),
        maintain_aspect_ratio=maintain_aspect_ratio
    )
