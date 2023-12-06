import os
import subprocess
import numpy as np
import video_comparer

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
            print("Conversion completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error: FFmpeg command failed with exit code {e.returncode}")


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
            print('The video codec you introduced can not be used.')
            return

        print("Executing FFmpeg command:", " ".join(command))
        try:
            subprocess.run(command, check=True)
            return output_name
        except subprocess.CalledProcessError as e:
            print(f"Error: FFmpeg command failed with exit code {e.returncode}")

    
if __name__ == "__main__":
    ## Path variables
    current_path = os.getcwd()
    path_videos = os.path.join(current_path, "videos")
    path_converter = os.path.join(path_videos, "converter")
    path_comparer = os.path.join(path_videos, "comparer")
    
    ## Task 1 variables
    input = os.path.join(path_videos, "Autumn Leaves  Fingerstyle JAZZ Guitar.mp4")
    resolutions = ['1280x720', '640x480', '360x240', '160x120']
    
    # Choose the resolutions (listed above)
    used_resol1 = resolutions[2]
    used_resol2 = resolutions[0]
    codecs = {
        "VP8": "libvpx",
        "VP9": "libvpx-vp9",
        "h265": "libx265",
        "AV1": "libaom-av1"
    }
    used_codec = list(codecs.items())

    # Choose the codecs (listed above)
    used_codec1 = used_codec[0]
    used_codec2 = used_codec[1]

    # Output variables
    output_res_1 = os.path.join(path_converter, f"AutumnLeaves_{used_resol1}.mp4")
    output_res_2 = os.path.join(path_converter, f"AutumnLeaves_{used_resol2}.mp4")
    output_codec_1 = os.path.join(path_converter, f"AutumnLeaves_{used_resol1}_{used_codec1[0]}")
    output_codec_2 = os.path.join(path_converter, f"AutumnLeaves_{used_resol2}_{used_codec2[0]}")
    
    ## Task 2 variables
    output_comparer = os.path.join(path_comparer,"AutumnLeaves_comparison.mp4")

    # Task 1
    print("\n\nTask 1:")
    # Creating input video 1
    print(f"\nVideo 1: Converting {os.path.basename(input)} into {used_resol1} with the codec {used_codec1[0]} stored as {output_res_1}")
    converter = VideoConverter(input_video=input)
    converter.convert_resolution(output_video=output_res_1, resolution=used_resol1)
    
    converter_codec = VideoConverter(input_video=output_res_1)
    output_name_1 = converter_codec.convert_codec(output_video=output_codec_1, video_codec=used_codec1[1])

    # Creating input video 2
    print(f"\nVideo 2: Converting {os.path.basename(input)} into {used_resol2} with the codec {used_codec2[0]} stored as {output_res_2}")
    converter.convert_resolution(output_video=output_res_2, resolution=used_resol2)

    converter_codec2 = VideoConverter(input_video=output_res_2)
    output_name_2 = converter_codec2.convert_codec(output_video=output_codec_2, video_codec=used_codec2[1])

    # Task 2
    print("\n\nTask 2:")
    print(f"\nVideo 2: Comparing {os.path.basename(output_codec_1)} with {os.path.basename(output_codec_2)}")
    converter = video_comparer.VideoComparer(input_video1=output_name_1, input_video2=output_name_2, output_video=output_comparer)
    converter.compare_videos(codec1=used_codec1[1], codec2=used_codec2[1])