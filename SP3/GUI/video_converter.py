import os
import subprocess
import numpy as np

# Task 1
class VideoConverter:
    def __init__(self, input_video):
        self.input_video = input_video

    def convert_resolution(self, output_video, resolution):
        command = [
            "ffmpeg",
            "-i", self.input_video,
            "-vf", f"scale={resolution}", # 1280x720
            "-c:a", "copy",
            output_video
        ]
        try:
            subprocess.run(command, check=True)
            #print("Conversion completed successfully.")
        except subprocess.CalledProcessError as e:
            #print(f"Error: FFmpeg command failed with exit code {e.returncode}")
            pass

    def convert_codec(self, output_video, video_codec):
        command = []
        output_name = ""
        if video_codec == "libvpx":
            command = [
                "ffmpeg",
                "-i", self.input_video,
                "-c:v", video_codec,
                "-b:v", "1M",
                "-c:a", "libvorbis",    
                f"{output_video}.webm"
            ]
            output_name = f"{output_video}.webm"
        elif video_codec == "libvpx-vp9":
            command = [
                "ffmpeg",
                "-i", self.input_video,
                "-c:v", video_codec,
                "-b:v", "2M",
                "-c:a", "libvorbis",    
                f"{output_video}.webm"
            ]
            output_name = f"{output_video}.webm"
        elif video_codec == "libx265":
            command = [
                "ffmpeg",
                "-i", self.input_video,
                "-c:v", video_codec,
                "-crf", "28",
                "-c:a", "aac",    
                "-b:a", "128k",
                f"{output_video}.mp4"
            ]
            output_name = f"{output_video}.mp4"
        elif video_codec == "libaom-av1":
            command = [
                "ffmpeg",
                "-i", self.input_video,
                "-c:v", video_codec,
                "-b:v", "2M",
                "-strict", "experimental",
                "-c:a", "libopus",    
                f"{output_video}.webm"
            ]
            output_name = f"{output_video}.webm"
        else:
            #print('The video codec you introduced can not be used.')
            return

        #print("Executing FFmpeg command:", " ".join(command))
        try:
            subprocess.run(command, check=True)
            return output_name
        except subprocess.CalledProcessError as e:
            #print(f"Error: FFmpeg command failed with exit code {e.returncode}")
            pass