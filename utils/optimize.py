import os
import io
from PIL import Image
from shutil import rmtree

def adjust_quality_to_target(file_path, target_size_kb, tolerance_kb=100, initial_quality=100):
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
                print(f"Final size: {size_bytes / 1024:.2f} KB")
                break
            elif quality > 10:  # Avoid going under 10
                print(f"Quality: {quality}, Size: {size_bytes / 1024:.2f} KB")
                quality -= 1  # Decrease quality by 1
            else:
                print("Minimum quality reached")
                break  # Stop if minimum quality is reached

    return output_io.getvalue(), quality

def process_images(input_folder, output_folder, target_size_kb=1000, tolerance_kb=100):
    if os.path.exists(output_folder):
        rmtree(output_folder)
    os.makedirs(output_folder)

    count = 0
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
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
