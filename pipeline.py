from option import Option
import pprint
import cv2
import numpy as np
import pandas as pd
import base64
import global_config
from w3lib.url import parse_data_uri
import matplotlib.pyplot as plt
import matplotlib.patches as patches

#https://github.com/opencv/opencv/raw/3.4.0/samples/dnn/face_detector/deploy.prototxt
PROTOTXT = "resources/deploy.prototxt"

#pre-trained weights: https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel
CAFFE_MODEL = "resources/res10_300x300_ssd_iter_140000.caffemodel"


def img_from_uri(photo_uri):
    """
    Regresa una imágen de cv codificada de un URI
    """
    parsed_uri = parse_data_uri(photo_uri)
    img_bytes = parsed_uri[2]
    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, flags=cv2.IMREAD_COLOR)
    return img


def pipeline_main(raw_img):
    pass


def detect_faces(raw_img):
    detector = cv2.dnn.readNetFromCaffe(PROTOTXT, CAFFE_MODEL)
    original_size = raw_img.shape
    target_size = (300, 300)
    resized_img = cv2.resize(raw_img, target_size)

    aspect_ratio_x = (original_size[0]/target_size[0])
    aspect_ratio_y = (original_size[1]/target_size[1])

    image_blob = cv2.dnn.blobFromImage(resized_img)

    detector.setInput(image_blob)
    detections = detector.forward()

    columns = ["img_id", "es_cara", "confianza",
               "left",  "top", "right", "bottom"]

    detections_df = pd.DataFrame(detections[0][0], columns=columns)

    detections_df = detections_df[detections_df["es_cara"] == 1]

    detections_df = detections_df[detections_df['confianza'] >= 0.90]

    detections_df['left'] = (detections_df['left'] * 300).astype(int)
    detections_df['bottom'] = (detections_df['bottom'] * 300).astype(int)
    detections_df['right'] = (detections_df['right'] * 300).astype(int)
    detections_df['top'] = (detections_df['top'] * 300).astype(int)

    if global_config.DEBUG:
        print(detections_df)

    for i, instance in detections_df.iterrows():
        left = instance["left"]
        right = instance["right"]
        bottom = instance["bottom"]
        top = instance["top"]
        #  print("l:{},r:{},t:{},b:{}".format(left, right, top, bottom))

        height = bottom - top
        width = right - left

        print("w:{},h:{}".format(width, height))

        rect = patches.Rectangle(
            (left, bottom), width, height, linewidth=1, edgecolor='r', facecolor='none')

        fig, ax = plt.subplots()

        ax.imshow(raw_img)
        ax.add_patch(rect)

        #  detected_face = raw_img[int(top*aspect_ratio_y):int(
        #  bottom*aspect_ratio_y), int(left*aspect_ratio_x):int(right*aspect_ratio_x)]

        #  pprint.pprint(detected_face)
        #  plt.imshow(detected_face[:, :, ::-1])
        plt.show()
