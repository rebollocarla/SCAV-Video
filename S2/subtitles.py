import yt_dlp
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
#from moviepy.video.io.VideoFileClip import VideoFileClipError
import os
from pytube import YouTube


def download_video(youtube_url, output_path):
    try:
        # Download YouTube video
        yt = YouTube(youtube_url)
        video = yt.streams.get_highest_resolution()  # Get the highest resolution stream
        video_path = video.download(output_path)

        return video_path

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def download_subtitles_with_yt_dlp(youtube_url, output_path):
    try:
        # Set up options for yt_dlp
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'writesubtitles': True,
            'subtitleslangs': ['en'],  # Language code for English subtitles
            'skip_download': True,  # Do not download the video file
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info about the video
            info_dict = ydl.extract_info(youtube_url, download=False)

            # Check if subtitles are available
            if 'en' in info_dict.get('requested_subtitles', {}):
                # Download subtitles
                ydl.download([youtube_url])

                # Get the subtitle file name
                subtitle_file_name = f"{output_path}/{info_dict['title']}.en.vtt"

                return subtitle_file_name
            else:
                print("No English subtitles available for this video.")
                return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def download_and_add_subtitles(youtube_url, output_path):
    try:
        # Download subtitles with yt_dlp
        subtitle_file = download_subtitles_with_yt_dlp(youtube_url, output_path)

        if subtitle_file:
            # Load video clip
            video_clip = VideoFileClip(f"{output_path}/{yt_dlp.YoutubeDL().extract_info(youtube_url)['title']}.mp4")

            # Load subtitles
            subtitles = TextClip.subclip(txt=subtitle_file, fontsize=24, color='white', bg_color='black')

            # Composite video clip with subtitles
            video_with_subtitles = CompositeVideoClip([video_clip.set_pos('center'), subtitles.set_pos('bottom')])

            # Write the final video with subtitles
            output_video_path = f"{output_path}/video_with_subtitles.mp4"
            video_with_subtitles.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

            return output_video_path
        else:
            print("Error: Subtitles not downloaded.")
            return None

    #except VideoFileClipError as ve:
    #    print(f"Error loading video: {str(ve)}")
    #    return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example usage
youtube_url = "https://www.youtube.com/watch?v=MPV7JXTWPWI&ab_channel=0612TVw%2FNERDfirst"
output_path = os.path.join(os.getcwd(),'output')
download_video(youtube_url=youtube_url,output_path=output_path)

final_video_path = download_and_add_subtitles(youtube_url, output_path)

if final_video_path:
    print(f"Video with subtitles created: {final_video_path}")
else:
    print("Error occurred. Video with subtitles not created.")
