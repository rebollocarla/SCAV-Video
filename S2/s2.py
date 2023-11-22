from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import subprocess
import os
from pytube import YouTube
#from YUVHistogramExtractorScript import YUVHistogramExtractor

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
        command = (
            f"ffmpeg -i {temp_output_path} quiet -vf"
            " showinfo;movie=gradients;mgbounds=macroblock"
            f" -an -c:v libx264 -crf 23 -preset ultrafast {self.output_video_path}"
        )
        subprocess.call(command, shell=True)

        # Step 4: Remove the temporary trimmed video
        subprocess.call(f"rm {temp_output_path}", shell=True)

    # Task 2
    def create_new_bbb_container(self):
        # Step 1: Cut BBB into a 50-second video
        clip = VideoFileClip(self.input_video_path)
        clip = clip.subclip(0, 50)

        # Step 2: Export BBB(50s) audio as MP3 mono track
        audio_mono_path = "audio_mono.mp3"
        clip.audio.write_audiofile(audio_mono_path, codec="mp3", bitrate="64k", mono=True)

        # Step 3: Export BBB(50s) audio in MP3 stereo w/ lower bitrate
        audio_stereo_path = "audio_stereo.mp3"
        clip.audio.write_audiofile(audio_stereo_path, codec="mp3", bitrate="32k", mono=False)

        # Step 4: Export BBB(50s) audio in AAC codec
        audio_aac_path = "audio_aac.aac"
        clip.audio.write_audiofile(audio_aac_path, codec="aac")

        # Step 5: Package everything into an MP4 with FFMPEG
        command = (
            f"ffmpeg -i {audio_mono_path} -i {audio_stereo_path} -i {audio_aac_path} "
            f"-i {self.input_video_path} -filter_complex "
            f"[0:a][1:a][2:a]amerge=inputs=3[aout] -map [aout] -map 3:v "
            f"-c:v copy -c:a aac {self.output_video_path}"
        )
        subprocess.call(command, shell=True)

        # Step 6: Remove temporary audio files
        subprocess.call(f"rm {audio_mono_path} {audio_stereo_path} {audio_aac_path}", shell=True)

    # Task 3
    def count_tracks_in_container(self):
        # Load the video file using moviepy
        clip = VideoFileClip(self.input_video_path)

        # Get the number of audio and video tracks
        num_audio_tracks = len(clip.audio)
        num_video_tracks = len(clip.video)

        # Print the results
        print(f"Number of audio tracks: {num_audio_tracks}")
        print(f"Number of video tracks: {num_video_tracks}")

if __name__ == "__main__":
    path_videos = os.path.join(os.getcwd(),'videos')
    input_video_path = os.path.join(path_videos,"bunny.mp4") 
    output_macroblocks = os.path.join(path_videos,"output_video_with_macroblocks.mp4")
    output_container = os.path.join(path_videos,"output_bbb_container.mp4")

    video_processor = VideoProcessor(input_video_path, output_macroblocks)
    # Task 1
    print('\n\nTask 1: ')
    video_processor.cut_video_and_show_macroblocks()
    # Task 2
    print('\n\nTask 2: ')
    video_processor.create_new_bbb_container()
    # Task 3
    print('\n\nTask 3: ')
    video_processor.count_tracks_in_container()
