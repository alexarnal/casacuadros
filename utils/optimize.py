import os
import io
from PIL import Image
from shutil import rmtree

def adjust_quality_to_target(file_path, target_size_kb, tolerance_kb=100, initial_quality=85):
    target_size_bytes = target_size_kb * 1024
    tolerance_bytes = tolerance_kb * 1024
    quality = initial_quality

    with Image.open(file_path) as img:
        while True:
            # Save image with current quality to a bytes buffer
            output_io = io.BytesIO()
            img.save(output_io, format='JPEG', quality=quality)
            size_bytes = output_io.tell()

            if target_size_bytes - tolerance_bytes <= size_bytes <= target_size_bytes + tolerance_bytes:
                break
            elif size_bytes < target_size_bytes - tolerance_bytes:
                quality = min(quality + 1, 95)  # Avoid going over 95
            else:
                quality = max(quality - 1, 10)  # Avoid going under 10

            # Break if quality adjustments are ineffective
            if quality == 95 or quality == 10:
                break

    return output_io.getvalue(), quality

def process_images(input_folder, output_folder, target_size_kb=1000, tolerance_kb=100):
    if os.path.exists(output_folder):
        rmtree(output_folder)
    os.makedirs(output_folder)

    count = 0
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.jpg'):
            count += 1
            file_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f'{count}.jpg')

            optimized_data, final_quality = adjust_quality_to_target(file_path, target_size_kb=target_size_kb, tolerance_kb=tolerance_kb)
            with open(output_path, 'wb') as f:
                f.write(optimized_data)
            print(f"Processed {filename} with final quality {final_quality}")

current_directory = os.getcwd()
input_folder = current_directory  # Use current directory for input
output_folder = os.path.join(current_directory, 'optimized')  # Save optimized images in 'optimized' subdirectory

process_images(input_folder, output_folder, target_size_kb=800, tolerance_kb=50)
