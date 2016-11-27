#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : utils.py
# Author        : bssthu
# Project       : rtk_trans
# Description   : 
# 


def split(data, sep, maxsplit=-1):
    """split bytes

    Args:
        data (bytes): 待处理数据
        sep (int | str): 分隔符
        maxsplit (int): 最多分几个
    """
    if isinstance(sep, str):
        sep = ord(sep[0])
    if maxsplit == 0:
        return [data, ]
    ret = []
    split_count = 0
    i = 0
    for j in range(0, len(data)):
        if maxsplit >= 0 and split_count >= maxsplit:
            ret.append(data[i:])
            i = len(data)
            break
        b = data[j]
        if b == sep:
            ret.append(data[i:j])
            i = j + 1
            split_count += 1
    if i != len(data):
        ret.append(data[i:])
    return ret

if __name__ == '__main__':
    data = b'1234-567-\x80'
    print(split(data, ord('-')))
    print(split(data, ord('-'), 2))
    print(split(data, ord('-'), 1))
    print(split(data, ord('-'), 0))
    print(split(data, ord('1')))
    print(split(data, ord('\x80')))
    print(split(data, ord('9')))
    print(split(data, '-'))
