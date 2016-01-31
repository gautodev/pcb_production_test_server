#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : rtk.py
# Author        : bssthu
# Project       : rtk_trans
# Description   : socket 转发数据
# 

import json
import log
from server_thread import ServerThread
from client_daemon import ClientDaemon


class Rtk:
    def __init__(self):
        self.recv_count = 0

    def got_data_cb(self, data):
        log.debug('recv %d bytes' % len(data))
        self.recv_count += 1
        clients = self.server.clients.copy()
        for c in clients:
            try:
                c.sendall(data)
            except:
                pass

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
        self.client_daemon = ClientDaemon(configs['serverIpAddress'], configs['serverPort'], self.got_data_cb)
        self.server.start()
        self.client_daemon.start()

        try:
            print("enter 'q' to quit. recv count: %d" % self.recv_count)
            while input() != 'q':
                print("enter 'q' to quit. recv count: %d" % self.recv_count)
                if not self.client_daemon.running or not self.server.running:
                    break
        except KeyboardInterrupt:
            pass

        self.client_daemon.stop_daemon()
        self.client_daemon.join()
        self.server.running = False
        self.server.join()
        log.info('main: bye')


if __name__ == '__main__':
    rtk = Rtk()
    rtk.main()
