利用ssh远程开发是我们要学习的技能之一,本文只记录客户端操作

ssh是一种协议,最常用的实现是openssh,内置在大部分linux系统下,现在的windows也可以选择添加了

```bash
# 连接
ssh 用户名@hostname

ssh -l [用户名] hostname

ssh hostname

# 文件复制
scp remote_username@remote_ip:/path/source_file /path/target_file
```

不过,更推荐使用vscode的remote-ssh插件

依照[官方文档](https://vscode.github.net.cn/docs/remote/ssh),可以非常简单的使用本地的vscode环境 (包含插件),编辑远程的文件


## 免密码登陆
首先,你需要生成一对SSH密钥对,包括一个私钥和一个公钥 如果你还没有密钥对,可以使用ssh-keygen命令生成：  
`ssh-keygen -t rsa -b 4096`  
将你的公钥复制到远程服务器的~/.ssh/authorized_keys文件中 你可以使用ssh-copy-id命令简化这个过程：  
`ssh-copy-id user@remote-host`  
确保ssh-agent正在运行 如果它没有运行,你可以手动启动它：  
`eval $(ssh-agent)`  
使用ssh-add命令将你的私钥添加到ssh-agent中：  
`ssh-add ~/.ssh/id_rsa`  

## 了解隧道
