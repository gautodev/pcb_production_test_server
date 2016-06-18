#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : rtk_trans.py
# Author        : bssthu
# Project       : rtk_trans
# Description   : socket 转发数据
# 

import os
import sys
import json
import time
from rtk_trans import log
from rtk_trans.control_thread import ControlThread
from rtk_trans.client_thread import ClientThread
from rtk_trans.dispatcher_thread import DispatcherThread
from rtk_trans.server_thread import ServerThread


class Rtk:
    def __init__(self):
        self.server = None
        self.controller = None
        self.dispatcher = None
        self.client = None

    def got_data_cb(self, data, rcv_count):
        """接收到差分数据的回调函数

        Args:
            data: 收到的数据包
            rcv_count: 收到的数据包的编号
        """
        self.dispatcher.data_queue.put((data, rcv_count))

    def got_client_cb(self, client_socket, address):
        """接受来自下层客户端的 socket 连接的回调函数

        Args:
            client_socket: 与客户端连接的 socket
            address: 客户端地址
        """
        self.dispatcher.add_client(client_socket, address)

    def got_command_cb(self, command):
        """接收到来自控制端口的指令的回调函数

        Args:
            command: 待处理的命令
        """
        if command == 'reset server':
            old_dispatcher = self.dispatcher
            self.dispatcher = DispatcherThread()
            old_dispatcher.running = False
            self.dispatcher.start()
        elif command == 'list':
            self.controller.msg_queue.put('client count: %d\r\n' % len(self.dispatcher.clients))
            for _id, sender in self.dispatcher.clients.copy().items():
                self.controller.msg_queue.put('%d: %s, %d\r\n' % (sender.sender_id, sender.address, sender.send_count))

    def wait_for_keyboard(self):
        """quit when press q or press ctrl-c, or exception from other threads"""
        try:
            print("enter 'q' to quit")
            while input() != 'q':
                print("enter 'q' to quit. rcv count: %d, client count: %d"
                      % (self.client.rcv_count, len(self.dispatcher.clients)))
                if not self.client.running or not self.server.running:
                    break
        except KeyboardInterrupt:
            pass
        except EOFError:
            # no input
            while True:
                time.sleep(1)
                if not self.client.running or not self.server.running:
                    break

    def main(self):
        # config
        config_file_name = os.path.join(sys.path[0], 'conf/config.json')
        try:
            with open(config_file_name) as config_fp:
                configs = json.load(config_fp)
        except:
            print('failed to load config from config.json.')
            return

        # log init
        log.initialize_logging(configs['enableLog'].lower() == 'true')
        log.info('main: start')

        # threads
        self.server = ServerThread(configs['listenPort'], self.got_client_cb)
        self.controller = ControlThread(configs['controlPort'], self.got_command_cb)
        self.dispatcher = DispatcherThread()
        self.client = ClientThread(configs['serverIpAddress'], configs['serverPort'], self.got_data_cb)

        self.server.start()
        self.controller.start()
        self.dispatcher.start()
        self.client.start()

        # wait
        self.wait_for_keyboard()

        # quit & clean up
        self.controller.running = False
        self.controller.join()
        self.client.running = False
        self.client.join()
        self.server.running = False
        self.server.join()
        self.dispatcher.running = False
        self.dispatcher.join()
        log.info('main: bye')
