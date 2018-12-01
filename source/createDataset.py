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

#  more fonts arial vs https://www.codesofinterest.com/2017/07/more-fonts-on-opencv.html

# fonts = [cv2.FONT_HERSHEY_COMPLEX,cv2.FONT_HERSHEY_COMPLEX_SMALL, cv2.FONT_HERSHEY_DUPLEX,cv2.FONT_HERSHEY_PLAIN,cv2.FONT_HERSHEY_SIMPLEX,cv2.FONT_HERSHEY_TRIPLEX,cv2.FONT_ITALIC]








for x  in list (string.ascii_uppercase ):
    img = np.zeros((80, 60,3), np.uint8)
    img.fill(255)
    # for a, font in zip(range(0, 9), fonts):
    #     konum = 5 + a * 45
    cv2.putText(img,x,(10,60), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0),2,cv2.LINE_AA)
    cv2.imshow("dataset",img)
    cv2.imwrite("dataset/"+x+".png",img)










# for x  in list (string.ascii_lowercase ):
#     img = np.zeros((80, 360,3), np.uint8)
#     img.fill(255)
#     for a,font in zip( range(0,9),fonts):
#         konum= 5+a*40
#         cv2.putText(img, x, (konum, 60), font, 2, (0, 0, 0), 2, cv2.LINE_AA)
#         cv2.imshow("dataset",img)
#         cv2.imwrite("dataset/"+x+"Low.png",img)
# for x  in list (string.ascii_uppercase ):
#     img = np.zeros((80, 360,3), np.uint8)
#     img.fill(255)
#     for a, font in zip(range(0, 9), fonts):
#         konum = 5 + a * 45
#         cv2.putText(img,x,(konum,60), font, 2,(0,0,0),2,cv2.LINE_AA)
#         cv2.imshow("dataset",img)
#         cv2.imwrite("dataset/"+x+"Upper.png",img)

# img = np.zeros((80, 250,3), np.uint8)
# # img.fill(255)
# # font = cv2.FONT_HERSHEY_SIMPLEX
# # cv2.putText(img,"ANKARA",(5,60), font, 2,(0,0,255),2,cv2.LINE_AA)
# # cv2.imwrite("ankara.png",img)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()