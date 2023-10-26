import os,subprocess,ffmpeg

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

if __name__ == '__main__':
    input_file = 'bunny.mp4'
    output_file = 'bigBuckBunny.mp2'
    
    convert_mp4_to_mp2(input_file, output_file)
    print(f'Conversion complete. Video saved as {output_file}')

    #video_info = get_video_info(output_file)
    print('Video Information:')
    #print(video_info)
