import sys
import subprocess
import ffmpeg
import cv2
import subprocess
import numpy as np
from PIL import Image

def rgb_to_yuv(red, green, blue):
    # Convert RGB to YUV
    y = 0.299 * red + 0.587 * green + 0.114 * blue
    u = 0.492 * (blue - y)
    v = 0.877 * (red - y)
    return y, u, v

def yuv_to_rgb(y, u, v):
    # Convert YUV to RGB
    red = y + 1.13983 * v
    green = y - 0.39465 * u - 0.5806 * v
    blue = y + 2.03211 * u
    return red, green, blue

# Define a method to automate resizing and quality reduction
def resize_and_reduce_quality(input_image, output_image, width, height, quality):
    # Get the width and height of the input image
    image = cv2.imread(input_image)
    og_height, og_width = image.shape[:2]
    print(f'Input image dimensions: {og_width}x{og_height}\n')

    # Check if the output image is reducing
    if width >= og_width & height >= og_height:
         # Use FFmpeg to resize and lower quality of the image
        ffmpeg_command = [
            'ffmpeg',
            '-v', 'quiet',  # Set FFmpeg's verbosity level to quiet
            '-i', input_image,
            '-vf', f'scale={width}:{height}',
            '-q:v', str(quality),
            output_image
        ]

        try:
            subprocess.run(ffmpeg_command, check=True)
            print(f"Resized and converted: {output_image}")
        except:
            print(f"Error processing {output_image}")
    else:
        print('The width x height of the output image needs to be smaller than the input.')

    
def serpentine_read_jpeg(file_path):
    with open(file_path, 'rb') as file:
        # Read the entire file as bytes
        data = file.read()
    
    # Check if it's a JPEG file (JPEG files start with bytes FF D8)
    if data[:2] != b'\xFF\xD8':
        print("This is not a valid JPEG file.")
        return
    
    # Get the width and height of the image from the JPEG header (offsets 163 and 164)
    width = (data[163] << 8) + data[164]
    height = (data[165] << 8) + data[166]

    # Initialize variables for tracking position and direction
    position = 2  # Start after the JPEG header
    direction = 1  # 1 for left-to-right, -1 for right-to-left
    
    for row in range(height):
        if direction == 1:
            # Read from left to right
            for col in range(width):
                print(data[position], end=' ')
                position += 1
        else:
            # Read from right to left
            for col in range(width - 1, -1, -1):
                print(data[position], end=' ')
                position += 1
        
        # Toggle direction for the next row
        direction *= -1
        print()  # Move to the next line for the next row

def convert_to_black_and_white_with_compression(input_image, output_image):
    """
    if not output_image:
        # Crear una nueva imagen en blanco
        cv2.imread(input_image)
        height, width = image.shape[:2]
        background_color = (255, 255, 255)  # Color de fondo blanco
        image = Image.new("RGB", (width, height), background_color)
        image.save(output_image, "JPG")
        image.close()
    """
    # Define FFmpeg command
    ffmpeg_cmd = [
        'ffmpeg',
        '-v', 'quiet',  # Set FFmpeg's verbosity level to quiet
        '-i', input_image,        # Input file
        '-vf', 'format=gray',    # Convert to grayscale
        '-crf', '0',             # Constant Rate Factor (0 for lossless)
        '-preset', 'ultrafast',  # Preset for compression (adjust as needed)
        output_image
    ]

    try:
        # Run the FFmpeg command
        subprocess.run(ffmpeg_cmd, check=True)
        print("Conversion and compression successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion and compression: {e}")

def run_length_encode(data):
    encoded_data = []
    count = 1  # Initialize count with 1 (for the first byte)

    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded_data.append((data[i - 1], count))
            count = 1  # Reset count for the new byte

    # Append the last byte and its count
    encoded_data.append((data[-1], count))

    return encoded_data

def run_length_decode(encoded_data):
    decoded_data = []
    for symbol, count in encoded_data:
        decoded_data.extend([symbol] * count)
    return decoded_data

def main():
    ## Task 1: Converting from RGB to YUV and viceversa
    print('\nTask 1: Converting from RGB to YUV and viceversa')
    # Defining RGB color
    red_rgb = 255
    green_rgb = 128
    blue_rgb = 64
    """
    # Convert RGB to YUV
    y, u, v = rgb_to_yuv(red_rgb, green_rgb, blue_rgb)
    # Convert YUV to RGB
    red, green, blue = yuv_to_rgb(y, u, v)

    print(f'Original RGB color = ({red_rgb}, {green_rgb}, {blue_rgb})')
    print(f'Conversion to YUV = ({y}, {u}, {v})')
    print(f'After transformation RGB = ({red}, {green}, {blue})')
    print(f'RGB truncated: ({int(red)}, {int(green)}, {int(blue)})')
"""
    ## Task 2: Resizing images
    print('\nTask 2: Resizing images')
    # Specify the input and output image files and quality
    input_image = "input.jpg"  # Replace with your input image
    output_image = "output.jpg"  # Replace with the output path
    quality = 20  # Adjust the quality as needed

    # Resize and reduce quality of the input image
    #resize_and_reduce_quality(input_image, output_image, 800, 600, quality)

    ## Task 3: Reading a file in serpentine mode
    print('\nTask 3: Reading a file in serpentine mode')
    serpentine_read_jpeg('degradado.jpg')

    ## Task 4: Transforming an image to B/W
    print('\nTask 4: Transforming an image to B/W')
    input_image = 'input.jpg'
    output_image = 'bw.jpg'
    #convert_to_black_and_white_with_compression(input_image, output_image)
"""
    # Task 5: Run-lenght encoding
    print('\nTask 5: Run-lenght encoding')
    original_data = [1, 1, 1, 2, 2, 3, 4, 4, 4, 4]
    encoded_data = run_length_encode(original_data)
    decoded_data = run_length_decode(encoded_data)

    print("Original Data:", original_data)
    print("Encoded Data:", encoded_data)
    print("Decoded Data:", decoded_data)
"""
if __name__ == "__main__":
    main()
