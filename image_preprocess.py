# -*- coding: UTF-8 -*-
from PIL import Image
from PIL import ImageEnhance
import pytesseract
import cv2


image = Image.open('Image/image2.jpg')

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
