from option import Option
import imutils
import pprint
import cv2
import numpy as np
import pandas as pd
import base64
import global_config as cfg
from w3lib.url import parse_data_uri
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import pickle

#https://github.com/opencv/opencv/raw/3.4.0/samples/dnn/face_detector/deploy.prototxt
#  PROTOTXT = "resources/deploy.prototxt"

#pre-trained weights: https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel
#  CAFFE_MODEL = "resources/res10_300x300_ssd_iter_140000.caffemodel"


def img_from_uri(photo_uri):
    """
    Regresa una imágen de cv codificada de un URI
    """
    parsed_uri = parse_data_uri(photo_uri)
    img_bytes = parsed_uri[2]
    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, flags=cv2.IMREAD_COLOR)
    return img


def recognize(img):

    prototype_path = cfg.DETECTOR_PATH
    model_path = cfg.CAFFE_MODEL

    detector = cv2.dnn.readNetFromCaffe(prototype_path, model_path)

    embedder_path = cfg.EMBEDDER_PATH
    embedder = cv2.dnn.readNetFromTorch(embedder_path)

    label_encoderer_path = cfg.LABEL_ENCODER_PATH
    recognizer_path = cfg.RECOGNIZER_PATH

    f1 = open(label_encoderer_path, "rb")
    f2 = open(recognizer_path, "rb")

    label_encoder = pickle.loads(f1.read())
    recognizer = pickle.loads(f2.read())

    f1.close()
    f2.close()

    image = imutils.resize(img, width=600)
    (h, w) = image.shape[:2]

    image_blob = cv2.dnn.blobFromImage(cv2.resize(
        image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=False, crop=False)

    # Detectar rostros en la imagen
    detector.setInput(image_blob)
    detections = detector.forward()

    for i in range(detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence > cfg.CONFIANZA_DETECTOR:

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            face = image[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]

            # ensure the face width and height are sufficiently large
            if fW < 20 or fH < 20:
                continue

            faceBlob = cv2.dnn.blobFromImage(
                face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()

            # perform classification to recognize the face
            preds = recognizer.predict_proba(vec)[0]
            j = np.argmax(preds)
            proba = preds[j]
            name = label_encoder.classes_[j]

            if cfg.DEBUG:
                # draw the bounding box of the face along with the associated
                # probability
                text = "{}: {:.2f}%".format(name, proba * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(image, (startX, startY), (endX, endY),
                              (0, 0, 255), 2)
                cv2.putText(image, text, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

                # show the output image
                cv2.imshow("Image", image)
                cv2.waitKey(0)

            return name
