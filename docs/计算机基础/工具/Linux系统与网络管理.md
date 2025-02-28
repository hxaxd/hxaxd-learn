# Linux 进阶

* [命令行的艺术](https://github.com/jlevy/the-art-of-command-line/blob/master/README-zh.md) - 指导向 - 4

## 网络

```shell
netstat -atunlp all/tcp/ucp/端口号/监听/PID # 看网络与对应进程

curl -I/wget <url> # 下载

ip # 用来显示和操作路由 网络设备 接口等
ifconfig # 传统的网络配置工具,用来显示和设置网络接口的参数
dig # 查询DNS

rsync -av 源 obj # 同步
```

## 账号

```shell
# 不妨使用图形界面进行账号的添加和修改吧
id # 看一眼
sudo command # 假装是root
last # 看登录记录
exit # 退账号
w # 看登陆
```

## 进程

```shell
pgrep -f name # 查询进程
pkill -f name # 发送 sign 可以用名字是优势

du # 当前目录硬盘占用 -h 人类可读 -s * 符合后面通配的文件的占用
df # 整个系统的情况 -i 看inode使用情况
free # 看内存情况

ps aux  # 看所有进程
ps -l  # 看自己shell的
pstree -pu # PID/User

top # 推荐用 glances代替

isof -u username dirname 看目录下文件的被使用情况

nice -n 10 vim # 以 10 为 nice 值运行 vim
renice -n 10 -p 12345 # 设置 PID 为 12345 的进程的 nice 值为 10

command& 放入后台执行  

Ctrl-Z 挂起(停止)

Ctrl-C 进程终止

jobs -l pid 列出所有后台或挂起进程

fg num 来指定恢复作业

bg 用于将一个挂起的作业恢复到后台执行

nohub command 持续运行,不随shell而死

kill sign PID   
```

```text
sign:
SIGTERM (默认信号,值为 15):请求进程安全退出 
SIGKILL (值为 9):强制立即终止进程,不给予进程清理资源的机会 
SIGINT (值为 2):与 Ctrl+C 相同,通常用于中断进程 
SIGSTOP (值为 19):暂停进程,直到收到 SIGCONT 
SIGCONT (值为 18):继续执行之前被 SIGSTOP 暂停的进程 
示例
```

### 文件系统

```shell
mount 挂载文件系统

fdisk 磁盘分区

mkfs 创建文件系统

lsblk 列出所有可用的块设备
```
