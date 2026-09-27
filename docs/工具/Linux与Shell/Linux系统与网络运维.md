# Linux 系统与网络运维

# Linux 基础

## 参考资料

- 鸟哥的 Linux 私房菜
- [Linux101](https://101.lug.ustc.edu.cn/)

## Linux

### 一切都是文件

- `dev/sd [a-z]` 表示不同的 sata/usb 存储硬件
- `dev/sda [1-4]` 是 MBR 分区表的主要分区或拓展分区 (最多一个)
- `[5-]` 是逻辑分区, 是拓展分区指引的分区
- `/` 根目录, 文件系统起点
- `/bin` 基础用户命令 (单用户模式可用)
- `/boot` 内核与引导加载器文件
- `/dev` 设备节点
    - `/dev/null` 黑洞, 写即丢, 读即 EOF
    - `/dev/zero` 零源, 无限 0 流
- `/etc` 系统配置
    - `/etc/hosts` 静态主机映射
    - `/etc/resolv.conf` DNS 服务器列表
    - `/etc/passwd` 用户账号数据库
    - `/etc/group` 用户组数据库
- `/home` 普通用户家目录
- `/lib` 基础共享库与内核模块
- `/media` 自动挂载点 (U 盘, 光驱等)
- `/mnt` 手动临时挂载点
- `/opt` 第三方大型软件包
- `/proc` 运行时内核与进程视图
    - `cat /proc/[pid]/status` 进程状态快照
    - `ls -l /proc/[pid]/fd` 已打开文件列表
    - `cat /proc/[pid]/fdinfo/[fd]` 文件描述符详情
    - `cat /proc/cpuinfo` CPU 硬件信息
    - `cat /proc/meminfo` 内存使用统计
- `/root` 超级用户家目录
- `/sbin` 系统管理命令
- `/srv` 本机对外提供的服务数据
- `/sys` 内核设备模型接口
    - `/sys/class` 按功能分类的设备
    - `/sys/block` 块设备
    - `/sys/char` 字符设备
    - `/sys/devices` 物理设备树
    - `/sys/fs` 文件系统参数
    - `/sys/kernel` 内核可调参数
    - `/sys/module` 已加载模块列表
- `/tmp` 临时文件 (重启清空)
- `/usr` 只读用户程序与数据
- `/var` 可变数据 (日志, 缓存, 队列)
- `lost+found` 每个路径下都有, 恢复文件系统错误
- `/run` 运行时系统信息

### GPT 分区表

- 由 LBA1 (兼容 MBR 的启动, 但不记录分区表, 所以还是启动不了, 保护作用), LBA2-33 组成, 每个可以记录四组分区

#### 文件信息

- `[d, -, l, b, c, s, p]` 目录, 文件, 链接文件, 区块设备, 字符设备, 数据接口文件, FIFO 管道文件 (解决多线程冲突)
- `[rwx]*3`, 读 写 修改
- 对于目录来说, r 是读有啥文件, w 是操纵目录结构 (不包括里面的文件内容), x 是能否进入目录工作

#### 隐藏属性

- SUID (Set User ID) 文件在执行时以文件所有者的权限运行
- SGID (Set Group ID) 文件在执行时以文件所属组的权限运行
- SBIT (Sticky Bit) 只有文件的所有者和 root 用户可以删除该文件
- 4+2+1 表示文件的隐藏属性

#### xfs 系统

- 实时分配 inode, 除了数据区域之外, 还有两个区域分别是记录文件系统的变化以及缓冲新建立的文件 (分配好再放)
- ext 文件系统只能针对整个文件系统配额, XFS 可以用 project 模式来设计不同目录的磁盘配额

#### ~~快捷方式~~

- 硬链接是建立两个不同的文件名, 指向同一个 inode, 但是不能链接目录, 也不能跨文件系统
- 软链接是一个文件, 当你操作的时候会导向实际的目录

### 用户

- 一个用户可以在多个用户组, 所以要区分有效用户组与初始用户组, 对已有文件, 该用户的权限是所有加入用户组, 新建文件归属有效用户组
- UID/GID 才是用户本体

---

# Linux 系统与网络管理

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

---

# 远程开发与集群

## 参考资料

- Codex

## SSH

### 配置

```sshconfig
Host lab
    HostName 10.0.0.12
    User hx
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 30
    ServerAliveCountMax 4

Host gpu01
    HostName 10.10.0.21
    User hx
    ProxyJump lab
```

- `~/.ssh/config` 给远程主机起别名, 后续 `ssh`, `scp`, `rsync` 都能用
- `ProxyJump` 走跳板机, 比先登录跳板机再手动登录目标机器干净
- `ServerAliveInterval` 与 `ServerAliveCountMax` 用于保活和断线检测
- 多级跳板可以写成 `ProxyJump gateway1,gateway2`

```bash
ssh lab
scp file.txt lab:~/tmp/
rsync -av project/ lab:~/project/
```

### 密钥

```bash
ssh-keygen -t ed25519 -C "name@example.com"
ssh-copy-id lab
ssh-add ~/.ssh/id_ed25519
```

- 私钥留在本地, 公钥写入远程 `~/.ssh/authorized_keys`
- 私钥建议设置 passphrase, 再用 `ssh-agent` 缓存
- 常见权限

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/config ~/.ssh/id_ed25519 ~/.ssh/authorized_keys
chmod 644 ~/.ssh/id_ed25519.pub
```

## tmux

```bash
tmux new -s work
tmux ls
tmux attach -t work
tmux kill-session -t work
```

- `tmux` 用来保持远程会话, SSH 断开后 session 仍在
- 长任务放进 `tmux` 前先确认机器规则, 不要在登录节点跑重计算
- 离开时用 `Ctrl-b d`, 不要直接关掉正在运行任务的 shell

## 文件传输

### scp

```bash
scp local.txt lab:~/tmp/
scp lab:~/result.txt .
scp -r project lab:~/project
scp -P 2222 local.txt user@host:~/tmp/
```

- `scp` 适合少量文件的一次性复制
- `-r` 复制目录, `-P` 指定端口
- 大目录, 断点续传和增量同步优先用 `rsync`

### rsync

```bash
rsync -avP source/ lab:~/target/
rsync -avP source lab:~/target/
```

- `source/` 同步目录内容
- `source` 同步目录本身

```bash
rsync -avP --exclude '.git/' --exclude '__pycache__/' project/ lab:~/project/
rsync -avP -e "ssh -p 2222" project/ user@host:~/project/
rsync -avn --delete source/ lab:~/target/
rsync -av --delete source/ lab:~/target/
```

- `-a` 保留权限, 时间戳和符号链接等信息
- `-P` 等价于 `--partial --progress`, 适合大文件和不稳定网络
- `--delete` 会删除目标端多余文件, 先用 `-n` dry run
- `--exclude` 排除缓存, 依赖目录和构建产物

### 大文件

```bash
tar -cf dataset.tar dataset/
rsync -avP dataset.tar lab:~/data/
sha256sum dataset.tar
```

- 海量小文件先打包再传, 避免元数据开销
- 文本和 CSV 适合压缩, 已压缩图片, 视频, parquet, zip 收益通常不大
- 重要数据传输后用 `sha256sum` 校验

## Slurm

- Linux 集群管理, 分配给每个作业固定资源
