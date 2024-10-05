import cv2
import numpy as np

class ImageStitcher:
    def __init__(self):
        self.stitcher = cv2.Stitcher_create()

    def stitch(self, images):
        (status, stitched) = self.stitcher.stitch(images)
        if status == cv2.Stitcher_OK:
            return stitched
        else:
            raise Exception("Image stitching failed with status {}".format(status))
