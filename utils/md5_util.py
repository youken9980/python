#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from hashlib import md5
from os.path import isfile


class Md5Util:


    def get_md5(file_path):
        if not isfile(file_path):
            return
        md5_hash = md5()
        file = open(file_path, 'rb')
        while True:
            buffer = file.read(8096)
            if not buffer:
                break
            md5_hash.update(buffer)
        file.close()
        return md5_hash.hexdigest()
