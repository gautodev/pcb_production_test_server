#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : rtk.py
# Author        : bssthu
# Project       : rtk_trans
# Description   : socket 转发数据
# 

import json
import log
import queue
from server_thread import ServerThread
from client_thread import ClientThread
from sender_thread import SenderThread


class Rtk:
    def __init__(self):
        self.data_queue = queue.Queue()

    def main(self):
        config_file_name = 'config.json'
        try:
            with open(config_file_name) as config_data:
                configs = json.load(config_data)
        except:
            print('load config fail.')
            return

        log.initialize_logging(configs['enableLog'].lower() == 'true')
        log.info('main: start')

        self.server = ServerThread(configs['listenPort'])
        self.sender = SenderThread(self.server.clients, self.data_queue)
        self.client = ClientThread(configs['serverIpAddress'], configs['serverPort'], self.data_queue)

        self.server.start()
        self.sender.start()
        self.client.start()

        try:
            print("enter 'q' to quit. recv count: %d" % self.sender.recv_count)
            while input() != 'q':
                print("enter 'q' to quit. recv count: %d" % self.sender.recv_count)
                if not self.client.running or not self.server.running:
                    break
        except KeyboardInterrupt:
            pass

        self.client.running = False
        self.client.join()
        self.sender.running = False
        self.sender.join()
        self.server.running = False
        self.server.join()
        log.info('main: bye')


if __name__ == '__main__':
    rtk = Rtk()
    rtk.main()
