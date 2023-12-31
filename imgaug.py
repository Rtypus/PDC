# -*- coding: utf-8 -*-
"""imgaug_cannavit.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16H_t-hcACvjRDm2Tkxme_WP0GblGRw9V
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import glob
import datetime
import random
from tqdm.notebook import tqdm
from PIL import Image
from PIL import ImageEnhance

from google.colab import drive
drive.mount('/content/drive')

inp = glob.glob('/content/drive/MyDrive/Plant/New/*',recursive=True)
len(inp)

contrastList = [0.25,0.5,1,2]
def augContrast(im):
  contrastImg=[]
  for img in im:
    for contrast in contrastList:
      contrastImg.append(np.asarray(ImageEnhance.Contrast(Image.fromarray(img, 'RGB')).enhance(contrast)))
  return(contrastImg)

brightnessList = [-3,-2,-1,1,2,3]
def augBrightness(im):
  brightnessImg=[]
  for img in im:
    for brightness in brightnessList:
      brightnessImg.append(np.asarray(ImageEnhance.Brightness(Image.fromarray(img, 'RGB')).enhance(brightness)))
  return(brightnessImg)

sharpnessList = [-5,-3,-1,1,3,-5]
def augSharpness(im):
  sharpnessImg=[]
  for img in im:
    for sharpness in sharpnessList:
      sharpnessImg.append(np.asarray(ImageEnhance.Sharpness(Image.fromarray(img, 'RGB')).enhance(sharpness)))
  return(sharpnessImg)

ColorList = [-2,-1,1,2]
def augColor(im):
  colorImg=[]
  for img in im:
    for Color in ColorList:
      colorImg.append(np.asarray(ImageEnhance.Color(Image.fromarray(img, 'RGB')).enhance(Color)))
  return(colorImg)

# import torchvision.transforms as transforms
# def jitter(img, b=0.2, c=0.2, s=0.2, h=0.1):
#     img = Image.fromarray(img)
#     transform = transforms.ColorJitter(
#     brightness=b, contrast=c, saturation=s, hue=h)
#     img = transform(img)
#     return img

import os
for i in range(len(inp)):
  name = inp[i].split("w/")[1]
  print(name)
  paths = glob.glob('/content/drive/MyDrive/Plant/New/'+str(name)+'*/*.jpg',recursive=True)
  origg= np.array([np.asarray(Image.open(img)) for img in paths])
  orig=[]
  for i in origg:
    image_array = Image.fromarray(i , 'RGB')
    resize_img = image_array.resize((224 , 224))
    orig.append(np.array(resize_img))
  print(len(orig))
  contrastImg = augContrast(orig)
  sharpnessImg = augSharpness(orig)
  colorImg = augColor(orig)
  brightnessImg =  augContrast(orig)
  allImg =  contrastImg+colorImg+sharpnessImg+brightnessImg


  new=[]
  for img in allImg:
    new.append(Image.fromarray(img, 'RGB'))
    rows,cols,channels= img.shape
    rotate_45 = cv2.warpAffine(img, cv2.getRotationMatrix2D((cols/2,rows/2),-45,1),(cols,rows))
    rotate_90 = cv2.warpAffine(img, cv2.getRotationMatrix2D((cols/2,rows/2),-90,1),(cols,rows))
    new.append(Image.fromarray(cv2.flip(img,1), 'RGB'))
    new.append(Image.fromarray(rotate_45, 'RGB'))
    new.append(Image.fromarray(rotate_90, 'RGB'))
  # plt.figure(figsize=(15,15))
  # i = 0
  # for img in new[:100]:
  #   plt.subplot(10, 10, i+1)
  #   plt.xticks([])
  #   plt.yticks([])
  #   plt.grid(False)
  #   plt.imshow(img)
  #   i += 1
  # plt.show()
  print(len(new))
  for i, image in tqdm(enumerate(new)):
    directory = '/content/drive/MyDrive/Plant/cnnavit/Train/'+str(name)+'/'

    os.makedirs(directory, exist_ok = True)
    image.save(directory + str(i)+str('.jpg'))