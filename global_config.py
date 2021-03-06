DEBUG = True
DETECTOR_PATH = "resources/deploy.prototxt"
CAFFE_MODEL = "resources/res10_300x300_ssd_iter_140000.caffemodel"
CONFIANZA_DETECTOR = 0.90
EMBEDDER_PATH = "resources/openface.nn4.small2.v1.t7"
TRAINING_SET = "training_data"
EMBEDDINGS_PATH = "output/embeddings.pickle"
RECOGNIZER_PATH = "output/recognizer.pickle"
LABEL_ENCODER_PATH = "output/label_encoder.pickle"
OUTPUT_DIR = "output"
DATABASE = "users.db"
PREPROCESSING_CONFIG = {
    "gaussian_blur": False,
    "hist_eq": False,
    "unsharp_mask": False
}
