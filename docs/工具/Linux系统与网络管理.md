# Linux 进阶

- [命令行的艺术](https://github.com/jlevy/the-art-of-command-line/blob/master/README-zh.md)

## 网络

```bash
netstat -atunlp all/tcp/ucp/端口号/监听/PID # 看网络与对应进程
tcpdump -i eth0 -n -s 0 -w dump.pcap # 抓包, 保存到 dump.pcap 中
ss -tuln # 查看监听端口

curl -I/wget <url> # 下载

ip # 用来显示和操作路由, 网络设备, 接口等
ifconfig # 传统的网络配置工具, 用来显示和设置网络接口的参数
dig # 查询 DNS

rsync -av 源 obj # 同步

iptables # 防火墙
# 规则链
```

## 账号

```bash
# 不妨使用图形界面进行账号的添加和修改吧
id # 看一眼
sudo command # 假装是 root
last # 看登录记录
exit # 退账号
w # 看登陆
```

## 日志

```bash
journalctl -u 服务名 # 查看服务的日志
cat /var/log/syslog # 查看系统日志
cat /var/log/* # 查看日志
cat /run/log/ # 查看日志

```

## 系统状态

```bash
dmesg # 查看内核日志
dmesg grep 错误关键词 # 查看内核日志中包含错误关键词的行
uname -r # 查看内核版本
```

## 进程

```bash
pgrep -f name # 查询进程
pkill -f name # 发送 sign 可以用名字是优势

du # 当前目录硬盘占用 -h 人类可读 -s - 符合后面通配的文件的占用
iostat -x 1 # 每 1 秒输出一次磁盘 IO 统计信息
df # 整个系统的情况 -i 看 inode 使用情况
free # 看内存情况
vmstat 1 # 每 1 秒输出一次内存统计信息

ps aux  # 看所有进程
ps -l  # 看自己 shell 的
pstree -pu # PID/User

top # 推荐用 glances 代替

isof -u username dirname # 看目录下文件的被使用情况
isof -i :80 # 看端口被哪个进程占用

nice -n 10 vim # 以 10 为 nice 值运行 vim
renice -n 10 -p 12345 # 设置 PID 为 12345 的进程的 nice 值为 10

command& 放入后台执行  

Ctrl-Z 挂起(停止)

Ctrl-C 进程终止

jobs -l pid 列出所有后台或挂起进程

fg num 来指定恢复作业

bg 用于将一个挂起的作业恢复到后台执行

nohub command 持续运行, 不随 shell 而死

kill sign PID   
```

```text
sign:
SIGTERM (默认信号, 值为 15):请求进程安全退出 
SIGKILL (值为 9):强制立即终止进程, 不给予进程清理资源的机会 
SIGINT (值为 2):与 Ctrl+C 相同, 通常用于中断进程 
SIGSTOP (值为 19):暂停进程, 直到收到 SIGCONT 
SIGCONT (值为 18):继续执行之前被 SIGSTOP 暂停的进程 
示例
```

### 文件系统

```bash
mount 挂载文件系统

fdisk 磁盘分区

mkfs 创建文件系统

lsblk 列出所有可用的块设备
```
