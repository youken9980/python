#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
import json
import os
from utils.system_util import SystemUtil


# 请求方法中使用的各常量
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}
CHARSET = "UTF-8"
TIMEOUT = 60
# bing 页面地址
BING_ROOT_URL = "https://cn.bing.com"
# 国际版参数
EN_PARAM = "&ensearch=1"
# BING_API_URL参数说明：
# format：xml(默认)-xml，js-json
# idx(取值范围0~7)：天数，0-今天，1-昨天，以此类推
# n(取值范围1~8)：返回数据条数
BING_API_URL = "/HPImageArchive.aspx?format=js&idx=0&n=8"
# 截取id开始标记
ID_BEGIN = "?id=OHR."
# 截取id结束标记
ID_END = "&rf="
# 本地储存路径
LOCAL_PATH = "/Users/youken/Destiny/Image/bing"


# 发送请求
def send_request(url):
    response = requests.get(url, params=HEADERS, timeout=TIMEOUT)
    return response.content


# 解析图片链接
def assemble_img_url_list(bing_url):
    img_url_list = []
    response = send_request(bing_url)
    json_obj = json.loads(response.decode(CHARSET))
    for img in json_obj["images"]:
        img_url_list.append(BING_ROOT_URL + img["url"])
    return img_url_list


# 若本地存储路径不存在则创建
def mkdir_if_not_exists(local_dir):
    if os.path.exists(local_dir) == False:
        try:
            os.mkdir(local_dir)
        except:
            print("新建本地存储文件夹失败")
            exit(1)


# 保存图片到本地
def save_img(bing_url, local_dir):
    for img_url in assemble_img_url_list(bing_url):
        img_id = img_url[img_url.find(ID_BEGIN) + len(ID_BEGIN) : img_url.find(ID_END)]
        # 截取文件名前缀，查找本地文件，判断是否已有相同图片
        idx_zh = img_id.find("_ZH-")
        idx_en = img_id.find("_EN-")
        img_prefix = img_id[0 : idx_zh + idx_en + 1]
        exist_file_list = SystemUtil.find(local_dir, img_prefix)
        if len(exist_file_list) > 0:
            print("文件已存在：%s" % exist_file_list[0])
            continue
        # 图片不存在，下载保存
        img_local_path = "%s/%s" % (LOCAL_PATH, img_id)
        response = send_request(img_url)
        try:
            file = open(img_local_path, "wb")
            file.write(response)
            file.close()
            print("保存成功：%s" % img_local_path)
        except:
            print("保存失败：%s" % img_local_path)


mkdir_if_not_exists(LOCAL_PATH)
save_img(BING_ROOT_URL + BING_API_URL, LOCAL_PATH)
save_img(BING_ROOT_URL + BING_API_URL + EN_PARAM, LOCAL_PATH)
