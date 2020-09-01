# -*- coding: UTF-8 -*-
from PIL import Image
from PIL import ImageEnhance
import cv2


image = Image.open('Image/t.jpg')

# Brightened
enh_bri = ImageEnhance.Brightness(image)
brightness = 1.5
image_brightened = enh_bri.enhance(brightness)
image_brightened.show()

# Colored
enh_col = ImageEnhance.Color(image_brightened)
color = 1.5
image_colored = enh_col.enhance(color)
image_colored.show()

# Contrasted
enh_con = ImageEnhance.Contrast(image_colored)
contrast = 1.5
image_contrasted = enh_con.enhance(contrast)
image_contrasted.show()

# Sharped
enh_sha = ImageEnhance.Sharpness(image_contrasted)
sharpness = 3.0
image_sharped = enh_sha.enhance(sharpness)
image_sharped.show()

def grayimg(img):
    gray = cv2.resize(img, (img.shape[1] * 3, img.shape[0] * 3), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 120, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
    ret, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    # cv2.imwrite("binary.png", binary)
    # return binary
    return gray


def preprocess(gray):
    ret, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite("Image/binary.jpg", binary)
    ele = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 10))
    dilation = cv2.dilate(binary, ele, iterations=1)
    cv2.imwrite("dilation.png", dilation)
    return dilation
