import sys
sys.path.insert(0, '../toys-data')
import conf

import glob
import os
import ffmpeg

#from moviepy.editor import *

mp4_dir = conf.WORDPIE_MP4_DIR
mp3_dir = conf.WORDPIE_MP3_DIR

mp4_list = glob.glob(os.path.join(mp4_dir, '*'))
for mp4_fullpath in mp4_list:
    p, mp4_filename = os.path.split(mp4_fullpath)

    mp3_fullpath = os.path.join(mp3_dir, mp4_filename.replace('.mp4', '.mp3'))
    try:
        print('=== Try ===', mp4_fullpath)
        video = ffmpeg.input(mp4_fullpath).output(mp3_fullpath).run(cmd=conf.FFMPEG_EXE_PATH)
    except:
        print('=== Except ===')
        None

    

print('=== END ===')
