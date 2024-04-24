#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *********************************************************#
# @@Author: 张某某
# @@Create Date: 2022/9/27 15:03
# @@Modify Date: 2022/9/27 15:03
# @@Description: OCR识别图片
# *********************************************************#
import pytesseract
from PIL import Image
from branch import globalparam

OCRPATH = globalparam.ocr_path

def imageToStr(image_url, lang):
    """
    ocr识别中文
    :param image_url:
    :param lang:
    :return:
    """
    im = Image.open(image_url)
    im = im.convert('L')
    im_str = pytesseract.image_to_string(im, lang=lang)
    im_str = im_str.replace("\n", "").replace("\r", "")
    return im_str

def ocr_toast(name, locate=(100, 370, 258, 410)):
    """
    识别二次截图的toast
    :return:
    """
    try:
        img = Image.open(OCRPATH + '\\' + '{}.jpg'.format(name))
        region = img.crop(locate)
        region.save(OCRPATH + '\\' + '{}_ocr.jpg'.format(name))
        text = imageToStr(OCRPATH + '\\' + '{}_ocr.jpg'.format(name), 'chi_sim')
        return text
    except:
        pass

def ocr_picture_text(path):
    """
    直接进行ocr识别
    """
    try:
        text = imageToStr(path, 'chi_sim')
        return text
    except:
        pass

if __name__ == "__main__":
    ocr_toast('两次输入密码不一致')