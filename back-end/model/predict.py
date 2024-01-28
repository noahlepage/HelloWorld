#!/usr/bin/env python
from keras.models import Model
from keras.layers import Flatten
from keras.applications import VGG16

from joblib import load

import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram
from scipy import signal

# save_spec
# get_person_name
# shuffle_dataset
# encode_labels
# predict_features
# convert_binary_to_numerical_encoding



# cut it into 1 second with ffmpeg (and get their shape)
# get the VGG16 transfer model
# predict the input's features
# use the saved SVM model to predict the class using the features

# clf = load('saved_model.joblib') 

# # =============================== Transfer Learning ======================== #
# vgg_model = VGG16(weights='imagenet',include_top=False, input_shape=saved_shape)

# for i,layer in enumerate(vgg_model.layers):
#   layer.trainable = False

# x = vgg_model.output
# x = Flatten(name="Flatten")(x) # Flatten dimensions to for use in FC layers
# trained_model = Model(inputs=vgg_model.input, outputs=x)
# transfer_model = Model(inputs=trained_model.input, outputs=trained_model.get_layer('Flatten').output)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

num_chunks = int(RATE / CHUNK * RECORD_SECONDS)

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()


def get_spect(sound, sr, path : str):
    fig, ax = plt.subplots(1)
    plt.axis('off')
    specgram(np.array(sound), Fs=sr)
    plt.savefig(path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    return plt.imread(path)

data = [[] for i in range(RECORD_SECONDS)]
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data[i // int(num_chunks / RECORD_SECONDS)].append(np.frombuffer(frames[i], dtype=np.int16))

data = [np.concatenate(d) for d in data]
spects = []
for i in range(len(data)):
    spects.append(get_spect(data[i], RATE, f"out{i}.jpg"))

vgg_model = VGG16(weights='imagenet',include_top=False, input_shape=(369, 496, 3))

for i,layer in enumerate(vgg_model.layers):
    layer.trainable = False

x = vgg_model.output
x = Flatten(name="Flatten")(x) # Flatten dimensions to for use in FC layers
trained_model = Model(inputs=vgg_model.input, outputs=x)
transfer_model = Model(inputs=trained_model.input, outputs=trained_model.get_layer('Flatten').output)

clf = load('saved_model.joblib') 
for s in spects[1:]:
    expanded_spect = np.expand_dims(s, axis=0)
    features = transfer_model.predict(expanded_spect)
    print(clf.predict(features))

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
