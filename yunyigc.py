#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup
import json
from pyecharts import Bar, Map, Geo
import pyecharts.echarts.events as events
from pyecharts_javascripthon import dom

TIMEOUT = 180
QUERY_TASK_URL = "http://cdtpwebgateway-hotfix-xdgc-idesign-dev.opaas.enncloud.cn/CDTPWebGateway/taskHall/follow"
FILE_PATH = "data/data.txt"

def request(url, headers, params, data):
    response = requests.post(url, headers=headers, params=params, data=data, timeout=TIMEOUT)
    return response.text


def query_task_list():
    params = {"sign": 0, "pageNum": 1, "pageSize": 10000, "sortRank": 9, "searchType": 0}
    response = request(QUERY_TASK_URL, {}, params, {})
    jsonObject = json.loads(response)
    status = jsonObject["status"]
    if status != 1:
        exit(1)
    return jsonObject["data"]["list"]


def trim_address(address):
    if '省' in address:
        address = address[:-1]
    elif '市' in address:
        address = address[:-1]
    elif '自治区' in address:
        address = address[:-3]
    elif '县' in address:
        address = address[:-1]
    return address


def render_map(title, maptype, attr, value, visual_range, on_event):
    map = Map(
        title,
        width=1200,
        height=600
    )
    map.add(
        "",
        attr,
        value,
        # 地图类型
        maptype=maptype,
        # 是否显示顶端图例
        is_legend_show=False,
        # 取消显示标记红点
        is_map_symbol_show=False,
        # 是否使用视觉映射组件
        is_visualmap=True,
        # 视觉映射组件两端文本颜色
        visual_text_color="#000",
        # 指定组件的允许的最小值与最大值
        visual_range=visual_range,
        # 显示各区域名称
        is_label_show=True,
        # 是否将组件转换为分段型（默认为连续型）
        is_piecewise=True,
    )
    map.on(events.MOUSE_CLICK, on_event)
    return map


def map_click(params):
    alert(params.data)
    map_city[params.name].render()


def dummy_click(params):
    pass


def geo_formatter(params):
    return params.name + ' : ' + params.value[2]


'''
# 发送请求获取订单列表并写入本地文件
task_list = query_task_list()
with open(FILE_PATH, 'w+') as file:
    for task in task_list:
        file.write(json.dumps(task) + "\n")
    file.close()
'''

# 读取本地文件获取订单列表
with open(FILE_PATH, 'r') as file:
    task_list = file.readlines()
    file.close()

# 循环订单列表获取各省市项目数
dict_province = {}
dict_city = {}
dict_cascade = {}
for item in task_list:
    task = json.loads(item)
    province = trim_address(task["demandProvince"])
    if province not in dict_province:
        dict_province[province] = 1
    else:
        dict_province[province] += 1

    city = trim_address(task["demandCity"])
    if city not in dict_city:
        dict_city[city] = 1
    else:
        dict_city[city] += 1

    if province not in dict_cascade:
        dict_cascade[province] = {}
    if city not in dict_cascade[province]:
        dict_cascade[province][city] = 1
    else:
        dict_cascade[province][city] += 1
print(dict_province)
print(dict_city)
print(dict_cascade)


# 生成地图
render_map(
    "项目分布图",
    "china",
    list(dict_province.keys()),
    list(dict_province.values()),
    [0, 150],
    map_click,
).render()
map_city = {}
for key in dict_cascade.keys():
    map_city[key] = render_map(
        "项目分布图",
        key,
        list(dict_cascade[province].keys()),
        list(dict_cascade[province].values()),
        [0, 75],
        dummy_click,
    )
print(map_city)


'''
geo = Geo(
    "项目分布图",
    title_color="#fff",
    title_pos="center",
    width=1200,
    height=600,
    background_color="#404a59",
)
geo.add(
    "中国",
    list(dict_city.keys()),
    list(dict_city.values()),
    maptype="china",
    is_visualmap=True,
    # 是否显示顶端图例
    is_legend_show=False,
    # 是否高亮显示标签。高亮标签即选中数据时显示的信息项
    is_label_emphasis=False,
    tooltip_formatter=geo_formatter,
)
geo.render(path="data/geo.html")
'''
