#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# https://s-file-1.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/version/data_version.json
# https://s-file-1.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/part_100.json
# https://s-file-1.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/part_101.json
# https://s-file-1.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/part_102.json

import requests
import json
import os
from utils.system_util import SystemUtil


# 请求方法中使用的各常量
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}
CHARSET = "UTF-8"
TIMEOUT = 60

ROOT_DIR = "/Users/youken/Destiny/Document/教科书"
DATA_URL = "https://s-file-1.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/version/data_version.json"
PDF_URL = "https://r2-ndr.ykt.cbern.com.cn/edu_product/esp/assets/{}.pkg/pdf.pdf"

# 发送请求
def send_request(url):
    response = requests.get(url, params=HEADERS, timeout=TIMEOUT)
    return response.content


# 解析链接
def get_urls():
    response = send_request(DATA_URL)
    json_obj = json.loads(response.decode(CHARSET))
    return json_obj["urls"]


def get_tag_name_by_tag_id(tag_id, tag_list):
    for tag in tag_list:
        if tag_id == tag["tag_id"]:
            return tag["tag_name"]
    return "xxx"


# 若本地存储路径不存在则创建
def mkdir_if_not_exists(local_dir):
    if os.path.exists(local_dir) == False:
        try:
            os.makedirs(local_dir)
        except Exception as e:
            print("新建本地存储文件夹失败")
            print(e.args)
            exit(1)


def save_pdf(url, local_dir, file_name):
    mkdir_if_not_exists(local_dir)
    response = send_request(url)
    local_file_path = local_dir
    if local_file_path.endswith("/"):
        local_file_path += file_name
    else:
        local_file_path += "/" + file_name
    try:
        file = open(local_file_path, "wb")
        file.write(response)
        file.close()
        print("保存成功：%s" % local_file_path)
    except Exception as e:
        print("保存失败：%s" % local_file_path)
        print(e.args)
        exit(1)


# urls = get_urls()
# url_list = urls.split(",")
# print(url_list)


start_flag = 0
with open(ROOT_DIR + "/part_101.json", "r") as file:
    data = json.load(file)
count = len(data)
for index in range(0, count):
    item = data[index]
    url = PDF_URL.format(item["id"])
    dir = ""
    tag_name_list = []
    paths = item["tag_paths"][0].split("/")
    for path in paths:
        tag_name = get_tag_name_by_tag_id(path, item["tag_list"])
        tag_name_list.append(tag_name)
    for i in range(len(tag_name_list) - 2):
        dir += tag_name_list[i] + "/"
    dir = ROOT_DIR + "/" + dir
    file_name = item["title"] + ".pdf"
    print("{}/{} ==> {}".format(index + 1, count, url))
    print(dir + file_name)
    if index >= start_flag:
        save_pdf(url, dir, file_name)
    print()

