"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st


import librosa
import gtts
from playsound import playsound
import random
import vlc
import time

#choose file
filename = 'firefly_inst'

#extract_beat(filename)
#def extract_beat(filename):
audio_data = '{}.wav'.format(filename)
x , sr = librosa.load(audio_data)

# load the audio as a waveform `y`, store the sampling rate as `sr`
# run the default beat tracker
# convert the frame indices of beat events into timestamps
x, sr = librosa.load(audio_data)
tempo, beat_frames = librosa.beat.beat_track(y=x, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

beat_intervals = []
for i in range(len(beat_times)-1):
    beat_intervals.append(beat_times[i+1]-beat_times[i])
beat_intervals.insert(0, beat_times[0])

#beat_times
#beat_intervals
#print(type(x), type(sr))
#print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

def play_sound():
    r = random.choice(word_list)
    playsound("sounds/{}.mp3".format(r))

def dont_play_sound():
    pass


#word list generator
lyrics = "To all the ladies in the place with style and grace"

word_list = lyrics.split()

for i in range(len(word_list)):
    word_list[i] = word_list[i].lower()

for i in word_list:
    gtts.gTTS(i).save("sounds/{}.mp3".format(i))





ratio = 50

p = vlc.MediaPlayer('{}.wav'.format(filename))
p.play()

if st.checkbox('Stop'):
    p.stop()

count = 0
for i in beat_intervals:
    time.sleep(i)
    if count == 0:
        play_sound()
        count = 1
    else:
        options = ['dont_play_sound()', 'play_sound()']
        eval(random.choices(options, weights = (ratio, 100-ratio))[0])
