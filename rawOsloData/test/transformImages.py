import os
import math
import numpy as np
from PIL import Image
import tifffile as tiff
import argparse


"""
To run the script and process a specific number of images:

python transformImages.py --input_folder ./eksport_6232023_1 --output_folder ./out --number 3
"""





# Constants
patch_size = 640

def pad_image(image, target_height, target_width):
    """Pads an image with black pixels to the target size."""
    padded_image = Image.new("RGB", (target_width, target_height))
    padded_image.paste(image, (0, 0))
    return padded_image

def save_image_patch(image_patch, row, col, base_name, coords, output_folder):
    """Saves a single image patch and its coordinates."""
    output_path = os.path.join(output_folder, base_name, f'{base_name}_patch_{row}_{col}.jpg')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image_patch.save(output_path, "JPEG")

    # Save coordinates
    coords_path = os.path.join(output_folder, base_name, f'patch_{row}_{col}.txt')
    with open(coords_path, 'w') as f:
        f.write(f'{coords}\n')

def split_image(image, patch_size, base_name, tfw_params, output_folder):
    """Splits the image into smaller patches of a given size."""
    width, height = image.size
    num_cols = math.ceil(width / patch_size)
    num_rows = math.ceil(height / patch_size)

    for row in range(num_rows):
        for col in range(num_cols):
            left = col * patch_size
            upper = row * patch_size
            right = min((col + 1) * patch_size, width)
            lower = min((row + 1) * patch_size, height)
            image_patch = image.crop((left, upper, right, lower))

            if image_patch.size[0] < patch_size or image_patch.size[1] < patch_size:
                image_patch = pad_image(image_patch, patch_size, patch_size)

            # Calculate coordinates
            coords = calculate_geographical_coordinates(left, upper, tfw_params)
            save_image_patch(image_patch, row, col, base_name, coords, output_folder)

def calculate_geographical_coordinates(x, y, tfw_params):
    """Calculates the geographical coordinates from image coordinates."""
    A, D, B, E, C, F = tfw_params
    x_geo = A * x + B * y + C
    y_geo = D * x + E * y + F
    return x_geo, y_geo

def read_tfw(tfw_file):
    """Reads the TFW file and returns the transformation parameters."""
    with open(tfw_file, 'r') as f:
        params = [float(line.strip()) for line in f.readlines()]
    return params

def process_all_files(input_folder, patch_size, output_folder, num_files=None):
    """Processes TIF files in the input folder."""
    tif_files = [f for f in os.listdir(input_folder) if f.endswith(".tif")]

    if num_files is not None:
        tif_files = tif_files[:num_files]

    for filename in tif_files:
        input_file = os.path.join(input_folder, filename)
        base_name = os.path.splitext(filename)[0]
        tfw_file = os.path.join(input_folder, base_name + '.tfw')
        
        # Read the TFW file
        tfw_params = read_tfw(tfw_file)

        # Open the TIF image
        with tiff.TiffFile(input_file) as tif:
            image = tif.asarray()
            image = Image.fromarray(image)

        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Split the image
        split_image(image, patch_size, base_name, tfw_params, output_folder)

def main():
    parser = argparse.ArgumentParser(description='Process TIF images.')
    parser.add_argument('--input_folder', type=str, required=True, help='Input folder containing TIF files')
    parser.add_argument('--output_folder', type=str, required=True, help='Output folder for processed images')
    parser.add_argument('--number', type=int, default=None, help='Number of images to process')
    
    args = parser.parse_args()

    input_folder = args.input_folder
    output_folder = args.output_folder
    num_files = args.number

    process_all_files(input_folder, patch_size, output_folder, num_files)

if __name__ == '__main__':
    main()