"""
# Task 4
def download_subtitles(youtube_url, output_path):
    # Download YouTube video
    yt = YouTube(youtube_url)
    video = yt.streams.filter(file_extension='mp4').first()
    video_path = video.download(output_path)

    # Download subtitles (assuming English)
    subtitles = yt.captions.get_by_language_code('en')
    subtitles_content = subtitles.generate_srt_captions()

    with open(output_path + "/subtitles.srt", 'w', encoding='utf-8') as file:
        file.write(subtitles_content)

    return video_path, output_path + "/subtitles.srt"
# Task 4
def add_subtitles(video_path, subtitles_path, output_path):
    # Load video and subtitles
    video_clip = VideoFileClip(video_path)
    subtitles_clip = TextClip(subtitles_path, fontsize=24, color='white')

    # Composite video with subtitles
    video_with_subtitles = CompositeVideoClip([video_clip.set_pos('center'), subtitles_clip.set_pos('bottom')])

    # Write the video with subtitles to a file
    video_with_subtitles.write_videofile(output_path, codec='libx264', audio_codec='aac', temp_audiofile='temp_audio.m4a', remove_temp=True)

if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=example"  # Replace with your YouTube video URL
    output_path = "./output"

    video_path, subtitles_path = download_subtitles(youtube_url, output_path)
    output_video_path = output_path + "/output_video_with_subtitles.mp4"

    add_subtitles(video_path, subtitles_path, output_video_path)


# EX 5

class SubtitleProcessor:
    def __init__(self, video_processor):
        self.video_processor = video_processor

    def download_subtitles(self, youtube_url, output_path):
        # Download subtitles using the new script
        return self.video_processor.download_subtitles(youtube_url, output_path)

    def add_subtitles(self, video_path, subtitles_path, output_path):
        # Inherit and modify the add_subtitles function
        video_clip = self.video_processor.add_subtitles(video_path, subtitles_path, output_path)

        # Add any additional modifications or enhancements if needed

        return video_clip


class EnhancedVideoProcessor(SubtitleProcessor, VideoProcessor):
    def __init__(self, input_video_path, output_video_path):
        VideoProcessor.__init__(self, input_video_path, output_video_path)
        SubtitleProcessor.__init__(self, self)

    def process_video_with_subtitles(self, youtube_url):
        # Download subtitles
        video_path, subtitles_path = self.download_subtitles(youtube_url, "./output")

        # Add subtitles to the video
        output_video_path = "./output/output_video_with_subtitles.mp4"
        self.add_subtitles(video_path, subtitles_path, output_video_path)


if __name__ == "__main__":
    input_video_path = "input_video.mp4"  # Replace with your input video path
    output_video_path = "output_bbb_container.mp4"
    youtube_url = "https://www.youtube.com/watch?v=example"  # Replace with your YouTube video URL

    video_processor = EnhancedVideoProcessor(input_video_path, output_video_path)
    video_processor.process_video_with_subtitles(youtube_url)


# EX 6
class YUVHistogramExtractor:
    def __init__(self, input_video_path, output_histogram_path):
        self.input_video_path = input_video_path
        self.output_histogram_path = output_histogram_path

    def extract_yuv_histogram(self):
        # Use FFmpeg to extract the YUV histogram
        command = (
            f"ffmpeg -i {self.input_video_path} -vf "
            "'split=3[a][b][c];[a]histogram=mode=waveform:format=yuv420p[al];"
            "[b]histogram=mode=waveform:format=yuv420p[bl];"
            "[c]histogram=mode=waveform:format=yuv420p[cl];"
            "[al][bl][cl]vstack=inputs=3[out]' "
            f"-map '[out]' -y {self.output_histogram_path}"
        )
        subprocess.call(command, shell=True)

if __name__ == "__main__":
    input_video_path = "input_video.mp4"  # Replace with your input video path
    output_histogram_path = "output_histogram.mp4"

    yuv_histogram_extractor = YUVHistogramExtractor(input_video_path, output_histogram_path)
    yuv_histogram_extractor.extract_yuv_histogram()





class MainVideoProcessor:
    def __init__(self, input_video_path, output_video_path):
        self.input_video_path = input_video_path
        self.output_video_path = output_video_path

    def process_video_with_histogram(self):
        # Inherit and modify the extract_yuv_histogram function
        histogram_extractor = YUVHistogramExtractor(self.input_video_path, "histogram.mp4")
        histogram_extractor.extract_yuv_histogram()

        # Load the video and the histogram
        video_clip = VideoFileClip(self.input_video_path)
        histogram_clip = VideoFileClip("histogram.mp4")

        # Composite video with histogram
        video_with_histogram = video_clip.set_duration(histogram_clip.duration)
        video_with_histogram = video_with_histogram.set_audio(histogram_clip.audio)
        video_with_histogram = video_with_histogram.set_video_clip(histogram_clip)

        # Write the video with histogram to a file
        video_with_histogram.write_videofile(self.output_video_path, codec='libx264', audio_codec='aac', temp_audiofile='temp_audio.m4a', remove_temp=True)

if __name__ == "__main__":
    input_video_path = "input_video.mp4"  # Replace with your input video path
    output_video_path = "output_video_with_histogram.mp4"

    main_processor = MainVideoProcessor(input_video_path, output_video_path)
    main_processor.process_video_with_histogram()
"""