import cvlib as cv

def verifyImage(image):
    #image = cv2.imread("RIDDHI_OZA.png")
    faces, confidences = cv.detect_face(image)
    if(len(faces)>1):
        return 0
    else:
        return max(confidences)