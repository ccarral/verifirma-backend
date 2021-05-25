from imutils import paths
from global_config import *
import numpy as np
import argparse
import imutils
import argparse
import cv2
import pickle
import os


prototype_path = DETECTOR_PATH
model_path = CAFFE_MODEL

embedder_path = EMBEDDER_PATH

detector = cv2.dnn.readNetFromCaffe(prototype_path, model_path)
embedder = cv2.dnn.readNetFromTorch(embedder_path)

# Enlistar las clases de nuestros datos de prueba

# Nombres conocidos
known_names = []

known_embeddings = []

image_paths = list(paths.list_images(TRAINING_SET))

# Número de caras procesadas
total = 0

# iterar sobre los paths

for (i, im_path) in enumerate(image_paths):
    name = im_path.split(os.path.sep)[-2]

    image = cv2.imread(im_path)
    image = imutils.resize(image, width=600)
    (h, w) = image.shape[:2]

    image_blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 1.0, (300, 300),
        (104.0, 177.0, 123.0), swapRB=False, crop=False)

    detector.setInput(image_blob)
    detections = detector.forward()

    total += 1
    print("Procesando foto {} [{} | detectados:{}]".format(
        total, name, len(detections)))

    if len(detections) > 0:

        i = np.argmax(detections[0, 0, :, 2])
        confidence = detections[0, 0, i, 2]

        if confidence > CONFIANZA_DETECTOR:
            # compute the (x, y)-coordinates of the bounding box for
            # the face
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            # extract the face ROI and grab the ROI dimensions
            face = image[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]
            # ensure the face width and height are sufficiently large
            if fW < 20 or fH < 20:
                continue

            face_blob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                                              (96, 96), (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(face_blob)
            vec = embedder.forward()
            # add the name of the person + corresponding face
            # embedding to their respective lists
            known_names.append(name)
            known_embeddings.append(vec.flatten())

data = {"embeddings": known_embeddings, "names": known_names}

output_embeddings_path = EMBEDDINGS_PATH

with open(output_embeddings_path, "wb") as f:
    f.write(pickle.dumps(data))
