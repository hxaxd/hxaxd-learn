- [命令行的艺术](https://github.com/jlevy/the-art-of-command-line/blob/master/README-zh.md) 指导向 4

### 帮助
面对一个command,你首先要知道它是可执行文件、shell 内置命令还是别名`type command`  

用man来查询帮助,不是所有shell都提供info/help,用apropos去查找文档

man代号
```shell
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
- sync数据写入磁盘
- shutddown 警告关机 -r/h/c/k [time/min] [warning]
- reboot 重启
- poweroff 关机
### 变量:
- name=abc  
- name="abc$LANG"->abczh_CN....  
- name='abc&LANG'->abc&LANG  
- name=${name}:abc 扩增
- name=$(command)
- export name=... 环境变量
- unset...
- env 看所有环境变量
- set 看所有
- ?变量是上一个命令的返回值
- echo 打印变量
- locale 打印本地化相关
### 命令
```
tab 补全
^+r 查找历史
^+u/k 删除命令
^+a/e 移动光标
^+i 清屏
shift+[PD/PU] 翻页

history n 显示历史
!command !! !n 执行历史

< 和 > 来重定向输出和输入, | 来重定向管道  > 会覆盖文件而 >> 在文件末添加  
<(command) 被视为文件
command <<EOF 和 EOF 之间的所有内容都会被当作输入传递给 cat,不必使用管道或者临时文件

标准输出 stdout >/>>和标准错误 stderr 2>/2>>  

通配符:  
*任意
?只一个任意字符  
[abc]任意其中一个
[^abc]任意不在其中
[0-9]

xargs 将输入转换为参数  
如:cat hosts | xargs -I{} ssh root@{} hostname

alias unalias 别名
```
### 文件基本操作
```bash
cp 复制 -r form obj
mv 移动 form obj
mkdir name 建立目录
pwd 当前目录
rmdir name 删除目录
rm name 删除

cd 跳转目录
.当前 ..父 -上 ~家 ~name name的家


ls 列出目录中文件 -al  -i 显示inode

ln from obj 硬链接 -s软

file filename 看文件类型
find 建议用fd代替
head/tail filename 看文件头尾 tail -f 自动跟随新增 (实时监控)
more/less filename 按页看文件
cat filename读文本文件 -n行号 -s多空行合并
od filename二进制看文件 -t x/c 16进制/字符
wc filename统计

chown name:group filename 改文件归属 -R递归
chmod [mode] filename -R递归

mode:
- ugoa +-= rwx
- xyz r/w/x=4/2/1 x/y/z=u/g/o(r+w+x) 如777

touch 建立空文件/改时间

umask 打印文件默认权限 拿掉的权限累加
chattr -R +-ai 只追加/不可修改 改变属性
lsattr 显示属性 -a 隐藏

spilt -b/l size/行 file 文件前缀 分割文件

rename from obj filename
```
### 解压缩
```bash
- tar -jcv -f name.tar.bz2 打包压缩
- tar -jtv -f f... 查询
- tar -jxv -f f... 解压
```






