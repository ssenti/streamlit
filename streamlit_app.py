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
import glob

st.title("Random Rap Filler Generator")

#word list generator
lyrics = "To all the ladies in the place with style and grace"

word_list = lyrics.split()

for i in range(len(word_list)):
    word_list[i] = word_list[i].lower()

for i in word_list:
    gtts.gTTS(i).save("sounds/{}.mp3".format(i))
def play_sound():
    r = random.choice(word_list)
    playsound("sounds/{}.mp3".format(r))

def dont_play_sound():
    pass

def extract_beat(filename):
    audio_data = 'songs/{}'.format(filename)
    x , sr = librosa.load(audio_data)

    x, sr = librosa.load(audio_data)
    tempo, beat_frames = librosa.beat.beat_track(y=x, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    beat_intervals = []
    for i in range(len(beat_times)-1):
        beat_intervals.append(beat_times[i+1]-beat_times[i])
    beat_intervals.insert(0, beat_times[0])

    return beat_intervals


ratio = 100-st.slider('How often should we fill the rap?', 0, 100, 25)

song_names = []
for filename in glob.glob('songs/*.wav'):
    song_names.append(filename.split('/', 1)[1])

song = st.radio(
     "Which song should we play?",
     tuple(song_names))

#st.write("Song Loading..")

filename = song
beat_intervals = extract_beat(filename)


if st.button('Play'):

    p = vlc.MediaPlayer('songs/{}'.format(filename))
    p.play()

    count = 0
    for i in beat_intervals:
        time.sleep(i)
        ans = 'Yes'
        ans = st.radio("Keep Playing?",('Yes', 'No'), key=count)
        if ans == 'No':
            p.stop()
            break
        else:
            if count == 0:
                play_sound()
                count = 1
            else:
                options = ['dont_play_sound()', 'play_sound()']
                eval(random.choices(options, weights = (ratio, 100-ratio))[0])
