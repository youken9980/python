#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
import sys
import os
from utils.system_util import SystemUtil
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib import parse
import time
import traceback


# 请求方法中使用的各常量
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}
CHARSET = "UTF-8"
PARSER = "html.parser"
TIMEOUT = 60
# 本地储存路径
LOCAL_PATH = "/Users/youken/Destiny/Music"


# 发送请求
def send_request(url: str):
    response = requests.get(url, params=HEADERS, timeout=TIMEOUT)
    return response.content


# 解析各属性
def extract_og(url: str):
    browser.get(url)
    time.sleep(0)
    browser.get(url)
    time.sleep(0)
    browser.switch_to.frame("g_iframe")
    html = BeautifulSoup(browser.page_source, PARSER)
    og_dict = {}
    for item in html.select("head meta"):
        if item.has_attr("property"):
            if item["property"] == "og:music:artist":
                og_dict['og:music:artist'] = item["content"]
            if item["property"] == "og:music:album":
                og_dict['og:music:album'] = item["content"]
            if item["property"] == "og:title":
                og_dict['og:title'] = item["content"]
            if item["property"] == "og:image":
                og_dict['og:image'] = item["content"]
    return og_dict


# 截取songId
def split_song_id(url: str):
    url_parse = parse.urlparse(url)
    url_query = parse.parse_qs(url_parse.query)
    id_list = url_query.get("id")
    return id_list[0]


# 若本地存储路径不存在则创建
def mkdir_if_not_exists(local_dir: str):
    if os.path.exists(local_dir) == False:
        try:
            os.mkdir(local_dir)
        except:
            print("新建本地存储文件夹失败")
            exit(1)


# 保存图片到本地
def download_media(url: str, local_dir: str):
    og_dict = extract_og(url)
    og_music_artist = og_dict['og:music:artist']
    og_music_album = og_dict['og:music:album']
    og_title = og_dict['og:title']
    # 下载封面
    og_image = og_dict['og:image']
    print("og_image: " + og_image)
    tmp_arr = og_image.split(".")
    tmp_arr_len = len(tmp_arr)
    file_ext = tmp_arr[tmp_arr_len - 1]
    file_name = "%s - %s - %s.%s" % (og_music_artist, og_music_album, og_title, file_ext)
    img_local_path = "%s/%s" % (local_dir, file_name)
    exist_file_list = SystemUtil.find(local_dir, file_name)
    if len(exist_file_list) < 1:
        response = send_request(og_image)
        try:
            file = open(img_local_path, "wb")
            file.write(response)
            file.close()
            print("保存成功：%s" % img_local_path)
        except:
            print("保存失败：%s" % img_local_path)
            exit(1)
    else:
        print("文件已存在：%s" % exist_file_list[0])
    # 保存歌曲
    song_id = split_song_id(url)
    song_url = "https://music.163.com/song/media/outer/url?id=%s.mp3" % song_id
    print("song_url: " + song_url)
    file_ext = "mp3"
    file_name = "%s - %s - %s.%s" % (og_music_artist, og_music_album, og_title, file_ext)
    img_local_path = "%s/%s" % (local_dir, file_name)
    exist_file_list = SystemUtil.find(local_dir, file_name)
    if len(exist_file_list) < 1:
        response = requests.get(song_url)
        response_url = response.url
        response = requests.get(response_url)
        try:
            file = open(img_local_path, "wb")
            file.write(response.content)
            file.close()
            print("保存成功：%s" % img_local_path)
        except:
            print("保存失败：%s" % img_local_path)
            exit(1)
    else:
        print("文件已存在：%s" % exist_file_list[0])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit(0)

    mkdir_if_not_exists(LOCAL_PATH)

    browser = webdriver.Chrome()
    try:
        for arg in sys.argv[1:]:
            download_media(arg, LOCAL_PATH)
    except Exception as e:
        print("下载失败")
        print(e)
        print(traceback.format_exc())
        exit(1)
    finally:
        browser.close()
        browser.quit()
