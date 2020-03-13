#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json

TIMEOUT = 180
USER_ID = "045c45dceaa14b9998350d32617214a2"
USERNAME = "yangjian"
PASSWORD = "123456"
HOTFIX_CDMP_URL = "http://cdmpwebgateway-hotfix-xdgc-idesign-dev.opaas.enncloud.cn/CDMPWebGateway"
USER_LOGIN_URL = HOTFIX_CDMP_URL + "/user/userlogin1"
QUERY_USER_OWN_ABILITY_LABEL_URL = HOTFIX_CDMP_URL + "/user_own_ability_label/findUserOwnAbilityLabelByTypeCode"
DELETE_USER_OWN_ABILITY_LABEL_URL = HOTFIX_CDMP_URL + "/user_own_ability_label/deleteUserOwnAbilityLabel"
QUERY_ABILITY_LABEL_TYPE_URL = HOTFIX_CDMP_URL + "/ability_label/findAbilityLabelType"
QUERY_ABILITY_LABEL_URL = HOTFIX_CDMP_URL + "/ability_label/findAbilityLabel"
SET_USER_OWN_ABILITY_LABEL_URL = HOTFIX_CDMP_URL + "/user_own_ability_label/setUserOwnAbilityLabel"


def request(url, headers, params, data):
    response = requests.post(url, headers=headers, params=params, data=data, timeout=TIMEOUT)
    return response.text


# 登录管理后台
def userLogin(username, password):
    params = {"userName": username, "password": password, "platformCode": "glht", "clientCode": "pc_browser"}
    response = request(USER_LOGIN_URL, {}, params, {})
    jsonObject = json.loads(response)
    status = jsonObject["status"]
    if status != 1:
        exit(1)
    token = jsonObject["data"]["token"]
    refreshToken = jsonObject["data"]["refreshToken"]
    return (token, refreshToken)


# 查询用户已有能力标签
def queryUserOwnAbilityLabel(token, refreshToken, labelTypeCode):
    labelList = []
    headers = {"token": token, "refreshToken": refreshToken}
    params = {"userId": USER_ID, "labelTypeCode": labelTypeCode}
    response = request(QUERY_USER_OWN_ABILITY_LABEL_URL, headers, params, {})
    jsonObject = json.loads(response)
    status = jsonObject["status"]
    if status != 1:
        exit(1)
    data = json.loads(jsonObject["data"])
    if len(data) < 1:
        return labelList
    for item in data:
        labelList.append((item["id"], item["userId"], item["labelTypeCode"], item["labelCode"]))
    return labelList


# 删除用户已有能力标签
def deleteUserOwnAbilityLabel(token, refreshToken, id, userId, labelTypeCode, labelCode):
    headers = {"token": token, "refreshToken": refreshToken, "Content-Type": "application/json"}
    data = {"id": id, "userId": userId, "labelTypeCode": labelTypeCode, "labelCode": labelCode, "isPassed": 1}
    response = request(DELETE_USER_OWN_ABILITY_LABEL_URL, headers, {}, json.dumps(data))
    jsonObject = json.loads(response)
    status = jsonObject["status"]
    if status == 1:
        print("删除用户已有能力标签成功：%s" % (labelCode))
    else:
        print(">>> 删除用户已有能力标签失败：%s" % (labelCode))


# 查询能力标签类型
def queryAbilityLabelType(token, refreshToken):
    typeList = []
    headers = {"token": token, "refreshToken": refreshToken}
    response = request(QUERY_ABILITY_LABEL_TYPE_URL, headers, {}, {})
    jsonObject = json.loads(response)
    status = jsonObject["status"]
    if status != 1:
        exit(1)
    data = jsonObject["data"]
    for item in data:
        if item["isValid"] == 1:
            typeList.append(item["typeCode"])
    return typeList


# 查询能力标签
def queryAbilityLabel(token, refreshToken, labelTypeCode):
    labelDict = {}
    headers = {"token": token, "refreshToken": refreshToken}
    params = {"labelTypeCode": labelTypeCode}
    response = request(QUERY_ABILITY_LABEL_URL, headers, params, {})
    jsonObject = json.loads(response)
    status = jsonObject["status"]
    if status != 1:
        exit(1)
    data = jsonObject["data"]
    for item in data:
        if item["isValid"] == 1 and item["isSelected"] == 1:
            labelDict[item["labelCode"]] = item["labelLevel"]
    return labelDict


# 为用户设置能力标签
def setUserOwnAbilityLabel(token, refreshToken, userId, labelTypeCode, labelCode):
    headers = {"token": token, "refreshToken": refreshToken, "Content-Type": "application/json"}
    data = {"userId": userId, "labelTypeCode": labelTypeCode, "labelCode": labelCode, "isPassed": 1}
    response = request(SET_USER_OWN_ABILITY_LABEL_URL, headers, {}, json.dumps(data))
    jsonObject = json.loads(response)
    status = jsonObject["status"]
    if status == 1:
        print("为用户设置能力标签成功：%s" % (labelCode))
    else:
        print(">>> 为用户设置能力标签失败：%s" % (labelCode))


# 获取最大值的能力标签
def getTopLevelLabel(labelDict):
    top = 0
    labelCode = ""
    for key in labelDict:
        if labelDict[key] > top:
            top = labelDict[key]
            labelCode = key
    return labelCode


####
topLabelCode = ""
loginData = userLogin(USERNAME, PASSWORD)
typeList = queryAbilityLabelType(loginData[0], loginData[1])
for labelTypeCode in typeList:
    # 查询并删除用户已有能力标签
    labelList = queryUserOwnAbilityLabel(loginData[0], loginData[1], labelTypeCode)
    if len(labelList) > 0:
        for labelData in labelList:
            deleteUserOwnAbilityLabel(loginData[0], loginData[1], labelData[0], USER_ID, labelTypeCode, labelData[3])
    # 重新设置用户的能力标签
    labelDict = queryAbilityLabel(loginData[0], loginData[1], labelTypeCode)
    # 教育学历、设计年限
    if labelTypeCode == "GCSJ-JYXL" or labelTypeCode == "GCSJ-SJNX":
        topLabelCode = getTopLevelLabel(labelDict)
        setUserOwnAbilityLabel(loginData[0], loginData[1], USER_ID, labelTypeCode, topLabelCode)
    else:
        for key in labelDict:
            setUserOwnAbilityLabel(loginData[0], loginData[1], USER_ID, labelTypeCode, key)

# 服务地区
labelTypeCode = "GCSJ-FWDQ"
# 查询并删除用户已有能力标签
labelList = queryUserOwnAbilityLabel(loginData[0], loginData[1], labelTypeCode)
if len(labelList) > 0:
    for labelData in labelList:
        deleteUserOwnAbilityLabel(loginData[0], loginData[1], labelData[0], USER_ID, labelTypeCode, labelData[3])
# 重新设置用户的能力标签
labelDict = queryAbilityLabel(loginData[0], loginData[1], labelTypeCode)
for key in labelDict:
    setUserOwnAbilityLabel(loginData[0], loginData[1], USER_ID, labelTypeCode, key)
