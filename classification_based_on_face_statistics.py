# -*- coding: utf-8 -*-
"""Classification Based on Face Statistics

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zNOBo3S_ZdqLutVGuE6Cq24IMHjLIoiq
"""

!pip install opencv-python --upgrade mediapipe

import cv2
import mediapipe as mp

from PIL import Image
import numpy as np
import pandas as pd

from scipy import stats

import copy

import math
import os

import colorsys
from google.colab.patches import cv2_imshow

def calculate_head_pose(landmarks_3d ):
    # Extracting individual landmarks for better readability
    nose_tip = landmarks_3d[2]  # assuming the nose tip is at index 33
    left_eye = landmarks_3d[130]  # assuming left eye corner is at index 36
    right_eye = landmarks_3d[359]


    vector1 = np.array([right_eye.x, right_eye.y, right_eye.z])
    vector2 = np.array([left_eye.x, left_eye.y, left_eye.z])
    eye_vector = vector1 - vector2
    eye_yaw = np.degrees(np.arctan2(eye_vector[1], eye_vector[0]))
    eye_pitch = np.degrees(np.arctan2(-eye_vector[2], np.linalg.norm(eye_vector[:2])))

    # For demonstration purposes, assuming the head is positioned at the nose tip
    head_vector = [nose_tip.x, nose_tip.y,nose_tip.z]

    # Calculate head yaw, roll, and pitch
    head_yaw = np.degrees(np.arctan2(head_vector[0], head_vector[2]))
    head_roll = np.degrees(np.arctan2(head_vector[1], head_vector[2]))
    head_pitch = np.degrees(np.arctan2(-head_vector[0], np.linalg.norm(head_vector[1:])))

    return eye_yaw, eye_pitch, head_yaw, head_roll, head_pitch

dataset=[]

!unzip -q '/content/Happy.zip' -d 'happy'
!unzip -q '/content/Sad.zip' -d 'sad'

count=0
for file in os.listdir('/content/sad/Sad'):

  mp_drawing = mp.solutions.drawing_utils
  mp_drawing_styles = mp.solutions.drawing_styles
  mp_face_mesh = mp.solutions.face_mesh
  PATH = '/content/sad/Sad/'
  original_image = Image.open(PATH + file)
  new_size = (300, 300)
  resized_image = original_image.resize(new_size)
  resized_image.save(PATH + file)
  print(resized_image.size)
  # image = cv2.imread("img.jpg")
  # drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
  with mp_face_mesh.FaceMesh(
      static_image_mode=True,
      max_num_faces=1,
      refine_landmarks=True,
      min_detection_confidence=0.5) as face_mesh:
      image = cv2.imread(PATH + file)
      results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
      annotated_image = image.copy()
  try:
    a,b,c,d,e = calculate_head_pose(results.multi_face_landmarks[0].landmark)
    dataset.append([a,b,c,d,e])
    count+=1
  except:
    continue

file = '/content/img.jpg'
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
PATH = '/content/sad/Sad/'
original_image = Image.open(file)
new_size = (300, 300)
resized_image = original_image.resize(new_size)
resized_image.save(file)
print(resized_image.size)
# image = cv2.imread("img.jpg")
# drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5) as face_mesh:
    image = cv2.imread(file)
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    annotated_image = image.copy()
a,b,c,d,e = calculate_head_pose(results.multi_face_landmarks[0].landmark)
# dataset.append([a,b,c,d,e])

dataset=[]
dataset.append([a,b,c,d,e])

len(dataset)

labels = [1 for x in range(2907)] + [0 for y in range(1792)]

len(labels)

type(dataset)

columns = ["A", "B", "C", "D", "E"]
data = pd.DataFrame(dataset, columns = columns)
data['label'] = labels

columns = ["A", "B", "C", "D", "E"]
data = pd.DataFrame(dataset, columns = columns)

from sklearn.model_selection import train_test_split
y = data.pop('label')
X = data

from sklearn.metrics import log_loss

Xt, Xv, yt, yv = train_test_split(X,y, test_size=0.2)

import xgboost as xgb
import lightgbm as lgbm
model = xgb.XGBClassifier()
model2 = lgbm.LGBMClassifier()
#model2.fit(Xt, yt)
model.fit(Xt, yt)
preds = model.predict_proba(Xv)
#preds2 = model.predict_proba(Xv)
log_loss(yv, preds)

model.predict_proba(data)

p = model.predict(Xv)

import pickle

with open('headStats.pkl', 'wb') as file:
    pickle.dump(model, file)