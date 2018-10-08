import cv2
import numpy as np

img1=cv2.imread('resim.jpg')
img2=cv2.imread('logo.jpg')

toplam=cv2.add(img2,img1)

cv2.imshow('toplam',toplam)
cv2.waitKey(0)
cv2.destroyAllWindows()