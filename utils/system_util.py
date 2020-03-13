#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from os import walk
from os.path import join

EXCLUDE_LIST = [
    '.DS_Store',
    'Thumbs.db',
]


class SystemUtil:


    def tree(root_path):
        file_list = []
        for parent_dir, dir_name_list, file_name_list in walk(root_path):
            for file_name in file_name_list:
                if file_name not in EXCLUDE_LIST:
                    file_list.append(join(parent_dir, file_name))
        # 忽略大小写排序
        list.sort(file_list, key=str.lower)
        return file_list


    def find(root_path, key):
        file_list = []
        for parent_dir, dir_name_list, file_name_list in walk(root_path):
            for file_name in file_name_list:
                if file_name.find(key) >= 0:
                    file_list.append(join(parent_dir, file_name))
        return file_list
