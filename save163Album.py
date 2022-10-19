#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
import sys
import os
from utils.system_util import SystemUtil
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time


# 请求方法中使用的各常量
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}
CHARSET = "UTF-8"
PARSER = "html.parser"
TIMEOUT = 60
# 本地储存路径
LOCAL_PATH = "/Users/youken/Destiny/Image/NeteaseMusic/专辑封面及头像"


# 发送请求
def send_request(url):
    response = requests.get(url, params=HEADERS, timeout=TIMEOUT)
    return response.content


# 解析图片链接
def extract_img_url(url):
    browser.get(url)
    time.sleep(0)
    browser.get(url)
    time.sleep(0)
    browser.switch_to.frame("g_iframe")
    html = BeautifulSoup(browser.page_source, PARSER)
    img_url = ""
    for item in html.select("head meta"):
        if item.has_attr("property"):
            if item["property"] == "og:image":
                img_url = item["content"]
                break
    return img_url


# 若本地存储路径不存在则创建
def mkdir_if_not_exists(local_dir):
    if os.path.exists(local_dir) == False:
        try:
            os.mkdir(local_dir)
        except:
            print("新建本地存储文件夹失败")
            exit(1)


# 保存图片到本地
def save_img(url, local_dir):
    img_url = extract_img_url(url)
    print("img_url: " + img_url)
    tmp_arr = img_url.split("/")
    tmp_arr_len = len(tmp_arr)
    file_name = tmp_arr[tmp_arr_len - 1]
    img_local_path = "%s/%s" % (local_dir, file_name)
    exist_file_list = SystemUtil.find(local_dir, file_name)
    if len(exist_file_list) > 0:
        print("文件已存在：%s" % exist_file_list[0])
        return
    response = send_request(img_url)
    try:
        file = open(img_local_path, "wb")
        file.write(response)
        file.close()
        print("保存成功：%s" % img_local_path)
    except:
        print("保存失败：%s" % img_local_path)
        exit(1)


try:
    if len(sys.argv) < 2:
        exit(0)

    mkdir_if_not_exists(LOCAL_PATH)

    # service = Service()
    # service.start()
    # browser = webdriver.Remote(service.service_url)
    browser = webdriver.Chrome()
    for arg in sys.argv[1:]:
        save_img(arg, LOCAL_PATH)
    browser.quit()
except:
    print("下载失败")
    exit(1)
