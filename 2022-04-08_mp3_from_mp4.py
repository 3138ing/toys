import glob
import os
import ffmpeg

#from moviepy.editor import *

mp4_dir = 'f:\\word_pie_video'
mp3_dir = 'f:\\word_pie_sound'

mp4_list = glob.glob(os.path.join(mp4_dir, '*'))
for mp4_fullpath in mp4_list:
    p, mp4_filename = os.path.split(mp4_fullpath)

    mp3_fullpath = os.path.join(mp3_dir, mp4_filename.replace('.mp4', '.mp3'))
    try:
        print('=== Try ===', mp4_fullpath)
        video = ffmpeg.input(mp4_fullpath).output(mp3_fullpath).run(cmd='C:\\Users\\xxx\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\imageio_ffmpeg\\binaries\\ffmpeg-win64-v4.2.2.exe')
    except:
        print('=== Except ===')
        None

    

print('=== END ===')
