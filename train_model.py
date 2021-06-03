from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle
from global_config import *


def main():
    f = open(EMBEDDINGS_PATH, "rb")
    data = pickle.loads(f.read())
    f.close()

    # Codificar las etiquetas
    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(data["names"])

    # Entrenamiento del modelo

    recognizer = SVC(C=1.0, kernel="linear", probability=True)
    recognizer.fit(data["embeddings"], labels)

    f2 = open(RECOGNIZER_PATH, "wb")
    f2.write(pickle.dumps(recognizer))
    f2.close()

    f3 = open(LABEL_ENCODER_PATH, "wb")
    f3.write(pickle.dumps(label_encoder))
    f3.close()


if __name__ == "__main__":
    main()
