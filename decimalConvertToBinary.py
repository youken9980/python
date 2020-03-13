#!/usr/bin/env python3
# -*- coding:utf-8 -*-

decimal = -1    # 定义变量接收输入数值
while (decimal < 0):    # 输入负数时，重复提示输入
	try:    # 当输入小数时，捕获异常，提示输入合规的数值
		decimal = int(input("请输入要转换进制的数值："))    # 接收输入数值并将字符串类型转换为数值类型
		if (decimal < 0):    # 当输入负数时，提示输入合规的数值
			print("请输入大于等于零的整数。")    # 输出提示话术
	except ValueError as e:    # 捕获数值转换异常，提示输入合规的数值
		print("请输入大于等于零的整数。")    # 输出提示话术

binary = ""    # 定义变量存储输出结果
if (decimal == 0):    # 当输入0时，结果也应是0
	binary = str(decimal)    # 将数值类型的0转换为字符串类型
else:    # 当输入正整数时
	while(decimal > 0):    # 使用循环除法计算二进制结果，当商大于零时则进入循环
		remainder = decimal % 2;    # 计算余数
		decimal = decimal // 2;    # 计算商
		binary = "%s%s" % (remainder, binary)    # 存储二进制结果
print("%s%s" % ("该数字转换为二进制后是：", binary))    # 输出结果
