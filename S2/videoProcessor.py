from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import subprocess
import os
from pytube import YouTube
import numpy as np
#from YUVHistogramExtractorScript import YUVHistogramExtractor
import subtitles
import yuv_histogram
from subtitles import download_video

class VideoProcessor:
    def __init__(self, input_video_path, output_video_path):
        self.input_video_path = input_video_path
        self.output_video_path = output_video_path

    # Task 1
    def cut_video_and_show_macroblocks(self):
        # Step 1: Cut 9 seconds from the input video
        clip = VideoFileClip(self.input_video_path)
        clip = clip.subclip(0, clip.duration - 9)

        # Step 2: Save the trimmed video
        temp_output_path = "temp_trimmed_video.mp4"
        clip.write_videofile(temp_output_path, codec="libx264", audio_codec="aac")


        # Step 3: Use FFmpeg to show macroblocks and motion vectors
        command = [
            'ffmpeg',
            '-v', 'quiet',
            '-i', temp_output_path,
            '-vf', 'showinfo,movie=gradients,mgbounds=macroblock',
            '-an', '-c:v',
            'libx264', '-crf',
            '23', '-preset', 'ultrafast',
            self.output_video_path
        ]
        subprocess.call(command)

        # Step 4: Remove the temporary trimmed video
        subprocess.call(['rm', temp_output_path])

    # Task 2
    def create_new_bbb_container(self):
        # Step 1: Cut BBB into a 50-second video
        clip = VideoFileClip(self.input_video_path)
        clip = clip.subclip(0, 50)

        # Step 2: Export BBB(50s) audio as MP3 mono track
        audio_mono_path = "audio_mono.mp3"
        # Extract audio
        audio = clip.audio
        # Convert stereo to mono using NumPy
        mono_audio = audio.to_soundarray(fps=44100)
        mono_audio = np.mean(mono_audio, axis=1)
        # Export mono audio
        #mono_audio.write_audiofile(audio_mono_path, codec="mp3", bitrate="64k")
        audio.write_audiofile(audio_mono_path, codec="mp3", bitrate="64k")

        # Step 3: Export BBB(50s) audio in MP3 stereo w/ lower bitrate
        audio_stereo_path = "audio_stereo.mp3"
        audio.write_audiofile(audio_stereo_path, codec="mp3", bitrate="32k")

        # Step 4: Export BBB(50s) audio in AAC codec
        audio_aac_path = "audio_aac.aac"
        audio.write_audiofile(audio_aac_path, codec="aac")

        # Step 5: Package everything into an MP4 with FFMPEG
        command = [
            'ffmpeg',
            '-v', 'quiet',
            '-i', audio_mono_path,
            '-i', audio_stereo_path,
            '-i', audio_aac_path,
            '-i', self.input_video_path,
            '-filter_complex',
            '[0:a][1:a][2:a]amerge=inputs=3[aout]',
            '-map', '[aout]',
            '-map', '3:v',
            '-c:v', 'copy',
            '-c:a', 'aac',
            self.output_video_path
        ]
        subprocess.call(command)

        # Step 6: Remove temporary audio files
        subprocess.call(['rm', audio_mono_path, audio_stereo_path, audio_aac_path])

    # Task 3
    def count_tracks_in_container(self):
        # Load the video file using moviepy
        #clip = VideoFileClip(self.input_video_path)

        try:
            # Load the video clip
            video_clip = VideoFileClip(self.input_video_path)

            # Get the number of audio and video tracks
            # Check if there is audio and video
            has_audio = video_clip.audio is not None
            has_video = video_clip.fps is not None

            # Close the video clip
            video_clip.close()
            print(has_audio, has_video)
            return has_audio, has_video

        except Exception as e:
            print(f"Error: {e}")
            return None
    
if __name__ == "__main__":
    path_videos = os.path.join(os.getcwd(),'videos')
    path_processor = os.path.join(os.getcwd(), 'videos', 'processor')
    input_video_path = os.path.join(path_processor,"bunny.mp4") 
    output_macroblocks = os.path.join(path_processor,"output_video_with_macroblocks.mp4")
    path_subtitles = os.path.join(os.getcwd(), 'videos', 'subtitles')
    path_yuv = os.path.join(os.getcwd(), 'videos', 'yuv')
    input_yuv = os.path.join(path_yuv, "Autumn Leaves  Fingerstyle JAZZ Guitar.mp4")
    output_yuv = os.path.join(path_yuv, "output_histogram.mp4")

    
    video_processor = VideoProcessor(input_video_path, output_macroblocks)
    # Task 1
    print('\n\nTask 1:')
    video_processor.cut_video_and_show_macroblocks()
    # Task 2
    print('\n\nTask 2:')
    video_processor.create_new_bbb_container()
    # Task 3
    print('\n\nTask 3:')
    video_processor.count_tracks_in_container()

    # Task 4 and 5
    print('\n\nTask 4 and 5:')
    subtitles.download_subtitles(youtube_url="https://www.youtube.com/watch?v=MPV7JXTWPWI&ab_channel=0612TVw%2FNERDfirst",output_path=os.path.join(path_subtitles,'subtitles'))

    # Task 6
    print('\n\nTask 6:')
    download_video(youtube_url='https://www.youtube.com/watch?v=-XR5ITf4Gj8&ab_channel=SeijiIgusa',output_path=path_yuv)
    hist_extr = yuv_histogram.YUVHistogramExtractor(input_video_path=input_yuv,output_histogram_path=output_yuv)
    hist_extr.create_video_with_histogram()