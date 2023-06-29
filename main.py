import os
import shutil
import numpy as np
from skimage import img_as_float
from skimage.metrics import structural_similarity as ssim
from PIL import Image

def scan_qr_codes(folder_path, original_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a directory.")
        return

    # Make sure a "readable" folder exists, if not, create one
    readable_dir = os.path.join(folder_path, "readable")
    os.makedirs(readable_dir, exist_ok=True)

    original_img = img_as_float(Image.open(original_path).convert('L'))
    
    file_count = 0
    qr_code_count = 0

    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            file_count += 1
            file_path = os.path.join(folder_path, filename)
            try:
                img = Image.open(file_path).convert('L')
                img_resized = img.resize(original_img.shape[1::-1])  # Resize to match original
                img_resized = img_as_float(img_resized)

                score = ssim(original_img, img_resized, data_range=1.0)

                if score > 0.22: # Change threshold as needed
                    qr_code_count += 1
                    print(f"Readable QR Code in {filename} with SSIM {score}")
                    # Copy the readable QR code to the "readable" folder
                    shutil.copy(file_path, readable_dir)
                else:
                    print(f"Unreadable QR Code in {filename} with SSIM {score}")

            except Exception as e:
                print(f"Error processing image file '{filename}': {str(e)}")

    if file_count == 0:
        print(f"No image files found in '{folder_path}'.")
    elif qr_code_count == 0:
        print(f"No QR codes found in the {file_count} image files.")

if __name__ == "__main__":
    scan_qr_codes("./images", "./original_qr.png")
