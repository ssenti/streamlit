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
import matplotlib.pyplot as plt
import librosa.display

st.title("Rap Generator")

#word list generator
#lyrics = "yeah ay braww whatsup hello nice letsgo"
#lyrics.split()
lyrics = st.text_area("Write your lyrics here")
punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
for ele in lyrics:
    if ele in punc:
        lyrics = lyrics.replace(ele, "")

word_list = [y for y in (x.strip() for x in lyrics.splitlines()) if y]

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

    return [beat_intervals, x, sr, beat_times]


ratio = 100-st.slider('How often should we rap?', 0, 100, 25)

song_names = []
for filename in glob.glob('songs/*.wav'):
    song_names.append(filename.split('/', 1)[1].split('.', 1)[0])

song = st.radio(
     "Which instrumental should we play?",
     tuple([i.capitalize() for i in song_names]))


#ans = st.radio("Keep Playing?",('Yes', 'No'), key=count)

filename = song

extract_beat_output = extract_beat(filename+"{}".format('.wav'))

beat_intervals = extract_beat_output[0]
x = extract_beat_output[1]
sr = extract_beat_output[2]
beat_times = extract_beat_output[3]

fig1 = plt.figure(figsize=(14, 5))
librosa.display.waveshow(x, sr=sr)
plt.title("Audio Amplitude of {}".format(filename.capitalize()))
plt.xlabel("Time")
plt.ylabel("Amplitude")
st.pyplot(fig1)

X = librosa.stft(x)
Xdb = librosa.amplitude_to_db(abs(X))
fig2 = plt.figure(figsize=(14, 5))
librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
#plt.colorbar()
plt.title("Spectrogram of {}".format(filename.capitalize()))
st.pyplot(fig2)

if st.button('Play'):
    p = vlc.MediaPlayer('songs/{}'.format(filename+"{}".format('.wav')))
    p.play()
    count = 0
    for i in beat_intervals:
        ii = beat_intervals.index(i)
        time.sleep(i)
        if count == 0:
            play_sound()
            #plt.vlines(x=beat_times[ii], ymin=0, ymax=1, linewidth=0.5, color='green',label='Beat Mark')
            #plt.legend()
        if count > 30:
            p.stop()
            break
        else:
            options = ['dont_play_sound()', 'play_sound()']
            eval(random.choices(options, weights = (ratio, 100-ratio))[0])
            #choice
            #if str(choice) == options[1]:
                #plt.vlines(x=beat_times[ii], ymin=0, ymax=1, linewidth=0.5, color='green',label='Beat Mark')
        count += 1
    p.stop()
