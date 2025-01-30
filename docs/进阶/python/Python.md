- Python编程 给外行看的... 1

## 解释器
mac自带python,但是一定要自己安装,否则pip安装的包会因为权限用不了

记得alias python与pip

其它系统正常安装即可,win注意加入环境变量
```shell
brew install python

pip install <package> #下载包

pip install --upgrade <package>  # 升级软件包

pip freeze # 查看已安装的内容

pip uninstall <package>  # 卸载包

export PATH=${PATH}:/opt/homebrew/bin/python3
alias python="/opt/homebrew/bin/python3"
alias pip="/opt/homebrew/bin/pip3"

```
## IDE与虚拟环境
推荐使用PyCharm,教育免费  
在py编程中,虚拟环境无疑是我们要关注的,py原生的虚拟环境工具venv足够使用,但如果目的是使用包进行科学研究,第三方的虚拟环境工具要更加易用

比如conda

pycharm支持虚拟环境的快速切换等操作,因此对我足够使用
```bash
python -m venv dir #建立
source ENV_DIR/bin/activate #激活
.\ENV_DIR\Scripts\activate #win激活
deactivate #退出
# 在虚拟环境当中的pip一切如常,会自动下载本环境
```
以上操作pycharm也都可以图形化

## 起步

介绍主流系统中python的安装与在终端和vscode中运行py代码

## 变量和简单的数据类型

- 变量名的规则与c一样,字母,数字与'_'(新版本支持Unicode,为兼容性不建议使用),并不可与关键字/库函数重复
- 对于一个变量,可以用.method()来调用方法
- 字符串可以用单引号或双引号引用,以便在字符串中包含另一个  
常用方法:  
```python
print(...)

# 这些方法都只是返回处理后的结果,而不是永久改变

.title()# 首字母大写
.upper()# 全部大写
.lower()# 全部小写

.len()# 长度
string1+=string2 # 连接字符串

.strip()# 去除首尾空格
.rstrip()# 去除尾部空格
.lstrip()# 去除首部空格

.repace(a,b)# 将字符串中a替换为b
.split(分隔符缺省为' ')# 将字符串分割成列表

.removeprefix(前缀)# 去除前缀
.removesuffix(后缀)# 去除后缀

f"{name}{name}"# 格式化字符串,可以引用变量
```
- 数分整数与浮点数, 整数有加减乘除,乘方运算,字面量中可以加入'_',没有任何影响  
除法运算的结果总是浮点数  
当表达式当中有浮点数,那么结果一定是浮点数  
```python
a=100_000 #注释

a ** b #乘方
a%b # 取余

a,b = 1,2 #同时赋值
```
- py没有常量, 但如果不打算改变一个变量值,我们约定将其标识符用全大写表示

## 列表简介
```python
name=[1,2,3,4] # 打印会显示[1,2,3,4]
#name[0~3]对应4个元素,左右值都能当,也就是说可以修改
name[-1] # 最后一个元素

.append(元素) #在列表末尾添加元素
.insert(位置,元素) #在列表指定位置添加元素

del name[0] #删除列表指定位置的元素

.pop(位置) #删除列表指定位置的元素并返回该元素
.pop() #删除列表末尾的元素并返回该元素

.remove(元素) #删除列表中指定元素

.sort() #排序,默认升序,参数reverse=True降序
sorted(name) #临时排序(不修改原列表)

.reverse() #反转列表

.len() #获取列表长度
```

## 操作列表
```python
for name in 列表name:
    ...
    ... # 缩进代码在循环体中执行
... # 在循环体外执行

# 数值列表的常用方法与函数
range(n1(缺省为0),n2,步长缺省为1) # 生成一个从n1到n2-1的数值列表
name=list(range(n1,n2)) # 将range()的结果转换为列表

name=[i**2 for i in range(1,11)] # 列表推导式

.min() # 最小值
.max() # 最大值
.sum() # 求和

name[:3] # 从列表第一个元素开始,取3个元素
name[3:] # 从列表第四个元素开始,取到最后一个元素
name[-3:] # 从列表倒数第三个元素开始,取到最后一个元素
# 切片也可以用在for in后
name1=name2[:] # 复制列表
name1=name2 # 两个标识符指向同一个列表

# 元组,不可修改的列表
name=(1,2,3)# ()只是看起来好看,真正的标识是依靠,所以至少有一个,
```
- 让文本编辑器输入TAB的时候自动转化成四个空格,而不是在文本当中留下'\t',有利于格式统一

## if语句
```python
if 条件:
    ...
elif 条件:
    ...
else:
    ...
# 条件
a==b # 等于
a!=b # 不等于
a>b # 大于
a<b # 小于
a>=b # 大于等于
a<=b # 小于等于
and # &&
or # ||
not # !
a in b # 判断一个元素是否在列表中/判断a为b的子字符串
a is  b # 判断两个标识符是否指向同一个对象
列表name # 判断列表非空
```

