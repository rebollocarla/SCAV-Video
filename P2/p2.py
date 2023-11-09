import os
import subprocess
import ffmpeg
import sys
from P1 import rgb_yuv

# Converting mp4 to mp2 
def convert_mp4_to_mp2(input_file, output_file):
    command = [
    'ffmpeg',
    '-v', 'quiet',  # Set FFmpeg's verbosity level to quiet
    '-i', input_file,
    '-vcodec', 'h264',
    '-acodec', 'mp2',
    output_file
    ]
    subprocess.run(command)

# Modifying the resolution of video to new_resolution
def modify_video_resolution(input_file, output_file, new_resolution):
    command = [
        'ffmpeg',
        '-v', 'quiet',
        '-i', input_file,
        '-vf', f'scale={new_resolution}',
        output_file
    ]
    subprocess.run(command)

# Modifying the chroa subsampling of a video to subsampling
def change_chroma_subsampling(input_file, output_file, subsampling):
    command = [
        'ffmpeg',
        '-v', 'quiet',
        '-i', input_file,
        '-vf', f'format=yuv420p',
        '-pix_fmt', subsampling,
        output_file
    ]
    subprocess.run(command)    

# Obtaining the video information 
def get_video_info(input_file):
    cmd = f'ffmpeg -i {input_file} -f null -  2>&1 | tee P2/videoInfo.txt'
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    return result.decode('utf-8')

# Interacting with resize_and_reduce_quality function from P1 capturing a frame from an input video and reducing its size.
def capture_modify_frame(input_file, output_frame_og, output_frame_reduced, width, height):
    cmd = f'ffmpeg -i {input_file} -ss 00:00:10 -vframes 1 {output_frame_og}'
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    rgb_yuv.resize_and_reduce_quality(input_image=output_frame_og,output_image=os.path.join(output_frame_reduced),width=width,height=height)

def main():
    ## Variables 
    current_path = os.getcwd()
    path_videos = f'{current_path}/P2/videos'
    #path_videos = os.path.join(current_path,'/P2/videos')
    # Task 1: Pick your input file and the name of the output MP2.
    input_file = os.path.join(path_videos,'bunny.mp4')
    mp2_file = os.path.join(path_videos,'bigBuckBunny.mp2')
    # Task 2: Choose your resolution (try to respect the aspect ratio) and the name of the output.
    new_resolution = "640x360"
    resolution_file = os.path.join(path_videos,'modified_bigBuckBunny.mp4')
    # Task 3: Choose your subsampling and the name of the output.
    subsampling = "yuv422p"
    subsampled_file = os.path.join(path_videos,'subsampled_bigBuckBunny.mp4')
    # Task 4: Choose the video to get info from.
    video_info = input_file
    
    # Task 5: Choose the video to get the frame from, the frame number to capture and the name to store it.
    input_video = input_file
    output_frame = os.path.join(path_videos,'bunny_frame.jpg')
    output_frame_red = os.path.join(path_videos,'bunny_frame_resized.jpg')
    width = 150
    height = 20
    
    ## Task 1: Convert MP4 to MP2
    print('\nTask 1: Converting MP4 to MP2')
    convert_mp4_to_mp2(input_file, mp2_file)
    print(f'Conversion complete. Video saved as {mp2_file}')

    ## Task 2: Modify the resolution (e.g., from 1280x720 to 640x360)
    print('\nTask 2: Modify the resolution of the video')
    modify_video_resolution(input_file, resolution_file, new_resolution)
    print(f'The resolution has been modified to: {new_resolution}.')
    print(f'Video saved as {resolution_file}')
    
    video_info = get_video_info(input_file)
    print(f'Video Information {resolution_file}:\n{video_info}')
    
    ## Task 3: Change the chroma subsampling (e.g., to yuv422p)
    print('\nTask 3: Change the chroma subsampling')
    change_chroma_subsampling(input_file, subsampled_file, subsampling)
    print(f'Chroma subsampling modified to {subsampling}.')
    print(f'Video saved as {subsampled_file}')
    
    ## Task 4: Get and print relevant video information
    print('\nTask 4: Get and print relevant video information')
    video_info = get_video_info(subsampled_file)
    print(f'Video Information {subsampled_file}:\n{video_info}')
    
    ## Task 5: Import P1 package and interact with it
    print('\nTask 5: Import P1 package and interact with it')
    capture_modify_frame(input_video, output_frame, output_frame_red, width, height)
    
if __name__ == "__main__":
    main()