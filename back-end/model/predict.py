#!/usr/bin/env python
from keras.models import Model
from keras.layers import Flatten
from keras.applications import VGG16

from joblib import load

import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.pyplot import specgram

import threading

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
matplotlib.use("agg")

def get_spect(sound, sr, path : str):
    fig, ax = plt.subplots(1)
    plt.axis('off')
    specgram(np.array(sound), Fs=sr)
    plt.savefig(path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    return plt.imread(path)

def predict(name, data, transfer_model, clf):
    # th = threading.current_thread()
    # data = np.frombuffer(buf, dtype=np.int16)
    data = np.concatenate(data)
    spect = get_spect(data, RATE, f"./temp/{name}.jpg")
    expanded_spect = np.expand_dims(spect, axis=0)
    features = transfer_model.predict(expanded_spect)
    print(f"Prediction for {name}: " + str(clf.predict(features)[0]))


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

vgg_model = VGG16(weights='imagenet',include_top=False, input_shape=(369, 496, 3))

for i,layer in enumerate(vgg_model.layers):
    layer.trainable = False

x = vgg_model.output
x = Flatten(name="Flatten")(x) # Flatten dimensions to for use in FC layers
trained_model = Model(inputs=vgg_model.input, outputs=x)
transfer_model = Model(inputs=trained_model.input, outputs=trained_model.get_layer('Flatten').output)
clf = load('saved_model.joblib') 


p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []
np_frames = []
chunks_per_second = int(RATE / CHUNK)

threads = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    curr_sec = i // chunks_per_second 
    
    data = stream.read(CHUNK)
    frames.append(data)
    
    np_frames.append(np.frombuffer(data, dtype=np.int16))
    if i % chunks_per_second == 0 and curr_sec > 1:
        data = np.copy(np_frames[(curr_sec - 1) * chunks_per_second : curr_sec * chunks_per_second])
        if curr_sec == 2:
            print(len(np_frames[(2 - 1) * chunks_per_second : 2 * chunks_per_second]))
        th = threading.Thread(target=predict, \
                              args=(curr_sec, data, transfer_model, clf), \
                                daemon=True)  
        threads.append(th)
        th.start()

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

for th in threads:
    th.join()