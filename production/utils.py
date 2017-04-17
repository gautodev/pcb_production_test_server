#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : utils.py
# Author        : bssthu
# Project       : rtk_trans
# Description   : 
# 


def split(data, sep):
    """split bytes

    Args:
        data (bytes): 待处理数据
        sep (bytes): 分隔符
    """
    ret = []
    i = 0
    j = 0
    while i < len(data):
        if data[i:].startswith(sep):
            ret.append(data[j:i])
            i = i + len(sep)
            j = i
        else:
            i = i + 1
    ret.append(data[j:])
    return ret


if __name__ == '__main__':
    data = b'1234-567-\x80'
    print(split(b'1234-567-\x80', b'\r\n'))
    print(split(b'1234567-\x80\r\n', b'\r\n'))
    print(split(b'1234567\r-x\r\n1234567\n-x\r', b'\r\n'))
