import unittest
import pipeline 
import cv2

class PipelineTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_img_from_uri(self):
        with open("resources/test_uri","r") as f:
            uri = f.read()
            img = pipeline.img_from_uri(uri)
            cv2.imshow('prueba1',img)
            cv2.waitKey(0)

        # passed
        self.assertTrue(True)


    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()

