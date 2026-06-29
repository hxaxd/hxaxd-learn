# Lua 基础

## 参考资料

- Programming in Lua
- Lua Reference Manual
- Lua Users Wiki

## 语言气质

- Lua 是一门小而可嵌入的脚本语言, 核心语法很少, 但元表和协程给了它很强的表达力
- Lua 的中心数据结构是 `table`, 数组, 字典, 对象, 模块, 命名空间都由它承担
- Lua 是动态类型, 弱类型倾向较明显, 变量无类型, 值有类型
- Lua 默认变量是全局变量, 写库和大程序时几乎总是优先使用 `local`
- Lua 的运行模型适合配置, 游戏脚本, 插件系统, DSL, 嵌入 C/C++ 程序

## 运行模型

```sh
lua hello.lua
lua -i hello.lua
luac -p hello.lua
```

- Lua 程序单位叫 chunk, 一个文件, 一段字符串, REPL 输入都可以是 chunk
- chunk 被编译成字节码再执行, `load`, `loadfile`, `dofile` 都围绕 chunk 工作
- 语句分隔符可以是换行或 `;`, 通常省略 `;`
- 注释使用 `--`, 块注释使用 `--[[ ... ]]`
- 第一行以 `#` 开头时可作为 shebang 被忽略

## 值与类型

- Lua 基本类型
    - `nil` 表示无值, 也用于删除 table 字段
    - `boolean` 只有 `false` 和 `true`
    - `number` 通常含 integer 和 float
    - `string` 是不可变字节串
    - `function` 是一等值和闭包
    - `table` 是唯一内置复合数据结构
    - `thread` 表示协程
    - `userdata` 表示宿主程序提供的外部对象
- 条件判断中只有 `false` 和 `nil` 为假, `0`, `""`, `{}` 都是真
- `type(x)` 返回类型名字符串

```lua
print(type(nil))      -- nil
print(type(false))    -- boolean
print(type(1))        -- number
print(type("x"))      -- string
print(type({}))       -- table
```

## 变量与作用域

```lua
x = 1                 -- 全局变量, 等价于 _ENV.x = 1
local y = 2           -- 局部变量
local a, b = 1, 2
a, b = b, a           -- 多重赋值

local c <const> = 3   -- Lua 5.4, 只读局部变量
local f <close> = assert(io.open("a.txt"))
```

- 未赋值变量的值为 `nil`
- 局部变量作用域从声明之后开始, 到当前块结束
- 多重赋值先计算右侧, 再统一赋给左侧, 所以可以直接交换变量
- 右侧值少则补 `nil`, 多则丢弃
- 函数调用和 vararg 位于表达式列表最后时可以展开多个返回值
- `_ENV` 是当前 chunk 的环境表, 全局变量实际是环境表字段

## 运算符

```lua
+ - * / // % ^        -- 算术, ^ 右结合
& | ~ << >>           -- 位运算, ~ 也可作按位取反
== ~= < > <= >=       -- 比较
and or not            -- 逻辑
..                    -- 字符串连接, 右结合
#                     -- 长度
```

- `/` 总是浮点除法, `//` 是向下取整除法
- `and` 返回第一个假值或最后一个值, `or` 返回第一个真值或最后一个值
- `a or default` 常用于默认值, 但当 `a == false` 时会误用默认值
- table, function, thread, userdata 默认按引用比较
- `#t` 只适合没有洞的序列, 稀疏数组长度未必符合直觉

## 字符串

```lua
local a = "hello\n"
local b = 'hello'
local c = [[
long string
]]
local d = [=[ can contain [[ and ]] ]=]

print("a" .. "b")
print(("x"):rep(3))
```

- 字符串不可变, 大量拼接优先用 table 收集后 `table.concat`
- 常见转义: `\n`, `\r`, `\t`, `\\`, `\"`, `\'`, `\ddd`, `\xXX`, `\u{XXX}`, `\z`
- 长字符串不会解释转义, 适合 SQL, 模板, 正则替代品等文本
- Lua 字符串按字节处理, Unicode 辅助功能在 `utf8` 库中

## Table

```lua
local t = {
    "a",
    "b",
    x = 1,
    ["y-z"] = 2,
    [10] = "ten",
}

print(t[1])           -- a, Lua 数组习惯从 1 开始
print(t.x)            -- t["x"]
t.x = nil             -- 删除字段
```

- table 构造器同时支持数组部分和哈希部分
- `t.name` 只是 `t["name"]` 的语法糖
- `pairs(t)` 遍历所有键值, 顺序不保证
- `ipairs(t)` 从 1 开始按整数键遍历序列, 遇到第一个 nil 停止
- `next(t, k)` 是底层遍历原语
- table 是引用语义, 赋值和传参不会复制内容

```lua
for k, v in pairs(t) do
    print(k, v)
end

for i, v in ipairs(t) do
    print(i, v)
end
```

## 控制流

```lua
if x < 0 then
    print("negative")
elseif x == 0 then
    print("zero")
else
    print("positive")
end

while x > 0 do
    x = x - 1
end

repeat
    x = x + 1
until x == 10
```

