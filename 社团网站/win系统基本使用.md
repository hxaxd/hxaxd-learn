培训目标:

- 了解win系统的关键组件与核心概念
- 流畅,安全,干净的使用win系统

培训实践:

全流程实操讲解

参考资料:

- [win快捷键](https://support.microsoft.com/zh-cn/windows/windows-%E7%9A%84%E9%94%AE%E7%9B%98%E5%BF%AB%E6%8D%B7%E6%96%B9%E5%BC%8F-dcc61a57-8ff0-cffe-9796-cb9706c75eec)
- [官方帮助](https://support.microsoft.com/zh-cn/windows)
- [win系统基本使用](https://www.bilibili.com/video/BV1RwidY1Eot/)

### 快捷键

> 每天思考使用鼠标最多的事情,寻找它的快捷键

删除了三种

- 不被尊重(被软件的快捷键覆盖)
- 没用
- 用不了(网络原因)

#### 必会

切换

- Alt+Esc 循环浏览打开的窗口
- Alt+Tab 多次按 Tab 键时在打开的应用之间切换 
- win+Ctrl+D 添加虚拟桌面
- win+Ctrl+向右/左键 在右/左侧创建的虚拟桌面之间切换
- win+Ctrl+F4 关闭正在使用的虚拟桌面
- win+数字 (0-9) 切换到任务栏中数字位置中应用的最后一个活动窗口 
- win+D 显示和隐藏桌面
- win+方向键 对齐应用或窗口

系统

- win 打开“开始”菜单 
- Alt+F4 关闭活动窗口
- Alt+带下划线的字母 在应用中对带下划线的字母运行命令 
- Ctrl+空格键 启用或禁用中文输入法(不如shift)
- win+R 打开“运行”命令
- win+I 打开设置
- Ctrl+Shift+Esc 打开任务管理器
- Ctrl+W 关闭活动窗口
- Ctrl+T 创建新的选项卡
- F11 切换活动窗口全屏模式
- win+E 打开文件资源管理器

编辑

- Alt+Page Down/Up 下/上移一个屏幕
- F2 重命名所选项目
- Ctrl+C 复制
- Ctrl+V 粘贴
- Ctrl+X 剪切
- Ctrl+Y 重做
- Ctrl+Z 撤消
- Ctrl+A 全选
- Ctrl+F 查找
- Tab 缩进

#### 有用

- win+A 打开操作中心 
- win+Ctrl+Shift+数字 (0-9) 在任务栏中的数字位置以应用管理员身份打开另一个实例
- win+H 打开听写功能 
- win+L 锁定计算机 
- Ctrl+B 将所选文本设为粗体
- Ctrl+I 使所选文本采用斜体
- Ctrl+U 为所选文本添加下划线
- End 转到当前行的末尾
- home 转到当前行的开头
- Shift+DEL 删除(跳过回收站)
 
#### 有用但会被替代

```

utools

win+Shift+S 创建屏幕屏幕截图的一部分
win+V 打开剪贴板箱

Alt+向左/右键 返回/前进(鼠标侧键)

Vim

Ctrl+Backspace 删除左侧的字词
Ctrl+Del 删除右侧的字词
Ctrl+向下键 转到换行符的末尾
Ctrl+End/hpme 转到文档末尾/开头
Ctrl+向左键 转到上一个单词的开头
Ctrl+向右键 到下一个单词的开头
Ctrl+向上键 转到换行符的开头
Shift+Ctrl 向下-选择右侧段落
Shift+Ctrl+End 选择光标和文档末尾之间的文本
Shift+Ctrl+开始 选择光标和文档开头之间的文本
Shift+Ctrl+向左 选择左侧的字词
Shift+Ctrl+向右 选择右侧的字词
Shift+Ctrl+向上 选择左侧的段落
Shift+End 选择光标与当前行末尾之间的文本
Shift+开始 选择光标与当前行开头之间的文本
Shift+向左键 选择左侧的字符
Shift+向右键 选择右侧的字符
Shift+Tab 外缩进
```

### 注册表(regedit)与设置

注册表是系统的所有可修改设置  
控制面板/设置是对它的图形化封装

正确使用的PC不需要杀毒软件与防火墙  
Definder往往是副作用偏大

win系统的自定义幅度很大,藏得也很深,[win10+优化小工具](https://www.52pojie.cn/thread-1651910-1-1.html)和[DISM++](https://chuyu.me/zh-Hans/)

具体设置视频讲解

### 资源管理器(explorer)与任务管理器

[everything](https://www.voidtools.com/zh-cn/downloads/)是更快的搜索本地文件的工具

无论是win系统自带的应用卸载程序还是我非常推荐的[geek](https://geekuninstaller.com/)本质上都是依赖**注册表**去找到应用本身的卸载程序 (相关法律法规落实后,这是有效的)    
而geek可以立刻清理干净残余 (卸载程序往往不舍得完全杀死自己)尤其是注册表残余  
geek的强力删除也可以解决无法卸载的应用   

但终有漏网之鱼,[SoftCnKiller](https://blog.csdn.net/hfhbutn/article/details/104799162)和everything可以帮你解决  
softcnkiller可以显示软件的发行商,这有助于你发现目标,不过相关法律法规落实后,我们鲜少使用它   
最后,如果一个程序没有注册表 (这意味着它无法自己设置自启动),往往在everything中搜索并删除  

[ccleaner](https://www.ccleaner.com/zh-cn)是有名的清理软件,正确的使用电脑与分盘无需使用它  
但清理缓存与注册表的功能不失一种选择  
但真的需要清理时,缓存只是杯水车薪  
固态硬盘不分盘+安装软件位置的合理性才是唯一解  

任务管理器是管理内存的正解,当我们提到删除一个流氓软件时,往往是它的自启动大量占用系统资源  
右键任务栏/ctrl+shift+esc打开它,可以调整启动项与关闭正在运行的进程  
几乎没有启动项是更推荐的使用方式 (所有启动项都可以关闭,不必顾忌)  

如果你希望关闭某个软件 (以便删除它),但找不到,[IObitUnlocker](https://www.iobit.com/en/iobit-unlocker.php)能够帮助你

- Alt+D 选择地址栏 
- Alt+Enter 打开选定项的属性设置 
- Alt+P 显示预览面板 
- Alt+向上/下键 在文件夹路径中向上移动级别 
- Alt+向左/右键 查看上/下一个文件夹 
- Ctrl+Shift+E 展开导航窗格中树中的所有文件夹 
 
完全掌握电脑中的文件是入门PC使用的标志  

具体来说,尽量将应用安装在program files文件夹而非appdate或其他,这能限制应用的权限  
要点是全英文有效的命名+分门别类的位置+合理的结构

### 组策略(gpedit.msc)与设备管理器

了解设备驱动即可

### 终端

- Ctrl+向下/上键 将屏幕向下/上移动一行 
- Ctrl+End/home 滚动到控制台顶部 
- Ctrl+F 打开搜索命令提示符 
- Page Down/Up 将光标向下/上移动一页 
- 向上或向下键 循环浏览当前会话的命令历史记录 

了解如何使用无图形化界面应用即可

2024 005 1 2024/12/5

