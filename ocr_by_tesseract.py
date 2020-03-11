# -*- coding: UTF-8 -*-
import pytesseract
import cv2


def grayimg(img):
    gray = cv2.resize(img, (img.shape[1] * 3, img.shape[0] * 3), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 120, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
    ret, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    return binary
    # return gray


# def preprocess(gray):
    # ret, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    # cv2.imwrite("Image/binary.jpg", binary)
    # ele = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 10))
    # dilation = cv2.dilate(binary, ele, iterations=1)
    # cv2.imwrite("dilation.png", dilation)
    # return dilation


image = cv2.imread('Image/image2.jpg')
gray_image = grayimg(image)
# image_preprocess = preprocess(gray_img)
text = pytesseract.image_to_string(gray_image, lang='eng')
print(text)
