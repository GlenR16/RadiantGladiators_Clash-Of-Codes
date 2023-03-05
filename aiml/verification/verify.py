import cvlib as cv
import cv2
import numpy

def verifyImage(image):
    img = cv2.imdecode(numpy.fromstring(image.file.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    faces, confidences = cv.detect_face(img)
    if(len(faces)>1):
        return 0
    else:
        return max(confidences)

