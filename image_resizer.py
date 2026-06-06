import os
import argparse
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image, ImageOps, UnidentifiedImageError
from tqdm import tqdm
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("resizer.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
# Disable PIL debug logging
logging.getLogger("PIL").setLevel(logging.WARNING)

# Remove the stream handler for the main script so it doesn't clutter the tqdm progress bar, 
# keep only FileHandler for worker processes, except for the main summary.
# Actually, tqdm and logging to stdout conflict slightly. Let's just log to a file and only print warnings/errors to stdout, or use tqdm.write.
# To keep it simple, we'll log everything to resizer.log, and use tqdm for console progress.

def process_single_image(args):
    """
    Worker function to process a single image.
    args is a tuple: (file_path, output_dir, filename, new_size, maintain_aspect_ratio, output_format, quality)
    Returns: (status, filename, message)
    """
    file_path, output_dir, filename, new_size, maintain_aspect_ratio, output_format, quality = args
    
    try:
        with Image.open(file_path) as img:
            # Correct orientation based on EXIF data
            img = ImageOps.exif_transpose(img)

            # Handle mode conversion (e.g., RGBA to RGB) to avoid issues saving as JPEG
            if img.mode in ('RGBA', 'P', 'LA'):
                # If target is PNG or WEBP, we might want to keep RGBA.
                # But for safety, if we're converting to JPEG, we MUST convert.
                if output_format and output_format.lower() in ('jpg', 'jpeg'):
                    img = img.convert('RGB')
                elif img.mode == 'P':
                    # Convert palette images
                    img = img.convert('RGBA' if 'transparency' in img.info else 'RGB')

            # Resize image
            if maintain_aspect_ratio:
                img.thumbnail(new_size, Image.Resampling.LANCZOS)
                resized_img = img
            else:
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Determine output filename and extension
            name, ext = os.path.splitext(filename)
            if output_format:
                ext = f".{output_format.lower()}"
                
            out_filename = f"{name}{ext}"
            output_path = os.path.join(output_dir, out_filename)

            # Determine save parameters
            save_kwargs = {}
            if ext.lower() in ('.jpg', '.jpeg'):
                save_kwargs = {'quality': quality, 'optimize': True}
            elif ext.lower() == '.webp':
                save_kwargs = {'quality': quality, 'method': 6}
            elif ext.lower() == '.png':
                save_kwargs = {'optimize': True}

            resized_img.save(output_path, **save_kwargs)
            return ('success', filename, "Processed successfully")

    except UnidentifiedImageError:
        return ('skipped', filename, "Invalid image format")
    except Exception as e:
        return ('error', filename, str(e))

def resize_images(source_dir, output_dir, new_size, maintain_aspect_ratio=True, output_format=None, quality=85, workers=None):
    """
    Resizes all valid images in the source directory using multiprocessing.
    """
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        sys.exit(1)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created output directory: '{output_dir}'")

    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff')
    
    # Collect valid files
    tasks = []
    skipped_count = 0

    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if not os.path.isfile(file_path):
            continue
        
        if not filename.lower().endswith(valid_extensions):
            skipped_count += 1
            logging.info(f"Skipped non-image file: {filename}")
            continue
            
        tasks.append((file_path, output_dir, filename, new_size, maintain_aspect_ratio, output_format, quality))

    total_tasks = len(tasks)
    if total_tasks == 0:
        print(f"No valid images found in '{source_dir}'.")
        return

    print(f"Starting batch process for {total_tasks} images...")
    print(f"Target size: {new_size} | Maintain aspect ratio: {maintain_aspect_ratio}")
    if output_format:
        print(f"Converting to: {output_format.upper()}")
        
    logging.info(f"Starting batch process. Target size: {new_size}, Format: {output_format}")

    processed_count = 0
    error_count = 0
    
    # Determine number of workers
    if workers is None:
        workers = min(32, (os.cpu_count() or 1) + 4)

    # Use ProcessPoolExecutor for CPU-bound image processing
    with ProcessPoolExecutor(max_workers=workers) as executor:
        # Submit all tasks
        futures = {executor.submit(process_single_image, task): task for task in tasks}
        
        # Process results with tqdm progress bar
        with tqdm(total=total_tasks, desc="Processing Images", unit="img") as pbar:
            for future in as_completed(futures):
                status, filename, msg = future.result()
                
                if status == 'success':
                    processed_count += 1
                    logging.info(f"Success: {filename}")
                elif status == 'skipped':
                    skipped_count += 1
                    logging.warning(f"Skipped: {filename} - {msg}")
                else:
                    error_count += 1
                    logging.error(f"Error processing {filename}: {msg}")
                    
                pbar.update(1)

    print("\n" + "=" * 40)
    print("Batch Processing Complete!")
    print(f"Processed: {processed_count}")
    print(f"Skipped:   {skipped_count}")
    print(f"Errors:    {error_count}")
    print("Check 'resizer.log' for detailed logs.")
    print("=" * 40)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Batch Image Resizer Tool")
    parser.add_argument("--source", type=str, default="input_images", help="Source directory containing images.")
    parser.add_argument("--output", type=str, default="resized_images", help="Output directory for resized images.")
    parser.add_argument("--width", type=int, default=800, help="Target width in pixels.")
    parser.add_argument("--height", type=int, default=600, help="Target height in pixels.")
    parser.add_argument("--force", action="store_true", help="Force resize to exact dimensions, ignoring aspect ratio.")
    parser.add_argument("--format", type=str, choices=['jpg', 'jpeg', 'png', 'webp'], default=None, help="Convert all images to a specific format.")
    parser.add_argument("--quality", type=int, default=85, help="Quality for JPEG/WEBP output (1-100). Default is 85.")
    parser.add_argument("--workers", type=int, default=None, help="Number of concurrent processes. Defaults to optimal CPU count.")

    args = parser.parse_args()
    maintain_aspect_ratio = not args.force

    # Setup console logging level based on standard run vs debug (omitted for brevity, keeping simple console output)
    logging.getLogger().handlers[1].setLevel(logging.WARNING) # Console only shows warnings/errors to keep tqdm clean

    resize_images(
        source_dir=args.source,
        output_dir=args.output,
        new_size=(args.width, args.height),
        maintain_aspect_ratio=maintain_aspect_ratio,
        output_format=args.format,
        quality=args.quality,
        workers=args.workers
    )
