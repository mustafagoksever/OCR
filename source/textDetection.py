# import os,sys
# import numpy as np
# import cv2
#
# # author: qzane@live.com
# # reference: http://stackoverflow.com/a/23565051
# # further reading: http://docs.opencv.org/master/da/d56/group__text__detect.html#gsc.tab=0
# def text_detect(img,ele_size=(8,2)): #
#     if len(img.shape)==3:
#         img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#     img_sobel = cv2.Sobel(img,cv2.CV_8U,1,0)#same as default,None,3,1,0,cv2.BORDER_DEFAULT)
#     img_threshold = cv2.threshold(img_sobel,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)
#     element = cv2.getStructuringElement(cv2.MORPH_RECT,ele_size)
#     img_threshold = cv2.morphologyEx(img_threshold[1],cv2.MORPH_CLOSE,element)
#     contours = cv2.findContours(img_threshold,0,1)
#     Rect = [cv2.boundingRect(i) for i in contours[1] if i.shape[0]>100]
#     RectP = [(int(i[0]-i[2]*0.08),int(i[1]-i[3]*0.08),int(i[0]+i[2]*1.1),int(i[1]+i[3]*1.1)) for i in Rect]
#     return RectP
#
#
# def main():
#     inputFile = "C:/Users/Mustafa/Desktop/bitirme/OCR/source/textDetection.png"
#     outputFile = inputFile.split('.')[0]+'-rect.'+'.'.join(inputFile.split('.')[1:])
#     print(outputFile)
#     img = cv2.imread("C:/Users/Mustafa/Desktop/bitirme/OCR/source/b.jpg")
#     rect = text_detect(img)
#     for i in rect:
#         cv2.rectangle(img,i[:2],i[2:],(0,0,255))
#     cv2.imwrite("a.jpg", img)
#
# if __name__ == '__main__':
#     main()



import sys
import os

import cv2
import numpy as np




img = cv2.imread("C:/Users/Mustafa/Desktop/bitirme/OCR/source/printable.jpg")
# for visualization
vis = cv2.imread("C:/Users/Mustafa/Desktop/bitirme/OCR/source/printable.jpg")


# Extract channels to be processed individually
channels = cv2.text.computeNMChannels(img)
# Append negative channels to detect ER- (bright regions over dark background)
cn = len(channels)-1
for c in range(0,cn):
  channels.append((255-channels[c]))

# Apply the default cascade classifier to each independent channel (could be done in parallel)
print("Extracting Class Specific Extremal Regions from "+str(len(channels))+" channels ...")
print("    (...) this may take a while (...)")
for channel in channels:

  erc1 = cv2.text.loadClassifierNM1("C:/Users/Mustafa/Desktop/bitirme/OCR/source/printable.jpg"+'/trained_classifierNM1.xml')
  er1 = cv2.text.createERFilterNM1(erc1,16,0.00015,0.13,0.2,True,0.1)

  erc2 = cv2.text.loadClassifierNM2("C:/Users/Mustafa/Desktop/bitirme/OCR/source/printable.jpg"+'/trained_classifierNM2.xml')
  er2 = cv2.text.createERFilterNM2(erc2,0.5)

  regions = cv2.text.detectRegions(channel,er1,er2)

  rects = cv2.text.erGrouping(img,channel,[r.tolist() for r in regions])
  #rects = cv.text.erGrouping(img,channel,[x.tolist() for x in regions], cv.text.ERGROUPING_ORIENTATION_ANY,'../../GSoC2014/opencv_contrib/modules/text/samples/trained_classifier_erGrouping.xml',0.5)

  #Visualization
  for r in range(0,np.shape(rects)[0]):
    rect = rects[r]
    cv2.rectangle(vis, (rect[0],rect[1]), (rect[0]+rect[2],rect[1]+rect[3]), (0, 0, 0), 2)
    cv2.rectangle(vis, (rect[0],rect[1]), (rect[0]+rect[2],rect[1]+rect[3]), (255, 255, 255), 1)


#Visualization
cv2.imshow("Text detection result", vis)
cv2.waitKey(0)