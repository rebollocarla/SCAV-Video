import os,subprocess,ffmpeg, sys

def convert_mp4_to_mp2(input_file, output_file):
    command = [
    "ffmpeg",
    "-i", input_file,
    "-vcodec", "h264",
    "-acodec", "mp2",
    output_file
    ]

    subprocess.run(command)

    #ffmpeg.input(input_file).output(output_file, acodec='mp2', vcodec='copy').run(overwrite_output=False)

def get_video_info(mp2_file):
    cmd = f'ffmpeg -i {mp2_file} 2>&1 | grep Video:'
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    return result.decode('utf-8')

def modify_video_resolution(input_file, output_file, new_resolution):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"scale={new_resolution}",
        output_file
    ]
    subprocess.run(command)

def change_chroma_subsampling(input_file, output_file, subsampling):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"format=yuv420p",
        "-pix_fmt", subsampling,
        output_file
    ]
    subprocess.run(command)    

def get_video_info2(mp2_file):
    cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration,codec_name,bit_rate -of default=noprint_wrappers=1:nokey=1 {mp2_file}'
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, _ = result.communicate()
    return output

if __name__ == '__main__':
    path_videos = os.path.join(os.getcwd(),'videos')
"""
    input_file = 'bunny.mp4'
    mp2_file = 'bigBuckBunny.mp2'
    resolution_file = 'modified_bigBuckBunny.mp2'
    subsampled_file = 'subsampled_bigBuckBunny.mp2'
    new_resolution = "640x360"
    subsampling = "yuv422p"

    # Convert MP4 to MP2
    convert_mp4_to_mp2(input_file, mp2_file)
    print(f'Conversion complete. Video saved as {mp2_file}')

    # Modify the resolution (e.g., from 1280x720 to 640x360)
    modify_video_resolution(mp2_file, mp2_file, new_resolution)
    print(f'Modified resolution. Video saved as {resolution_file}')

    video_info = get_video_info(mp2_file)
    print('Video Information:')
    print(video_info)
   
    # Change the chroma subsampling (e.g., to yuv422p)
    change_chroma_subsampling(mp2_file, subsampled_file, subsampling)
    print(f'Changed chroma subsampling. Video saved as {subsampled_file}')
    
    # Get and print relevant video information
    video_info = get_video_info2(subsampled_file)
    print('Video Information:')
    print(video_info)
"""
# Add the directory containing your class module to the sys.path
current_path = os.path.abspath(os.getcwd())
p1_path = os.path.join(current_path,'P1')
os.chdir(p1_path)
sys.path.append(os.getcwd())

# Now you can import the class
from DCTConverter import DCTConverter

class ModifiedDCTConverter(DCTConverter):
    def __init__(self, block_size=8):
        self.block_size = block_size

    def print_value(self):
        print(f"Value: {self.value}, Extra Value: {self.extra_value}")

obj = ModifiedDCTConverter([1,1,1,2])
obj.print_value()