import unittest
import pipeline
import cv2
import global_config


class PipelineTest(unittest.TestCase):
    def setUp(self):
        global img_a

        f = open("resources/test_uri", "r")
        uri = f.read()
        img_a = pipeline.img_from_uri(uri)
        f.close()

        global_config.DEBUG = True

    def test_img_from_uri(self):
        with open("resources/test_uri", "r") as f:
            uri = f.read()
            img = pipeline.img_from_uri(uri)
            #  cv2.imshow('prueba1',img)
            #  cv2.waitKey(0)

        # passed
        self.assertTrue(True)

    def test_face_detector(self):
        pipeline.detect_faces(img_a)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
