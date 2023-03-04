import cvlib as cv
import sys
import cv2
import os 
import matplotlib.pyplot as plt

image = cv2.imread("RIDDHI_OZA.png")

faces, confidences = cv.detect_face(image)

print(faces)
print(confidences)
print(type(confidences))

count=0
for face,conf in zip(faces,confidences):

    (startX,startY) = face[0],face[1]
    (endX,endY) = face[2],face[3]

    cv2.rectangle(image, (startX,startY), (endX,endY), (0,255,0), 2)
    count+=1
print("NO. OF FACES DETECTED :",count)
if(count>1):
    print("MORE THAN ONE FACE DETECTED")
    print("FACE DETECTION PROBABILITY : 0%")
else:
    print("FACE DETECTION PROBABILITY :",max(confidences)*100)
probability = max(confidences)
# cv2.imshow("face_detection", image)
plt.imshow(image)
plt.show()
cv2.imwrite("face_detection.jpg", image)
cv2.destroyAllWindows()