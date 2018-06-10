# -*-coding:utf-8-*-

import time

from PIL import Image
import pytesseract

time1 = time.time()

image = Image.open(r'img_01.png')
code = pytesseract.image_to_string(image)
print(code)
