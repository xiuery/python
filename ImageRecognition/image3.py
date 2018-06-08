# -*-coding:utf-8-*-

from PIL import Image
import pytesseract


def binarizing(img, threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


def depoint(img):
    pixdata = img.load()
    w, h = img.size
    for y in range(1, h-1):
        for x in range(1, w-1):
            count = 0
            if pixdata[x, y-1] > 245:
                count = count + 1
            if pixdata[x, y+1] > 245:
                count = count + 1
            if pixdata[x-1, y] > 245:
                count = count + 1
            if pixdata[x+1, y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x, y] = 255
    return img


image = Image.open('20170608124203095.png')
img = image.convert('L')
img1 = binarizing(img, 190)
img1.show()
code = pytesseract.image_to_string(img1)
print("识别该验证码是:" + str(code))
