import os
import csv

def convert_to_geo_coords(normalized_x, normalized_y, coord_x, coord_y, patch_size=640):
    """Converts normalized coordinates to geographical coordinates using base coordinates."""
    pixel_x = normalized_x * patch_size
    pixel_y = normalized_y * patch_size
    geo_x = coord_x + pixel_x
    geo_y = coord_y + pixel_y
    return geo_x, geo_y

def process_detection_files(output_folder, output_geo_file):
    """Processes all detection files and converts YOLO coordinates to geographical coordinates."""
    if not os.path.exists(output_folder):
        print(f"Output folder does not exist: {output_folder}")
        return
    else:
        print(f"Processing files in {output_folder}")

    os.makedirs(os.path.dirname(output_geo_file), exist_ok=True)
    
    with open(output_geo_file, 'w', newline='') as geo_file:
        csv_writer = csv.writer(geo_file)
        csv_writer.writerow(['X', 'Y'])  # Write header

        for root, dirs, files in os.walk(output_folder):
            for file in files:
                if file.endswith("_detect.txt"):
                    detect_file_path = os.path.join(root, file)
                    base_name = file.replace("_detect.txt", "")
                    txt_file_path = os.path.join(root, base_name + ".txt")

                    if not os.path.exists(txt_file_path):
                        print(f"Coordinate file not found for {base_name}, skipping...")
                        continue

                    try:
                        with open(txt_file_path, 'r') as txt_file:
                            coords = txt_file.read().strip()
                            coord_x, coord_y = map(float, coords.strip('()').split(', '))
                    except Exception as e:
                        print(f"Error reading coordinates from {txt_file_path}: {e}")
                        continue

                    try:
                        with open(detect_file_path, 'r') as detect_file:
                            lines = detect_file.readlines()

                        for line in lines:
                            parts = line.split()
                            normalized_x = float(parts[1])
                            normalized_y = float(parts[2])
                            geo_coords = convert_to_geo_coords(normalized_x, normalized_y, coord_x, coord_y)
                            csv_writer.writerow([geo_coords[0], geo_coords[1]])
                    except Exception as e:
                        print(f"Error processing {file}: {e}")

# Define your inputs here
output_folder = 'D:/Master/Data/test/out'
output_geo_file = 'D:/Master/Data/test/output_geographical_coordinates.csv'

# Process the detection files
process_detection_files(output_folder, output_geo_file)
