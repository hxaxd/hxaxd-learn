> 将时间花在你的开发环境上是最节省时间的举措

## vscode

|MAC|WIN|
:----:|:----:|
|Ctr|win|
|opt|Alt|
|cmd|ctr|

### 命令面板

- vsc命令以及插件的命令都会在命令面板中呈现 `cmd+shift+p`
- vsc有新手引导,命令面板也有大量help
- `cmd+p`可以快速打开文件(尝试反复按) 输入? 可以查看推荐命令
- 点右箭头也可以打开
- `edu/term`加' '即可打开编辑器/终端
- Configure Display Language”命令修改界面自然语言(需要先下载语言插件)

### 编辑器

界面

- `cmd+b` 切换侧边栏
- `cmd+j` 切换面板
- `ctr+enter` 在新窗口打开
- `cmd+\` 分屏 `cmd+1/2/3` 换分屏
- `shift+cmd+e` 换到资源管理器
- `ctr+TAB` 历史记录 `ctr+-`向前  `ctr+-+shift` 向后
- `shift+click` 多选文件(explorer)中
- `cmd+opt+f` 搜索文件

代码

- 当vsc提醒你可以修改代码(小灯泡) `cmd+space`快速打开
- `shift+cmd+m` 跳转到err
- `cmd+click(点击代码中的文件)` 转到
- `opt+click` 添加多光标
- `shift+cmd+l` 选中当前标识符的所有实例 `cmd+d` 逐个
- `shift+opt` 垂直选中
- `opt+cmd+up/down` 向上/下移动一行
- `ctr+opt+up/down` 向上/下复制一行
- `shift+cmd+o` 转到文件
- `ctr+g` 跳转到行
- `cmd+u` 回退光标位置
- `opt+cmd+ [ / ] ` 折叠代码
- `cmd+up/down` 顶/底
- `shift+cmd+v` md预览
- `opt+F12` 暂时转到源码 `F12` 转到 `shift+F12`转到资料
- `F2` 重命名
- `opt+cmd+R` 正则替换

`cmd+k`

- `cmd+k z` zen 模式
- `cmd+k f`关闭当前文件
- `ctr+k ctr+x` 修剪空格
- `cmd+k cmd+c` 注释
- `cmd+k o`分离窗口
- `cmd+k shift+cmd+\` 分屏

### 插件

- `shift+cmd+x` 插件界面
- 我推荐`one dark pro darker`主题
- `error lens` 可以显示错误
- 关键软件/语言配套的插件
- `vscode-icons` 图标主题
- `markdown all in one` 可以预览markdown
- `MarsCode AI` 豆包
- `path intellisense` 路径补全

### 终端

- vscode内置终端,实现编译的插件本质都是快捷命令
- `ctr+反引号` 打开终端
- `cmd+click` 点击终端的输出直接转到
- `cmd+up/down` 上下转命令
- `ctr+shift+反引号` 打开另一个终端
- `shift+cmd+[/]` 切换终端

### 设置

- 打开设置 `cmd+,` 亦可直接修改`settings.json`
- 工作区设置仅应用于局部(本工作区)
- 会在根目录下建立`.vscode`文件夹保存
- 详见官方文档

主流快捷键  
Vim  
Sublime  
Emacs  
Atom  
Brackets  
Eclipse  
Visual Studio  


## clion

> jetbrains的IDE通用功能与快捷键高度统一,且大部分功能易用,设置齐全
> 但亦要注意不同语言的特色功能,如C/C++的动态软件分析/内存堆,Python的框架插件
> 不会记录所有,因为它太强大了

- Key Promoter X 快捷键提示插件

### 命令面板

- `cmd+shift+a` 查找命令
- `ctr+反引号` 快速切换
- `double shift` 全局搜索

### 设置

- `cmd+,` 打开设置

### 编辑器

coding

- `opt+enter` 快速修复
- `ctr+n` 快速生成
- `ctr+j` 实时模版
- `ctr+.` 快速补全
- `opt+F7` 显示使用方法
- `double ctr` 输入命令运行
- `ctr+r`运行
- `opt+up/down` 修改选中范围
- `cmd+/` 注释
- `cmd+opt+/` 行内注释
- `ctr+shift+F12` 最大显示编辑器
- `ctr+TAB` 跳转器
- `shift+enter` 在当前行下方插入新行 `cmd+opt+enter` 新行上方
- `cmd+d` 复制一行
- `cmd+backspace` 删除一行
- `opt+shift+up/down` 移动一行

debug

- `ctr+d` 调试
- `cmd+shift+opt+i` 快速静态分析
- `opt+F8` 调试时计算值
- `cmd+F8` 切换断点
- `F8` 单步跳过
- `F7` 步进
- `cmd+F2` 停止
- `cmd+opt+r` 恢复

view code

- `F10` 切换头/源
- `cmd+B+(opt)` 转到声明(定义)
- `cmd+7` 显示文件结构
- `cmd+h+(opt)` 显示类(调用)层次
- `opt+shift+h` 查看import层次
- `cmd+e` 显示最近文件