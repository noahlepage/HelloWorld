#!/usr/bin/env python
from keras.models import Model
from keras.layers import Flatten
from keras.applications import VGG16

from joblib import load

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

clf = load('saved_model.joblib') 

# =============================== Transfer Learning ======================== #
vgg_model = VGG16(weights='imagenet',include_top=False, input_shape=saved_shape)

for i,layer in enumerate(vgg_model.layers):
  layer.trainable = False

x = vgg_model.output
x = Flatten(name="Flatten")(x) # Flatten dimensions to for use in FC layers
trained_model = Model(inputs=vgg_model.input, outputs=x)
transfer_model = Model(inputs=trained_model.input, outputs=trained_model.get_layer('Flatten').output)