import sys, subprocess, ffmpeg, cv2, os
import numpy as np
from PIL import Image

def rgb_to_yuv(rgb_color,truncate=False):
    # Convert RGB to YUV
    red = rgb_color[0]
    green = rgb_color[1]
    blue = rgb_color[2]

    y = 0.299 * red + 0.587 * green + 0.114 * blue
    u = 0.492 * (blue - y)
    v = 0.877 * (red - y)

    if truncate:
        return [int(y), int(u), int(v)]
    else:
        return [y, u, v]

def yuv_to_rgb(yuv_color,truncate=False):
    # Convert YUV to RGB
    y = yuv_color[0]
    u = yuv_color[1]
    v = yuv_color[2]

    red = y + 1.13983 * v
    green = y - 0.39465 * u - 0.5806 * v
    blue = y + 2.03211 * u

    if truncate:
        return [int(red), int(green), int(blue)]
    else:
        return [red, green, blue]

# Define a method to automate resizing and quality reduction
def resize_and_reduce_quality(input_image, output_image, width, height):
    
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
            output_image
        ]

        try:
            subprocess.run(ffmpeg_command, check=True)
            print(f"Resized and converted: {output_image}")
            print(f'Output image dimensions: {width}x{height}\n')
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

    # Get the width and height of the image from the JPEG header (offsets 163 and 164)
    width = (data[163] << 8) + data[164]
    height = (data[165] << 8) + data[166]

    # Determine the matrix size as the minimum of width and height
    matrix_size = min(width, height)

    # Initialize variables for tracking position
    position = 2  # Start after the JPEG header

    # Define the order to read the matrix in the specified pattern
    order = []

    # Calculate the order of elements in the matrix
    row, col = 0, 0  # Start at the top-left corner
    order.append(row * matrix_size + col)
    col += 1
    order.append(row * matrix_size + col)
    upwards = False

    while row != matrix_size - 1 or col != matrix_size - 1:
        if upwards:
            while row > 0 and col < matrix_size - 1:
                row -= 1
                col += 1
                order.append(row * matrix_size + col)
            if col == matrix_size - 1:
                row += 1
            else:
                col += 1
            order.append(row * matrix_size + col)
            
        else:
            while col > 0 and row < matrix_size - 1:
                row += 1
                col -= 1
                order.append(row * matrix_size + col)
            if row == matrix_size - 1:
                col += 1
            else:
                row += 1
            order.append(row * matrix_size + col)
        
        upwards = not upwards

    count = 0
    for index in order:
        print(data[position + index], end=' ')
        
        # If we've reached the end of a row, print a newline
        if count % matrix_size == matrix_size - 1:
            print()
        count += 1

def convert_to_black_and_white_with_compression(input_image, output_image):

    # Define FFmpeg command
    ffmpeg_cmd = [
        'ffmpeg',
        '-v', 'quiet',  # Set FFmpeg's verbosity level to quiet
        '-i', input_image,        # Input file
        '-vf', 'format=gray',    # Convert to grayscale
        '-crf', '30',             # Constant Rate Factor (0 for lossless), higher for more compression
        '-preset', 'slow',  # Preset for compression (adjust as needed)
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
    ## Variables
    path_images = os.path.join(os.getcwd(),'images')
    # Task 1
    rgb_og = [255, 128, 64]
    # Task 2
    resize_input = os.path.join(path_images,"resize_input.jpg")  # Replace with your input image
    resize_output = os.path.join(path_images,"resize_output.jpg")  # Replace with the output path
    width = 800
    height = 600
    # Task 3
    serpentine_img = os.path.join(path_images,'degradado.jpg')
    # Task 4
    bw_input = os.path.join(path_images,'bw_input.jpg')
    bw_output = os.path.join(path_images,'bw_output.jpg')
    # Task 5
    original_data = [1, 1, 1, 2, 2, 3, 4, 4, 4, 4]

    ## Task 1: Converting from RGB to YUV and viceversa
    print('\nTask 1: Converting from RGB to YUV and viceversa')
    
    # Convert RGB to YUV
    yuv_color = rgb_to_yuv(rgb_og,truncate=True)
    # Convert YUV to RGB
    rgb_color = yuv_to_rgb(yuv_color,truncate=True)

    print(f'Original RGB color = {rgb_og}')
    print(f'Conversion to YUV = {yuv_color}')
    print(f'After transformation RGB = {rgb_color}')


    ## Task 2: Resizing images
    print('\nTask 2: Resizing images')
    # Resize and reduce quality of the input image
    resize_and_reduce_quality(resize_input, resize_output, width, height)

    ## Task 3: Reading a file in serpentine mode
    print('\nTask 3: Reading a file in serpentine mode')
    serpentine_read_jpeg(serpentine_img)

    ## Task 4: Transforming an image to B/W
    print('\nTask 4: Transforming an image to B/W')
    convert_to_black_and_white_with_compression(bw_input, bw_output)

    # Task 5: Run-lenght encoding
    print('\nTask 5: Run-lenght encoding')
    encoded_data = run_length_encode(original_data)
    decoded_data = run_length_decode(encoded_data)

    print("Original Data:", original_data)
    print("Encoded Data:", encoded_data)
    print("Decoded Data:", decoded_data)

if __name__ == "__main__":
    main()
