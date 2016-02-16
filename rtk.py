#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : rtk.py
# Author        : bssthu
# Project       : rtk_trans
# Description   : socket 转发数据
# 

import json
import log
from control_thread import ControlThread
from client_thread import ClientThread
from dispatcher_thread import DispatcherThread
from server_thread import ServerThread


class Rtk:
    def __init__(self):
        pass

    def got_data_cb(self, data, rcv_count):
        self.dispatcher.data_queue.put((data, rcv_count))

    def got_client_cb(self, client_socket, address):
        self.dispatcher.add_client(client_socket, address)

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

        self.server = ServerThread(configs['listenPort'], self.got_client_cb)
        self.controller = ControlThread(configs['controlPort'])
        self.dispatcher = DispatcherThread()
        self.client = ClientThread(configs['serverIpAddress'], configs['serverPort'], self.got_data_cb)

        self.server.start()
        self.controller.start()
        self.dispatcher.start()
        self.client.start()

        try:
            print("enter 'q' to quit")
            while input() != 'q':
                print("enter 'q' to quit. rcv count: %d, client count: %d"
                      % (self.client.rcv_count, len(self.dispatcher.clients)))
                if not self.client.running or not self.server.running:
                    break
        except KeyboardInterrupt:
            pass

        self.controller.running = False
        self.controller.join()
        self.client.running = False
        self.client.join()
        self.dispatcher.running = False
        self.dispatcher.join()
        self.server.running = False
        self.server.join()
        log.info('main: bye')


if __name__ == '__main__':
    rtk = Rtk()
    rtk.main()
