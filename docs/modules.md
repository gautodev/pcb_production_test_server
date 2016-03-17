## 组件说明

#### rtk
主程序，启动各子线程，负责键盘交互。

#### log
日志。

#### server_thread
本地 socket server 线程，监听来自下层客户端的连接。

#### sender_thread
每个 SenderThread 管理一个从 ServerThread accept 到的 socket，
负责数据发送。

#### client_thread
socket client 线程，主动连接到差分源服务器，并接收数据。

#### dispatcher_thread
数据分发线程，
将 ClientThread 收到的数据转发到各 SenderThread。

#### control_thread
查询状态，调试（或维护）用。
