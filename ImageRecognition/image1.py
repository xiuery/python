# -*- coding: utf-8 -*-
__author__ = 'XIUERY'

"""
pip install pillow      # 安装完成之后PIL会自动安装上
相关链接：http://pillow.readthedocs.io/en/latest/

pip install pytesseract
相关链接：https://pypi.org/project/pytesseract/

安装识别引擎tesseract-ocr：
https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-LSTM#400-alpha-for-windows
安装完成,需要将tesseract-ocr加入环境变量
"""

from PIL import Image
import pytesseract

for picture in ['images/img_01.png']:
    text = pytesseract.image_to_string(Image.open(picture), lang='chi_sim')

    print(text)
