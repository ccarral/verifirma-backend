import pandas as pd
import global_config
import extract_embeddings
import train_model
import numpy as np
import pipeline
import preprocessing
from imutils import paths
import os
import cv2

#  Debería de generar una tabla de la forma
#  img_path | etiqueta_detectada | etiqueta_esperada | correcto


def generate_data_frame(config):
    image_paths = list(paths.list_images("preprocessing_test_resources"))

    normalized_image_paths = []
    expected_labels = []
    detected_labels = []
    correct_list = []

    for p in image_paths:
        expected = p.split(os.path.sep)[-2]

        expected_labels.append(expected)

        img_path = p.split(os.path.sep)[-1]

        normalized_image_paths.append(img_path)

        img = cv2.imread(p)

        img = preprocessing.preprocess(img, config)

        detected = pipeline.recognize(img)

        detected_labels.append(detected)

        correct = expected == detected

        correct_list.append(correct)

    data_frame = pd.DataFrame(
        data={"img": normalized_image_paths, "etiqueta_esperada": expected_labels, "etiqueta_detectada": detected_labels, "correcto": correct_list})

    return data_frame


def main():

    global_config.DEBUG = False

    configs = [
        ("Sin preprocesamiento", {
         "gaussian_blur": False, "hist_eq": False, "unsharp_mask": False}),
        ("Con equalización del histograma", {
         "gaussian_blur": False, "hist_eq": True, "unsharp_mask": False}),
        ("Con unsharp mask", {
         "gaussian_blur": False, "hist_eq": False, "unsharp_mask": 1}),
        ("Con doble unsharp mask", {
         "gaussian_blur": False, "hist_eq": False, "unsharp_mask": 2}),
        ("Con unsharp mask y ecualización", {
         "gaussian_blur": False, "hist_eq": True, "unsharp_mask": 1}),
    ]

    for legend, cfg in configs:

        extract_embeddings.main(cfg)
        train_model.main()

        df = generate_data_frame(cfg)

        correct = df.correcto.sum()
        total = len(df.index)

        pctg = (correct/total)*100

        print(legend)
        print("---------------------------------")
        print(df)

        print("\n")
        print("Aciertos: [{}/{}]".format(correct, total))
        print("Efectividad: {}%".format(pctg))
        print("\n\n")


if __name__ == "__main__":
    main()
