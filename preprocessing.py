import cv2
import numpy as np


def preprocess(img, params):

    if params["hist_eq"]:

        imgYuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        imgYuv[:, :, 0] = cv2.equalizeHist(imgYuv[:, :, 0])
        img = cv2.cvtColor(imgYuv, cv2.COLOR_YUV2BGR)

    if params["gaussian_blur"]:
        img = cv2.GaussianBlur(img, (3, 3), 0)

    if params["unsharp_mask"]:
        for i in range(params["unsharp_mask"]):
            img = unsharp_mask(img)

    return img


def unsharp_mask(img):
    kernel_size = (7, 7)
    gauss = cv2.GaussianBlur(img, ksize=kernel_size, sigmaX=0)
    unsharp_img = cv2.addWeighted(img, 2, gauss, -1, 0)
    return unsharp_img


if __name__ == "__main__":
    img = cv2.imread(
        "preprocessing_test_resources/carlos_carral_cortes/2020-06-24-162622.jpg")
    unsharp = unsharp_mask(img)
    unsharp2 = unsharp_mask(unsharp)
    cv2.imshow("unsharpened", unsharp2)
    cv2.waitKey()
