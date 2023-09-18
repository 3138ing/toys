import speech_recognition as sr
from gtts import gTTS
import random
import os, time
import datetime
import playsound
import threading
import ctypes

#paths = ['./01.txt', './02.txt', './03.txt', './04.txt','./05.txt', './06.txt', './07.txt', './08.txt', './09.txt', './10.txt']
#paths = ['./T원.txt']
#paths = ['./T웅.txt']
paths = ['./10.txt','./09.txt','./08.txt']



last_time = None
keep_thread = True
current_key = None
is_speaking = False

def dura_time():
    if last_time == None:
        return datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    now = datetime.datetime.now() - last_time
    return str(now).split(".")[0]

def get_time():
    return datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

def show_time():
    global keep_thread
    global current_key
    while keep_thread:
        text = dura_time()
        ctypes.windll.kernel32.SetConsoleTitleW(text)
        #if text.find('/') == -1 and int(text[-2:])//10 == 0:
        if text.find('/') == -1 and int(text[-2:]) != 0 and int(text[-2:])%15 == 0:
            speak(current_key)
        time.sleep(1)

def speak(text):
    global is_speaking
    if is_speaking:
        return
    is_speaking = True
    tts = gTTS(text='listen,' + text + ',' + text + ',' + text, slow=True, lang='en')
    filename='temp.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)
    is_speaking = False

def make_dic(lines):
    dic = {}
    for index, line in enumerate(lines):
        line = line.decode().strip()
        if len(line) == 0:
            continue
        splits = line.split('\t')
        if splits[0] in dic:
            print('### [INFO: Duplicated word]', splits[0])
        dic[splits[0]] = splits[1]
    return dic
    
def read_file(path):
    with open(path, 'rb') as f:
        lines = f.readlines()
    line_number = 0
    for line in lines:
        line_number += 1
        line = line.strip()
        if len(line) == 0:
            continue
        splits = line.split(b'\t')
        if len(splits) != 2:
            print('### [ERROR: Split]', f'{path}:{line_number}', line)
            return None

    return lines

def main_function():
    # read lines
    all_lines = []
    for path in paths:
        lines = read_file(path)
        if lines == None:
            return
        if len(lines) != 100:
            print('### [INFO: LINE COUNT]', len(lines))
        all_lines.extend(lines)

    # make dic
    dic = make_dic(all_lines)
    if dic == None:
        print('### [ERROR: dic is None]')
        return
    if len(dic) != len(paths) * 100:
        print('### [INFO: WORD COUNT]', len(dic))

    # suffle dic
    l = list(dic.items())
    random.shuffle(l)
    dic = dict(l)
    
    # start test
    global last_time
    global current_key
    for index, key in enumerate(dic):
        current_key = key
        last_time = None
        input('# [ROUND ' + str(index + 1) + ']    ===>    press enter key\n')
        print()
        print(get_time(), key + '    ===>    ?\n')
        last_time = datetime.datetime.now()
        speak(key)
        while True:
            c = input('[a]gain [n]ext [q]uit\n\n')
            print('')
            if c =='a':
                speak(key)
            elif c =='n':
                break
            elif c =='o':
                break
            elif c =='x':
                break
            elif c =='q':
                exit(0)
        print(get_time(), key + '    ===>    ' + dic[key] + '\n')

try:
    thread = threading.Thread(target=show_time)
    thread.start()
    main_function()
finally:
    keep_thread = False
