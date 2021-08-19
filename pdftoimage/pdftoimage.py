#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/8/13 14:18
@Author   : colinxu
@File     : pdftoimage.py
@Desc     : 
"""

from pdf2image import convert_from_path
from PIL import Image


def cur_array(array, nums):
    """
    切割数组
    :param array: 数组
    :param nums: 目标数量
    :return: 二维数组
    """
    result = []
    step = len(array) // nums
    for num in range(nums):
        if num == (nums - 1):
            result.append(array[num * step:])
        else:
            result.append(array[num * step:(num + 1) * step])
    return result


def splice_image(images, scale: float = 1):
    """
    拼接图片
    :param images: 图片列表
    :param scale: 缩放比例
    :return: 图片
    """
    width, height = images[0].size
    width = int(width * scale)
    height = int(height * scale)
    background = Image.new('RGB', (width, height * len(images)), (255, 255, 255))
    for index, image in enumerate(images):
        image = image.resize((width, height), Image.ANTIALIAS)
        location = (0, index * height)  # 放置位置
        if image.mode != "RGB":  # mode规整
            image = image.convert("RGB")
        background.paste(image, location)
    return background


if __name__ == '__main__':
    # 转化图片
    image_list = convert_from_path('D:/799640/Desktop/JM_销管家操作手册（全）V3.pdf')
    image_list = cur_array(image_list, 5)
    for i in range(len(image_list)):
        gen_image = splice_image(image_list[i], 0.5)
        gen_image.save('result-' + str(i + 1) + '.png')
