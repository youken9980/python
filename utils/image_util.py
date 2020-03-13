#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import cv2
from numpy import float32
from numpy import mean


class ImageUtil:


    # 均值哈希算法
    def a_hash(img):
        # 缩放为8*8
        img = cv2.resize(img, (8, 8))
        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # s为像素和初值为0，hash_str为hash值初值为''
        s = 0
        hash_str = ''
        # 遍历累加求像素和
        for i in range(8):
            for j in range(8):
                s = s + gray[i, j]
        # 求平均灰度
        avg = s / 64
        # 灰度大于平均值为1相反为0生成图片的hash值
        for i in range(8):
            for j in range(8):
                if gray[i, j] > avg:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'
        return hash_str


    # 差值哈希算法
    def d_hash(img):
        # 缩放8*8
        img = cv2.resize(img, (9, 8))
        # 转换灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hash_str = ''
        # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
        for i in range(8):
            for j in range(8):
                if gray[i, j] > gray[i, j + 1]:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'
        return hash_str


    # 感知哈希算法
    def p_hash(img):
        # 缩放32*32
        img = cv2.resize(img, (32, 32))  # , interpolation=cv2.INTER_CUBIC
        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 将灰度图转为浮点型，再进行dct变换
        dct = cv2.dct(float32(gray))
        # opencv实现的掩码操作
        dct_roi = dct[0:8, 0:8]
        hash_list = []
        average = mean(dct_roi)
        for i in range(dct_roi.shape[0]):
            for j in range(dct_roi.shape[1]):
                if dct_roi[i, j] > average:
                    hash_list.append(1)
                else:
                    hash_list.append(0)
        return hash_list


    # Hash值对比
    # 均值哈希算法、差值哈希算法、感知哈希算法，相似度值为[0~64]之间，值越小越相似，相同图片值为[0]
    def hash_compare(hash1, hash2):
        # 算法中1和0顺序组合起来的即是图片的指纹hash。顺序不固定，但是比较的时候必须是相同的顺序。
        # 对比两幅图的指纹，计算汉明距离，即两个64位的hash值有多少是不一样的，不同的位数越小，图片越相似
        # 汉明距离：一组二进制数据变成另一组数据所需要的步骤，可以衡量两图的差异，汉明距离越小，则相似度越高。汉明距离为0，即两张图片完全一样
        n = 0
        # hash长度不同则返回-1代表传参出错
        if len(hash1) != len(hash2):
            return -1
        # 遍历判断
        for i in range(len(hash1)):
            # 不相等则n计数+1，n最终为相似度
            if hash1[i] != hash2[i]:
                n = n + 1
        return n


    # 单通道(灰度)直方图算法
    def gray_histogram(img):
        # 计算单通道的直方图的相似值
        return cv2.calcHist([img], [0], None, [256], [0.0, 255.0])


    # 三通道(RGB)直方图算法
    def rgb_histogram(img, size=(256, 256)):
        # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
        return cv2.split(cv2.resize(img, size))


    # 使用单通道(灰度)直方图算法计算两张图像的相似度
    # 单通道直方图算法、三通道直方图算法，相似度值为[0~1]之间，值越大越相似，相同图片值为[1]
    def calc_gray_histogram(hist1, hist2):
        # 计算直方图的重合度
        degree = 0
        for i in range(len(hist1)):
            if hist1[i] != hist2[i]:
                degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
            else:
                degree = degree + 1
        return degree / len(hist1)


    # 使用三通道(RGB)直方图算法计算两张图像的相似度
    # 单通道直方图算法、三通道直方图算法，相似度值为[0~1]之间，值越大越相似，相同图片值为[1]
    def calc_rgb_histogram(split_img1, split_img2):
        sub_data = 0
        for im1, im2 in zip(split_img1, split_img2):
            hist1 = gray_histogram(im1)
            hist2 = gray_histogram(im2)
            sub_data += calc_gray_histogram(hist1, hist2)
        return sub_data / 3
