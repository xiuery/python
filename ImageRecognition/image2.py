# -*-coding:utf-8-*-

import time

from PIL import Image
import pytesseract

time1 = time.time()

image = Image.open(r'20170608124203095.png')
code = pytesseract.image_to_string(image)
print(code)
