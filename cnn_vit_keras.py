# -*- coding: utf-8 -*-
"""3 dense of vit_keras.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19csE_TCs3wYBCCAyFtgNjIOZsmnCiUYY
"""

from google.colab import drive
import glob

drive.mount('/content/drive')

paths = glob.glob('/content/drive/MyDrive/Plant/imgaug2/*',recursive=True)
namee = [i.split("2/")[1] for i in paths]
name=[]
for i in namee:
  name.append(i)
name

from PIL import Image
import numpy as np
datas=[]
labels=[]
for i in range(len(name)):
    print(i,name[i])
    paths = glob.glob('/content/drive/MyDrive/Plant/imgaug2/'+name[i]+'*/*.jpg')
    sett =np.array([np.asarray(Image.open(img)) for img in paths])
    print(len(sett))
    for j in sett:
        datas.append(j)
        labels.append(int(i))
    print((len(datas)),len(labels))
cells = np.array(datas)
labels = np.array(labels)

np.save('Cells' , cells)
np.save('Labels' , labels)
print('Cells : {} | labels : {}'.format(cells.shape , labels.shape))

from sklearn.model_selection import train_test_split
x_train, X_test, y_train, y_test = train_test_split(cells, labels, test_size=0.2, random_state=42)

num_classes = 12

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, losses

from vit_keras import vit
IMAGE_SIZE = 224
b0_model = tf.keras.applications.efficientnet.EfficientNetB0(include_top=False, weights = 'imagenet', input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3))
for layer in b0_model.layers:
    layer.trainable = True

vit_model = vit.vit_b16(
        image_size = IMAGE_SIZE,
        activation = 'relu',
        pretrained = True,
        include_top = False,
        pretrained_top = False,
        classes = num_classes)

inputs = tf.keras.layers.Input((IMAGE_SIZE, IMAGE_SIZE, 3))
b0_output = tf.keras.layers.Flatten()(b0_model(inputs))
vit_output = vit_model(inputs)
x = tf.keras.layers.Concatenate(axis=-1)([b0_output, vit_output])
# pooling_layer = tf.keras.layers.GlobalAveragePooling2D()(x)


dropout_layer = tf.keras.layers.Dropout(0.5)(x)

outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(dropout_layer)
model = tf.keras.Model(inputs, outputs)
print(model.summary())

model.compile(optimizer="adam", loss=losses.sparse_categorical_crossentropy, metrics=['accuracy'])
history =model.fit(x_train, y_train, batch_size=64, epochs=500, validation_data=(X_test, y_test))

model.save('cnn_vit_keras.h5')