from option import Option
import cv2
import numpy as np
import base64
from w3lib.url import parse_data_uri

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




def pipeline_main(img_bytes):
    img = np.frombuffer(img_bytes, dtype=np.uint8)

#  def has_face(img) -> Option[(int,int)]:
    #  detector = cv2.dnn.readNetFromCaffe(PROTOTXT, CAFFE_MODEL)

