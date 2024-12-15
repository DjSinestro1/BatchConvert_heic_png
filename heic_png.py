import os
from PIL import Image

# Set directory containing HEIC files
directory = 'heic_img'

# Get all HEIC files
files = [f for f in os.listdir(directory) if f.endswith('.heic')]

# Convert each file
for filename in files:
    input_path = os.path.join(directory, filename)
    output_path = os.path.join(directory, os.path.splitext(filename)[0] + '.png')
    image = Image.open(input_path)
    image.save(output_path)