- `if`, `while`, `for`, `function`, `do` 都以 `end` 结束
- `repeat ... until` 的条件为真时退出, 循环体至少执行一次
- `break` 退出最近一层循环
- Lua 没有 `continue`, 常用 `goto` 或重排逻辑替代

```lua
for i = 1, 10, 2 do
    print(i)
end

for k, v in pairs(t) do
    print(k, v)
end

goto skip
print("ignored")
::skip::
```

## 函数

```lua
local function add(a, b)
    return a + b
end

local function pack(...)
    return {...}, select("#", ...)
end

local function div(a, b)
    if b == 0 then
        return nil, "divide by zero"
    end
    return a / b
end
```

- 函数是一等值, 可以存入变量, table, 作为参数和返回值
- 函数可以返回多个值, 常见约定是成功返回结果, 失败返回 `nil, err`
- `...` 表示可变参数, `select("#", ...)` 可得到参数数量
- 尾调用形如 `return f(x)`, Lua 会复用调用栈
- 闭包会捕获外层局部变量, 捕获的是变量而不是值

```lua
local function counter()
    local n = 0
    return function()
        n = n + 1
        return n
    end
end
```

## 方法与对象风格

```lua
local Account = {}
Account.__index = Account

function Account.new(balance)
    return setmetatable({balance = balance or 0}, Account)
end

function Account:deposit(n)
    self.balance = self.balance + n
end

local a = Account.new(10)
a:deposit(5)          -- 等价于 a.deposit(a, 5)
```

- `:` 定义和调用方法时会自动传入 `self`
- Lua 没有 class 关键字, 对象通常由 table + metatable + `__index` 组合实现
- 原型, mixin, 单例模块都能自然用 table 表达

## 元表

```lua
local mt = {
    __index = function(t, k)
        return "missing " .. k
    end,
    __tostring = function(t)
        return "object"
    end,
}

local obj = setmetatable({}, mt)
print(obj.x)
print(tostring(obj))
```

- metatable 定义 table 或 userdata 的特殊行为
- 常用元方法
    - `__index`, 读取缺失字段
    - `__newindex`, 写入缺失字段
    - `__call`, 把值当函数调用
    - `__tostring`, 字符串化
    - `__len`, `#`
    - `__pairs`, `pairs`
    - `__gc`, 回收 userdata
    - `__close`, 关闭 to-be-closed 变量
    - `__eq`, `__lt`, `__le`, 比较
    - `__add`, `__sub`, `__mul`, `__div`, `__idiv`, `__mod`, `__pow`
    - `__unm`, `__band`, `__bor`, `__bxor`, `__bnot`, `__shl`, `__shr`
    - `__concat`
- `rawget`, `rawset`, `rawequal`, `rawlen` 可绕过元方法
- 弱表通过 `__mode = "k"`, `"v"`, `"kv"` 声明弱键或弱值

## 模块

```lua
-- mathx.lua
local M = {}

function M.square(x)
    return x * x
end

return M
```

```lua
local mathx = require("mathx")
print(mathx.square(4))
```

- `require` 搜索并运行模块, 返回模块的返回值
- 模块结果会缓存在 `package.loaded`
- 搜索路径来自 `package.path` 和 `package.cpath`
- Lua 现代模块通常返回一个局部 table, 避免污染全局环境

## 协程

```lua
local co = coroutine.create(function()
    coroutine.yield(1)
    return 2
end)

print(coroutine.resume(co))    -- true 1
print(coroutine.resume(co))    -- true 2
```

- 协程是协作式调度, 只有显式 `yield` 才会让出执行权
- `coroutine.create(f)` 创建协程
- `coroutine.resume(co, ...)` 恢复协程, 返回 `ok, ...`
- `coroutine.yield(...)` 暂停当前协程
- `coroutine.status(co)` 返回 `suspended`, `running`, `normal`, `dead`
- `coroutine.wrap(f)` 返回一个直接调用的恢复函数, 失败时抛错
- 协程常用于生成器, 状态机, 异步框架的底层调度

## 错误处理

```lua
local ok, result = pcall(function()
    error("bad")
end)

local ok2, value = xpcall(function()
    error("bad")
end, debug.traceback)
```

- `error(msg)` 抛出错误
- `assert(v, msg)` 当 `v` 为假时抛错, 否则返回所有参数
- `pcall(f, ...)` 保护调用, 返回 `true, ...` 或 `false, err`
- `xpcall(f, handler, ...)` 可指定错误处理函数
- Lua 没有异常类型层级, 错误值可以是任意值, 通常用字符串或 table

## 标准库总览

### 基础库

- `_G` 全局环境表
- `_VERSION` Lua 版本字符串
- `assert`, `error`, `pcall`, `xpcall`
- `print`, `warn`
- `type`, `tostring`, `tonumber`
- `pairs`, `ipairs`, `next`
- `select`
- `load`, `loadfile`, `dofile`
- `getmetatable`, `setmetatable`
- `rawget`, `rawset`, `rawequal`, `rawlen`
- `collectgarbage`

