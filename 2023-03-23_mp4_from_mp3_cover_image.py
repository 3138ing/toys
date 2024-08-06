import sys
sys.path.insert(0, '../toys-data')
import conf

from moviepy.editor import AudioFileClip, ImageClip

audio_path = conf.READY_ACTION_AUDIO_PATH
image_path = conf.READY_ACTION_IMAGE_PATH
output_path = conf.READY_ACTION_OUTPUT_PATH

audio_clip = AudioFileClip(audio_path)
image_clip = ImageClip(image_path)
video_clip = image_clip.set_audio(audio_clip)
video_clip.duration = audio_clip.duration
video_clip.fps = 1
video_clip.write_videofile(output_path)
