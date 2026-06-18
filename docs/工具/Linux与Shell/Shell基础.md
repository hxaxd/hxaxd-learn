# Shell 基础

## 参考资料

- [命令行的艺术](https://github.com/jlevy/the-art-of-command-line/blob/master/README-zh.md)

## 帮助

- 面对一个 command, 你首先要知道它是可执行文件 shell 内置命令还是别名 `type command`
- 用 man 来查询帮助, 不是所有 shell 都提供 info/help, 用 apropos 去查找文档

```text
man 的代号
1 shell
2 内核可用
3 库
4 设备
5 配置
6 games
7 协议
8 管理命令
9 内核文件
```

### 开关机

- `sync` 数据写入磁盘
- `shutddown [时间] [消息]` 警告关机
- `reboot` 重启
- `poweroff` 关机

### 命令

```bash
tab # 补全
^+r # 查找历史
^+u/k # 删除命令
^+a/e # 移动光标
^+i # 清屏
shift+[PD/PU] # 翻页

history n # 显示历史
!command !! !n # 执行历史

alias/unalias # 别名

command1 | command2 # 管道 (前一个命令的输出作为后一个命令的输入)
```

### 通配符

```bash
# 通配符
# *任意
# ?只一个任意字符  
# [abc]任意其中一个
# [^abc]任意不在其中
# [0-9]
```

### 文件基本操作

```bash
cp # 复制 -r form obj
mv # 移动 form obj
mkdir # 建立目录
pwd # 输出当前目录
rmdir # 删除目录
rm # 删除

cd # 跳转目录
# .当前 ..父 -上 ~家 ~name name 的家

ls # 列出目录中文件 -al  -i 显示 inode

ln from obj 硬链接 -s 软

file filename # 看文件类型
find # 建议用 fd 代替
head/tail filename # 看文件头尾 tail -f 自动跟随新增 (实时监控)
more/less filename # 按页看文件
cat filename # 读文本文件 -n 行号 -s 多空行合并
od filename # 二进制看文件 -t x/c 16 进制/字符
wc filename # 统计

touch # 建立空文件/改时间

spilt -b/l # size/行 file 文件前缀 分割文件

rename from obj filename # 重命名
```

### 系统与编码差异

- dos 与 unix 换行符不同, dos 为 `\r\n`, unix 为 `\n`
- `dos2unix filename` 转换为 unix 格式
- `unix2dos filename` 转换为 dos 格式
- `file filename` 查看文件类型 (编码)
- `iconv -f from -t to filename` 转换编码

### 文件权限

```bash
chown name:group filename # 改文件归属 -R 递归
chmod [mode] filename -R # 递归

# mode:
# - u/g/o/a +/-/= r/w/x
# - xyz r/w/x=4/2/1 x/y/z=u/g/o(r+w+x) 如 777

umask # 打印文件默认权限 拿掉的权限累加
chattr -R +-ai # 只追加/不可修改 改变属性
lsattr # 显示属性 -a 隐藏
```

### 解压缩

```bash
- tar -jcv -f name.tar.bz2 # 打包压缩
- tar -jtv -f f... # 查询
- tar -jxv -f f... # 解压
```