```lua
local f = assert(load("return 1 + 2"))
print(f())
```

### string

- `string.len`, `#s`
- `string.sub(s, i, j)`
- `string.lower`, `string.upper`
- `string.reverse`, `string.rep`
- `string.byte`, `string.char`
- `string.format`
- `string.find`, `string.match`, `string.gmatch`, `string.gsub`
- `string.dump`
- `string.pack`, `string.unpack`, `string.packsize`

```lua
local name = "lua"
print(string.format("%s %.2f", name, 3.14159))
print(("a=1 b=2"):gsub("%a", string.upper))
```

### 模式匹配

- Lua pattern 不是正则表达式, 但足够轻量
- 字符类: `.`, `%a`, `%c`, `%d`, `%g`, `%l`, `%p`, `%s`, `%u`, `%w`, `%x`, `%z`
- 大写字符类表示取反, 如 `%D`
- 魔法字符: `^$()%.[]*+-?`
- 数量: `*`, `+`, `-`, `?`
- 捕获: `(pat)`
- 锚点: `^`, `$`
- 平衡匹配: `%bxy`
- frontier: `%f[set]`

```lua
for word in ("one two"):gmatch("%w+") do
    print(word)
end
```

### utf8

- `utf8.len(s)`
- `utf8.codes(s)`
- `utf8.codepoint(s, i, j)`
- `utf8.char(...)`
- `utf8.offset(s, n, i)`
- `utf8.charpattern`

```lua
for pos, code in utf8.codes("中文") do
    print(pos, code)
end
```

### table

- `table.concat(t, sep, i, j)`
- `table.insert(t, pos, value)`
- `table.remove(t, pos)`
- `table.move(a1, f, e, t, a2)`
- `table.sort(t, comp)`
- `table.pack(...)`
- `table.unpack(t, i, j)`

```lua
local xs = {3, 1, 2}
table.sort(xs)
print(table.concat(xs, ","))
```

### math

- 常量: `math.pi`, `math.huge`, `math.maxinteger`, `math.mininteger`
- 转换: `math.tointeger`, `math.type`
- 比较: `math.max`, `math.min`, `math.ult`
- 整数和浮点: `math.floor`, `math.ceil`, `math.modf`, `math.fmod`, `math.abs`
- 幂和指数: `math.sqrt`, `math.exp`, `math.log`
- 三角: `math.sin`, `math.cos`, `math.tan`, `math.asin`, `math.acos`, `math.atan`, `math.deg`, `math.rad`
- 随机: `math.random`, `math.randomseed`

### io

- `io.read`, `io.write`
- `io.open(path, mode)`
- `io.lines(path)`
- `io.input`, `io.output`
- `io.flush`
- `io.tmpfile`
- `io.type`
- `io.popen`
- file 方法: `read`, `write`, `lines`, `seek`, `flush`, `close`, `setvbuf`

```lua
local f = assert(io.open("a.txt", "w"))
f:write("hello\n")
f:close()

for line in io.lines("a.txt") do
    print(line)
end
```

### os

- `os.clock`
- `os.date`, `os.time`, `os.difftime`
- `os.execute`, `os.exit`
- `os.getenv`
- `os.remove`, `os.rename`
- `os.tmpname`
- `os.setlocale`

```lua
print(os.date("%Y-%m-%d %H:%M:%S"))
```

### package

- `require`
- `package.loaded`
- `package.preload`
- `package.path`, `package.cpath`
- `package.searchers`
- `package.searchpath`
- `package.loadlib`
- `package.config`

### coroutine

- `coroutine.create`
- `coroutine.resume`
- `coroutine.yield`
- `coroutine.status`
- `coroutine.running`
- `coroutine.wrap`
- `coroutine.isyieldable`
- `coroutine.close`

### debug

- `debug.traceback`
- `debug.getinfo`
- `debug.getlocal`, `debug.setlocal`
- `debug.getupvalue`, `debug.setupvalue`
- `debug.upvalueid`, `debug.upvaluejoin`
- `debug.getmetatable`, `debug.setmetatable`
- `debug.getregistry`
- `debug.getuservalue`, `debug.setuservalue`
- `debug.sethook`, `debug.gethook`
- `debug.setcstacklimit`
- `debug.debug`

- `debug` 能破坏封装和优化假设, 主要用于调试器, 日志, 测试工具

## 惯用法

- 文件开头常写 `local M = {}` 并在结尾 `return M`
- 热路径中把常用全局函数局部化, 如 `local insert = table.insert`
- `nil` 表示缺失, 所以数组中间不要随意放 `nil`
- 用 `pcall` 隔离插件, 配置和用户脚本
- 用 table 表达数据, 用 metatable 表达行为
- 用 coroutine 表达可暂停的流程, 不要把它误当抢占式线程
- Lua 的简洁来自少量机制反复组合, 不是语法糖堆叠
