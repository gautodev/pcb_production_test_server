# rtk_trans
直接转发

## Usage
```bash
python rtk.py
```

按回车查询状态。按'q'+回车退出程序。

通过 socket 发送命令到 `controlPort` 端口，命令格式为 `*#*#command#*#*`。

- `reset server` 关闭所有连到 rtk_trans 的客户 socket
- `list` 查询

## License
All rights reserved.