## 字典
```python
# map/哈希表
name={'key1':'value1','key2':'value2'} # 字典的键值对

name['key1'] # 访问
name['key1']='value3' # 修改
name['key3']='value3' # 添加
del name['key1'] # 删除

name.keys() # 获取所有键
name.values() # 获取所有值

name.get(key,若无返回值(缺省为none)) # 获取键对应的值

for key,value in name.items():
    ...

set(name.values()) # 用集合去重
```
- 显然以上这些都是可以嵌套的

## 用户输入和while循环
```python
name=input(提示信息) # 输入字符串
name=int(name) # 转换为整数
name=float(name) # 转换为浮点数

while 条件:
    ...
    break # 跳出循环
    continue # 跳过当前循环
```

## 函数
```python
def 函数名(参数1,参数2=默认值2):
    """这是这个函数的简介注释"""
    ...
    return 结果 # 返回结果

函数名(值1,值2) # 调用函数,参数按照顺序对应
函数名(参数1=值1,参数2=值2) # 调用函数,参数按照名称对应

def 函数名(参数1,*参数): # 可变数量参数,建立一个名为'参数'的元组

def 函数名(**参数): # 关键字参数,建立一个名为'参数'的字典
函数名(参数1=值1,参数2=值2) # 会自动将参数转化为键值对

import 模块名(filename) as 别名 # 导入模块
模块名/别名.函数名(值1,值2) # 调用函数

from 模块名 import 函数名 as 别名 # 导入模块中的函数
函数名/别名(值1,值2) # 调用函数

from 模块名 import * # 导入模块中的所有函数
```
- 有默认值的参数调用函数时可以不传,不传的话就用默认值
- 声明函数时有默认值的参数必须在后
- 传递列表时,可以修改列表,若果不修改,则应复制列表

## 类
```python
class 类名:
    """类的简介注释"""
    def __init__(self,参数1,参数2=123):
        """初始化函数"""
        self.参数1=参数1
        self.参数2=参数2
        self.参数3=1234
    def 函数名(self):
        """函数的简介注释"""
        ...
        ...
        return 结果

my_class=类名(值1,值2) # 实例化类
my_class.函数名() # 调用函数
my_class.参数1 # 访问参数

class 类名(父类名):
    """子类的简介注释"""
    def __init__(self,参数1,参数2):
        """初始化函数"""
        super().__init__(参数1,参数2) # 调用父类(spuerclass)的初始化函数
       ...
       ...
    def 函数名(self):
        """同名函数将覆盖父类函数"""
        ...
        ...
        return 结果

form 模块名 import 类名1,类名2 # 导入模块中的类
... # 同函数
```
- 类名用大驼峰命名法

## 文件与异常
```python
# 文件
from pathlib import Path
path=Path('文件路径') # 不完整路径会在本目录下找
# 注意,这只是定位文件路径,即使这个文件不存在,也不会有任何问题
path.touch() # 创建文件
path.unlink() # 删除文件
path.rename('新文件名') # 重命名文件
path.mkdir() # 创建目录
path.rmdir() # 删除目录

path.exists() # 验证文件是否存在

context=path.read_text().rstrip # 读取文本文件,到达文件尾返回空字符串,因此要去除末尾空格
lines=path.read_text().splitlines() # 读取文本文件,将文本按行分割,返回一个列表

path.write_text(context) # 写入文本文件,会覆盖原文件
path.write_text(context,append=True) # 写入文本文件,不会覆盖原文件

# 异常
try:
    ...
except 异常名: # 使用内置异常,自定义异常需要自行编写对应类
    ...
else:
    ...

pass # 什么也不做,填充代码块,可用于静默失败

# json
import json
path.write_text(json.dumps(数据)) # 将数据写入json文件
name=json.loads(path.read_text()) # 从json文件中读取数据
```

## 测试代码
```python
from 模块名 import 函数名
def 测试函数():
    """测试函数的简介注释"""
    assert 函数名(值1,值2)==值3 # 断言一个布尔表达式

#测试类同理

@pytest.fixture
def 夹具函数():
    """夹具函数的简介注释"""
    ...
    ...
    return 测试参数

def 测试函数(夹具函数):
    """测试函数的简介注释"""
    assert 函数名(夹具函数)==值 # 断言一个布尔表达式

# 夹具函数会统一返回真正的参数,方便一口气测试很多函数并更改用例

```
- 用pip安装pytest库
- 测试代码文件所在目录下终端执行pytest,自动测试

## 第二部分--三个项目

不记录