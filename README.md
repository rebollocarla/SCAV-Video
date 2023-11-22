# SCAV-Video

All the tasks are develops in functions and tested afterwards in the main. The variables are found in the beginning of the main. You can change them as you want. The input images are in the folder /images or /videos so all input and output photos are going to be stored there by default.

**P1: JPEG & MPEG**

File **_rgb_yuv.py_**

TASK 1: _yuv_to_rgb_ and _rgb_to_yuv_ are functions that transform a color from one measure system to the other. The input and output is a three-element array with the components of the color.

TASK 2: _resize_and_reduce_quality_ receives an input image and returns an image in the same folder as the input photo resized with your desired parameters. 

TASK 3: _serpentine_read_jpeg_ follows an algorithm in order to read an input image (recommended square image for a perfect lecture) in a serpentine way. The output is the matrix following the read order and its size is the size of the image (in pixels).

TASK 4: _convert_to_black_and_white_with_compression_ resizes and compresses and input image. You can change the compression rate in the # Constant Rate Factor (0 for lossless), higher for more compression line. The default value is 30. In the same path as the input image, there appears an output image with the modifications. If the image already exists you are going to be asked to overwrite it.

TASK 5: Given a series of bytes, the function _run_length_encode_ and _run_length_decode_ use run-lenght encoding to encode and decode the array.


File **_DCTConverter.py_**

TASK 6: Using an input an image data, this file encodes and decodes it using DCT.
Functions implemented: __init_, __dct_, __idct_, _convert_to_dct_, _decode_dct_

**P2: Python & Video**

File **_p2.py_**

TASK 1: Having as an input a mp4 file,  _convert_mp4_to_mp2_ converts it and stores it as a mp2 file.

TASK 2: Modifying the resolution of a video to the one you desire (new_resolution variable).

TASK 3: Changing the chroma subsampling of a video (subsampling variable).

TASK 4: Storing and showing in the terminal info of the video of your choice.

TASK 5: Getting a frame from the video of your choice with ffmpeg and resizing it using the function resize_and_reduce_quality from P1 module.

**S2: Python Video**

File **_video_processor.py_**

TASK 1, 2 and 3 are defined in functions in this file inside the class _VideoProcessor_. The main of the whole seminar is found in this file as well.

File **_subtitles.py_**
TASK 4: Downloading the URL video, downloading its subtitles and joining them with the video developed in different functions.
TASK 5 is calling it in the previous file.

File **_yuv_histogram.py_**
TASK 6: Creates the YUV histogram of the video introduced as input inside the class YUVHistogram. Called in the _video_processor.py_ main.
