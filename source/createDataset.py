import cv2
import numpy as np
import string


# FONT_HERSHEY_COMPLEX
# FONT_HERSHEY_COMPLEX_SMALL
# FONT_HERSHEY_DUPLEX
# FONT_HERSHEY_PLAIN
# FONT_HERSHEY_SCRIPT_COMPLEX
# FONT_HERSHEY_SCRIPT_SIMPLEX
# FONT_HERSHEY_SIMPLEX
# FONT_HERSHEY_TRIPLEX
# FONT_ITALIC
fonts = [cv2.FONT_HERSHEY_COMPLEX,cv2.FONT_HERSHEY_COMPLEX_SMALL, cv2.FONT_HERSHEY_DUPLEX,cv2.FONT_HERSHEY_PLAIN,cv2.FONT_HERSHEY_SIMPLEX,cv2.FONT_HERSHEY_TRIPLEX,cv2.FONT_ITALIC]

for x  in list (string.ascii_lowercase ):
    img = np.zeros((60, 400,3), np.uint8)
    img.fill(255)
    for a,font in zip( range(0,9),fonts):
        konum= 5+a*40
        cv2.putText(img, x, (konum, 45), font, 2, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow("dataset",img)
        cv2.imwrite("dataset/"+x+"Low.png",img)
for x  in list (string.ascii_uppercase ):
    img = np.zeros((60, 400,3), np.uint8)
    img.fill(255)
    for a, font in zip(range(0, 9), fonts):
        konum = 5 + a * 45
        cv2.putText(img,x,(konum,45), font, 2,(0,0,0),2,cv2.LINE_AA)
        cv2.imshow("dataset",img)
        cv2.imwrite("dataset/"+x+"Upper.png",img)

# img = np.zeros((60, 250,3), np.uint8)
# img.fill(255)
# font = cv2.FONT_HERSHEY_SIMPLEX
# cv2.putText(img,"ANKARA",(5,45), font, 2,(0,0,0),2,cv2.LINE_AA)
# cv2.imwrite("ankara.png",img)
cv2.waitKey(0)
cv2.destroyAllWindows()