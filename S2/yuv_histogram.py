import subprocess
import os

# Task 6
class YUVHistogramExtractor:
    def __init__(self, input_video_path, output_histogram_path):
        self.input_video_path = input_video_path
        self.output_histogram_path = output_histogram_path

    def create_video_with_histogram(self):
        # Step 1: Extract YUV Histogram as Image Sequence
        histogram_images = "histogram_%03d.png"
        histogram_cmd = [
            "ffmpeg",
            "-i", self.input_video_path,
            "-vf", "waveform",
            "-pix_fmt", "yuv420p",
            "-vsync", "vfr",
            histogram_images
        ]
        subprocess.run(histogram_cmd)

        # Check if histogram images were created
        if not os.path.exists(histogram_images % 1):
            print("Error: No histogram images were created.")
            return

        # Step 2: Create Video with Histogram
        output_video_cmd = [
            "ffmpeg",
            "-i", self.input_video_path,
            "-i", histogram_images,
            "-filter_complex", "[0:v][1:v] overlay",
            "-c:a", "copy",
            self.output_histogram_path
        ]
        subprocess.run(output_video_cmd)

        # Clean up: Remove temporary histogram images
        for image_file in os.listdir('.'):
            if image_file.startswith("histogram_") and image_file.endswith(".png"):
                os.remove(image_file)