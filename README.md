# pcb_production_test_server
PCB板卡生产测试服务器

## Intro
主要功能：

1. 转发差分数据
2. 接收客户端的心跳信息
3. 向管理端发送当前客户端状态

## Setup
```bash
cp ./docs/config.json.default ./conf/config.json
```
并按需修改配置文件`conf/config.json`。

## Usage
- 启动方法
```bash
python3 rtk.py
# or
./start.sh
```

按回车查询状态。按'q'+回车或Ctrl+c退出程序。

通过 socket 发送命令到 `controlPort` 端口，命令格式为 `*#*#command#*#*`。

- `reset server` 关闭所有连到 rtk_trans 的客户 socket
- `list` 查询

## 其他说明
* [主要模块](docs/modules.md)

## License
All rights reserved.
