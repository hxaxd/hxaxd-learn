# Emacs

## 参考资料

- [Emacs](https://zhuanlan.zhihu.com/p/385214753) - 知乎大佬 - 4

## 快捷键

配置在环境配置中

|   功能键   |  缩写 | 对应键盘按键 (PC/Mac) |
| :-----: | :-: | :-------------: |
| Control |  C  |  Ctrl / Control |
|   Meta  |  M  |    Alt/Option   |
|  Shift  |  S  |      Shift      |
|  Super  |  s  |   Win/Command   |

```text
# 光标移动
C-x C-c 退出
C-g 终止操作
C-z 挂起回到命令行 fg回来
C-p C-n C-b C-f 上下左右
M-b 左移一个词 M-f 右移一个词
C-a 移至行首 C-e 移至行尾
M-a 移至句首 M-e移至句尾 
M-< 移到文件开头 M-> 移到文件末尾
M-r 按第一次移到窗口中间 第二次移到窗口最上面 第三次移到窗口最下
C-v 向下一页 M-v 向上一页
跳行 M-g M-g 行号

# 移除
<DEL>或<backspace>删左侧字符 C-d删右侧字符
M-d 移除右一个词 M-<DEL>移除左一个词
移除右侧到句子结尾 M-k
移除右侧到行结尾 C-k 

# 复制粘贴
C-SPC 选中 Emacs下方显示 "Mark set"
M-w 复制选中的区域 C-w 剪切选中的区域
C-y 粘贴 加上M-y粘贴倒数第n+1次移除的内容
C-x C-SPC或C-u C-SPC 跳转回maek

# 搜索
C-s 搜索 再按一次 C-s 下一个 
回车退出 
C-g 退出并返回

# 换格式
交换左右字符 C-t 
交换词 M-t 
交换行 C-x C-t
创建新空行C-o 
前后所有连续空行变为一个空行 C-x C-o
后一词变为小写 M-l 变为大写 M-u 变为首字母大写 M-c

# 改字号
字号放大 C-x C-= 
缩小C-x C--
重置字号 C-x C-0

# 其他
C-u 12 meta-数字 给指令参数
C-/ C-_ C-x u 撤销 C-g 恢复

# 文件
C-x C-f 打开文件
C-x b 换文件
C-x C-b 列出已打开文件 
C-x o 转到列表
# 列表中
q 退出
d 标记打算关闭
s 标记打算保存
u 取消标记
x 执行
p 和 n 上下

# 多窗口
C-x 2 上下分割
C-x 3 左右分割
C-x 0 关闭
C-x 1 关闭其它 (仅针对窗口而非文件)
C-x o 切换到下一个 Window (列表也是 win)
C-x 4 f 在另一个窗口打开新的文件,如果只有一个窗口就分割成两个
C-x 4 b 切换文件
C-x 4 d 打开目录

C-M-v 另一个窗口向下翻页
C-M-S-v 向上翻页
```

### 如果参考上面教程的配置

```shell
交换 M-w 和 C-w,M-w 为剪切 C-w 为复制
交换 C-a 和 M-m,C-a 为到缩进后的行首 M-m 为到真正的行首

M-n 光标向下移动 10 行
M-p 光标向上移动 10 行
```
