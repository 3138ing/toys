from moviepy.editor import AudioFileClip, ImageClip

audio_path = r'D:\pc\01\sync\영어CD\Ready,Action!\track\40.S_6-7.mp3'
image_path = r'D:\pc\01\sync\영어CD\Ready,Action!\my\57.S_6-7.png'
output_path = r'D:\pc\01\sync\영어CD\Ready,Action!\my\57.S_6-7.mp4'

audio_clip = AudioFileClip(audio_path)
image_clip = ImageClip(image_path)
video_clip = image_clip.set_audio(audio_clip)
video_clip.duration = audio_clip.duration
video_clip.fps = 1
video_clip.write_videofile(output_path)
