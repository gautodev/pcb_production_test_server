#!/bin/sh
# -*- coding:utf-8 -*-
kill -2 $(ps -ef | grep $(ls *.py) | awk '{print $2}')
