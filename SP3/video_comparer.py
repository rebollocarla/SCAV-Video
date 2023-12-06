import subprocess
import os

# Task 2
class VideoComparer:
    def __init__(self, input_video1, input_video2, output_video):
        self.input_video1 = input_video1
        self.input_video2 = input_video2
        self.output_video = output_video

    def compare_videos(self, codec1, codec2):
        command1 = [
            "ffmpeg",
    
            "-i", self.input_video1,
            "-c:v", codec1,
            "-c:a", "copy",
            "temp_video1.mp4"
        ]
        command2 = [
            "ffmpeg",
            
            "-i", self.input_video2,
            "-c:v", codec2,
            "-c:a", "copy",
            "temp_video2.mp4"
        ]
        command3 = [
            "ffmpeg",
  
            "-i", "temp_video1.mp4",
            "-i", "temp_video2.mp4",
            "-filter_complex", "[0:v][1:v]hstack=inputs=2[v];[0:a][1:a]amerge[a]",
            "-map", "[v]",
            "-map", "[a]",
            "-ac", "2",
            "-c:v", "libx264",
            "-c:a", "aac",
            self.output_video
        ]
        subprocess.run(command1)
        #result = subprocess.run(command1, stderr=subprocess.PIPE)
        #if result.returncode != 0:
        #    print("Error:", result.stderr.decode("utf-8"))

        print('done 1')
        subprocess.run(command2)
        print('done 2')
        subprocess.run(command3)

        print(f"Comparison completed for {codec1} vs {codec2}. Output video saved to {self.output_video}")
#"-v", "quiet",