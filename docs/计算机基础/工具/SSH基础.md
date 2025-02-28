# SSH

## 参考资料

* [ssh](https://blog.csdn.net/m0_51720581/article/details/131796669) - csdn - 4

## 概念

* ssh 是一种协议, 最常用的实现是 openssh, 内置在大部分 Linux 系统下, 现在的 Windows 也可以选择添加了
* `~/.ssh` 存放 SSH 客户端相关配置和密钥文件
* 生成 `authorized_keys` 文件用于存放相关的主机和密钥信息
* `sshd_config` (server 配置文件)
* `ssh_config` (client 配置文件)

```shell
# 连接
ssh 用户名@hostname

ssh -l [用户名] hostname

ssh hostname

# 将本地机器中的文件复制到远程机器中
scp /path/local_file remote_username@remote_ip:/path/target_file

# 添加-r参数,递归拷贝目录
scp -r /path/local_directory remote_username@remote_ip:/path/target_directory

# 将远程机器中的文件复制到本地机器中
# 远程拷贝多个文件的命令形式比较繁琐,就不写了
scp remote_username@remote_ip:/path/source_file /path/target_file

# 指定使用23号端口
scp -P　23 /path/local_file remote_username@remote_ip:/path/target_file
```

* 更推荐使用 `VSCode` 的 `remote-ssh` 插件
* 依照[官方文档](https://VSCode.github.net.cn/docs/remote/ssh), 可以非常简单的使用本地的 VSCode 环境 (包含插件), 编辑远程的文件

## 免密码登陆

```shell
# 首先, 你需要生成一对 SSH 密钥对, 包括一个私钥和一个公钥 如果你还没有密钥对, 可以使用 ssh-keygen 命令生成
ssh-keygen -t rsa -b 4096

# 将你的公钥复制到远程服务器的 ~/.ssh/authorized_keys 文件中 你可以使用 ssh-copy-id 命令简化这个过程
ssh-copy-id user@remote-host

# 确保 ssh-agent 正在运行 如果它没有运行, 你可以手动启动它
eval $(ssh-agent)

# 使用 ssh-add 命令将你的私钥添加到 ssh-agent 中
`ssh-add ~/.ssh/id_rsa
```
