import os
from PIL import Image, ImageDraw, ImageFont

def create_dummy_images(folder_name="input_images", count=5):
    """
    Creates simple colored placeholder images for testing the resizer.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created directory: {folder_name}")

    colors = ['red', 'blue', 'green', 'yellow', 'purple']
    
    print(f"Generating {count} test images in '{folder_name}'...")

    for i in range(count):
        # Create a large random image (e.g., 1920x1080)
        img = Image.new('RGB', (1920, 1080), color=colors[i % len(colors)])
        draw = ImageDraw.Draw(img)

        # Draw a white square
        draw.rectangle([400, 400, 600, 600], fill="white")

        # Optional: Add text for identification
        try:
            font = ImageFont.load_default()
            draw.text((420, 420), f"Img {i+1}", fill="black", font=font)
        except:
            pass  # Safe fallback

        filename = f"test_image_{i+1}.jpg"
        file_path = os.path.join(folder_name, filename)

        img.save(file_path)
        print(f" - Created: {filename}")

    print("Done! You can now run 'image_resizer.py'.")

if __name__ == "__main__":
    create_dummy_images()
