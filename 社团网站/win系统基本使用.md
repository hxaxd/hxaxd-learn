培训目标:

- 了解win系统的关键组件与核心概念
- 流畅,安全,干净的使用win系统

培训实践:

全流程实操讲解

参考资料:

- [win系统基本使用]()
 

### 系统设置与设备管理*

Win+I 呼出设置 必要的设置是打开开发者模式 (从松散源安装软件)与个性化 (显示设置),比较有名的"骗局"是电源设置与清理缓存  
![](https://s2.loli.net/2024/05/20/SgjoZb5srhDiWFX.png)

较新的打印机等硬件可被系统直接识别,没有的话调用疑难解答,再没有下载驱动  
如果是局域网下共享打印机,应选择网络打印机,不能自动识别手动输入IP

其他设备管理 win+R devmgmt.msc,更推荐win键后直接搜索,可对设备禁用,删除,回退或更新驱动

### 文件管理与软件删除*

[everything](https://www.voidtools.com/zh-cn/downloads/)是更快的搜索本地文件的工具![](https://s2.loli.net/2024/05/20/yswIYa1xXq8Wb7l.png)

无论是win系统自带的应用卸载程序还是我非常推荐的[geek](https://geekuninstaller.com/)本质上都是依赖**注册表**去找到应用本身的卸载程序 (相关法律法规落实后,这是有效的)  
而geek可以立刻清理干净残余 (卸载程序往往不舍得完全杀死自己)尤其是注册表残余  
geek的强力删除也可以解决无法卸载的应用  
![](https://s2.loli.net/2024/05/21/n4u2176daxbXOPj.png)

但终有漏网之鱼,[SoftCnKiller](https://blog.csdn.net/hfhbutn/article/details/104799162)和everything可以帮你解决  
softcnkiller可以显示软件的发行商,这有助于你发现目标,不过相关法律法规落实后,我们鲜少使用它  
最后,如果一个程序没有注册表 (这意味着它无法自己设置自启动),往往在everything中搜索并删除

### 系统工具与疑难问题*

相关环境的缺失是常见问题,尤其是C++环境的缺失,可去官网下载C++2016-解决  
也可以使用[DirectX修复工具](https://blog.csdn.net/vbcom/article/details/7245186)一键解决  
![](https://s2.loli.net/2024/05/21/OeUpoXBNw31qs4I.png)

win系统的图形界面依赖于资源管理器,而对其的更改 (例如对右键菜单的增加),也许会导致异常的卡死,而一个线程的卡死意味着explorer的完全卡死,在注册表的更改能解决不希望存在的选项

无论是设置还是控制面板,本质是对底层系统工具的包装,对接口的精简,因此当遇到疑难问题搜索时,解决方案中可能涉及的系统工具有必要熟悉  
设备管理器  
注册表管理器  
系统配置----底层接口调用的程序    
组策略----底层设置  
CMD/powershell----命令行


## 使用体验的优化

### 系统设置的优化

win系统的自定义幅度很大,藏得也很深,[win10+优化小工具](https://www.52pojie.cn/thread-1651910-1-1.html)和[DISM++](https://chuyu.me/zh-Hans/)
![](https://s2.loli.net/2024/05/21/oOjalneFxYJygZ7.png)
![](https://s2.loli.net/2024/05/21/FrGA6yMfTNsi4wn.png)  
相关功能自行搜索

正确使用的PC不需要杀毒软件与防火墙
Definder往往是副作用偏大

### 空间清理与内存管理*

[ccleaner](https://www.ccleaner.com/zh-cn)是有名的清理软件,正确的使用电脑与分盘无需使用它  
但清理缓存与注册表的功能不失一种选择  
但真的需要清理时,缓存只是杯水车薪  
固态硬盘不分盘+安装软件位置的合理性才是唯一解

任务管理器是管理内存的正解,当我们提到删除一个软件时,往往是它的自启动大量占用系统资源  
右键任务栏/ctrl+shift+esc打开它,可以调整启动项与关闭正在运行的进程  
几乎没有启动项是更推荐的使用方式 (所有启动项都可以关闭,不必顾忌)  
![](https://s2.loli.net/2024/05/21/o7KRpXzBDLrQTGE.png)

如果你希望关闭某个软件 (以便删除它),但找不到,[IObitUnlocker](https://www.iobit.com/en/iobit-unlocker.php)能够帮助你

![](https://s2.loli.net/2024/05/22/y6wGNerOiPz95v8.png)

### 合理的组织文件结构

完全掌握电脑中的文件是入门PC使用的标志  

![](https://s2.loli.net/2024/05/21/qQnOdmv29JGfuUR.png)  

要点是全英文有效的命名+分门别类的位置+合理的结构

具体来说,尽量将应用安装在program files文件夹而非appdate或其他,这能限制应用的权限

## 常用软件与系统安装



### office

office tools plus 安装激活,除三件套外推荐OneDrive,对于文档代码等同步方便  
[下载](https://otp.landian.vip/zh-cn/)  

![](https://s2.loli.net/2024/05/20/yjp6LHcRg1lumCP.png)



