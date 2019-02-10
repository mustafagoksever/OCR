
import numpy as np
import cv2
import urllib.request
import ssl

def takeAPhotoFromPhoneCamere():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = 'http://192.168.1.128:8080/photoaf.jpg'
    imageResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imageResp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    return img