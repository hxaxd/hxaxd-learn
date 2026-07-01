# Lua 基础

## 参考资料

- Codex

## 环境与工程

```sh
lua -v # PUC Lua, 标准实现, 版本可能是 5.1/5.4/5.x 等
luajit -v # LuaJIT, Lua 5.1 语义 + JIT + bit + ffi
lua -e "print(_VERSION)"
luac -p main.lua # 只检查语法, 不执行
```

```lua
local bit = require("bit") -- LuaJIT / Lua 5.1 常见位运算库
print(bit.band(0x0f, 0x33))

local ffi = require("ffi") -- LuaJIT FFI, 直接声明和调用 C 接口
ffi.cdef("int puts(const char *s);")
ffi.C.puts("hello from C")

jit.off() -- 关闭当前函数或后续代码的 JIT, 排查性能/兼容问题时会见到
jit.on()
```

```sh
luarocks search cjson
luarocks install lua-cjson
luarocks list
luarocks show lua-cjson
luarocks remove lua-cjson
```

```lua
local cjson = require("cjson") -- LuaRocks 安装后仍然通过 require 使用
print(cjson.encode({name = "lua"}))
```

- LuaRocks 是 Lua 常用包管理器, 包叫 rock
- 嵌入式场景可能没有包管理器, 依赖由宿主程序直接塞进全局变量或 `package.preload`

## Chunk 和注释

```lua
-- 一个文件, 一段字符串, REPL 输入都是 chunk
-- 单行注释

--[[
块注释
]]

print("hello") -- 语句分隔靠换行
print("lua"); print("ok") -- `;` 可写, 通常省略

local f = load("return 1 + 2") -- 编译字符串 chunk
print(f()) -- 执行编译后的函数
```

## 值, 变量, 作用域

```lua
local n = nil -- nil 表示无值
local b = true -- boolean
local x = 1 -- number, Lua 5.3+ 区分 integer 和 float
local s = "lua" -- string, 不可变字节串
local t = {} -- table, 唯一内置复合结构
local fn = function(a) return a + 1 end -- function 是一等值

g = 1 -- 全局变量, 等价于 _ENV.g = 1
local y = 2 -- 局部变量, 作用域到当前块结束

do
    local y = 3 -- 遮蔽外层 y
end

local a, b = 1, 2
a, b = b, a -- 多重赋值先算右侧, 再统一赋值
local c, d = 1 -- d == nil
local e = 1, 2 -- 2 被丢弃

local k <const> = 1 -- Lua 5.4, 局部常量
-- local r <close> = assert(io.open("a.txt")) -- Lua 5.4, 离开块自动关闭
```

## 表达式和运算符

```lua
local a = 7 / 2 -- 3.5, 浮点除法
local b = 7 // 2 -- 3, 向下取整除法
local c = 7 % 2 -- 1
local d = 2 ^ 3 ^ 2 -- 512, `^` 右结合

local bits = (1 << 4) | 3 -- 位运算: &, |, ~, <<, >>
local inv = ~bits -- `~` 也可作按位取反

local ok = a ~= b and a >= b or false -- 逻辑运算返回原值
local name = input or "anonymous" -- 默认值写法, 但 input == false 时会被覆盖

local text = "lua" .. "!" -- 字符串连接, `..` 右结合
local len = #text -- 字符串长度或序列长度

local same = {} == {} -- false, table 默认按引用比较
```

## 字符串和模式

```lua
local a = "hello\n"
local b = 'hello'
local c = [[
long string -- 长字符串不考虑注释
\n -- 也不转义
]]
local d = [=[ can contain [[ and ]] ]=] -- 内部含有 `[[` 和 `]]` 的长字符串, 用若干成对 `=` 来区分

local path = "a\\b"
local unicode = "\u{4e2d}" -- UTF-8 字节序列

local s = "one two"
for w in s:gmatch("%w+") do -- 等效 string.gmatch(s, "%w+"), 模式匹配
    print(w)
end

local changed = s:gsub("(%w+)", "[%1]") -- 捕获用 `%1`, `%2`
```

```lua
-- Lua pattern 不是正则表达式
-- 字符类: . %a %c %d %g %l %p %s %u %w %x %z, 大写取反如 %D
-- 数量: * + - ?
-- 锚点: ^ $
-- 平衡匹配: %b()
-- frontier: %f[%w]
```

## Table

```lua
local t = {
    "a", -- t[1], Lua 序列习惯从 1 开始
    "b", -- t[2]
    x = 1, -- t["x"]
    ["y-z"] = 2, -- 任意表达式都能当 key
    [10] = "ten",
}

print(table.unpack(t)) -- unpack 序列, 等价于 t[1], t[2], t[3], ...

print(t[1], t.x, t["y-z"])
t.x = nil -- table 字段赋 nil 等于删除字段

local same = t
same[1] = "changed" -- table 是引用语义, 赋值不复制

for i, v in ipairs(t) do
    print(i, v) -- 按 1..n 遍历序列, 遇到第一个 nil 停止
end

for k, v in pairs(t) do
    print(k, v) -- 遍历所有键值, 顺序不保证
end

local n = #t -- 只适合无洞序列
```

```lua
local xs = {}
xs[#xs + 1] = "a" -- 追加元素的基础写法
xs[#xs + 1] = "b"

local dict = {name = "lua", year = 1993}
local key = "name"
print(dict[key]) -- 动态 key 用 []
print(dict.name) -- 固定标识符 key 可用 .
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
    if x == 3 then break end -- 退出最近一层循环
end

repeat
    x = x + 1
until x == 10 -- 至少执行一次, 条件为真时退出

for i = 1, 10, 2 do -- 数值 for: 初值, 终值, 步长
    print(i)
end

for k, v in pairs(t) do -- 泛型 for: 迭代器, 状态, 初值
    print(k, v)
end

goto skip -- Lua 没有 continue, 有时用 goto 模拟
print("ignored")
::skip::
```

## 函数

```lua
local function add(a, b) -- 等价于 local add; add = function(a, b) ... end
    return a + b
end

local function div(a, b)
    if b == 0 then
        return nil, "divide by zero" -- 多返回值常用于 `结果, 错误`
    end
    return a / b
end

local value, err = div(1, 0)
if not value then print(err) end

local function pack(...)
    return {...}, select("#", ...) -- `...` 是可变参数, select 避免 nil 值不被统计
end

local function call_last(f, x)
    return f(x) -- 尾调用, 可复用调用栈
end
```

```lua
local function counter()
    local n = 0
    return function()
        n = n + 1 -- 闭包捕获外层局部变量
        return n
    end
end

local next_id = counter() -- 一个闭包
print(next_id(), next_id()) -- 输出 1 2
```

## 方法, 对象, metatable

```lua
local Account = {} -- 这个 table 当作类, 里面放共享方法
Account.__index = Account -- 实例找不到字段时, 回到 Account 里找

function Account.new(balance)
    local obj = {balance = balance or 0} -- 每个实例自己的状态
    return setmetatable(obj, Account) -- 给实例绑定元表 Account
end

function Account:deposit(n) -- 等价于 function Account.deposit(self, n)
    self.balance = self.balance + n -- self 就是调用者 a
end

local a = Account.new(10)
print(a.balance) -- 10, 字段在实例 a 自己身上
a:deposit(5) -- 等价于 a.deposit(a, 5)
print(a.balance) -- 15

print(a.deposit) -- a 没有 deposit, 触发 __index
```

```lua
local readonly = {}
local data = {x = 1}

setmetatable(readonly, {
    __index = data,

    __newindex = function(t, k, v)
        error("readonly: " .. k) -- 只在写入缺失字段时触发
    end,

    __tostring = function(t)
        return "object"
    end,
})

print(readonly.x) -- 1, 来自 data.x
print(tostring(readonly)) -- object

local ok, err = pcall(function() -- 保护调用, 捕获错误
    readonly.y = 2 -- 报错, 因为 y 是缺失字段
end)
print(ok, err)

rawset(readonly, "y", 2) -- 绕过 __newindex, 直接写入 readonly.y
print(rawget(readonly, "y"))
```

```lua
-- 常见元方法
-- __index: 读不到字段时触发, 可以是 table 或 function
-- __newindex: 写入缺失字段时触发, 已存在字段会直接改
-- __call: 让 table 像函数一样被调用, obj(...)
-- __tostring: tostring(obj) 或 print(obj) 时触发
-- __len: #obj
-- __pairs: pairs(obj)
-- __gc: userdata 被回收时触发
-- __close: <close> 变量离开作用域时触发
-- __add/__sub/__mul/__div/__idiv/__mod/__pow/__unm: 算术
-- __concat: ..
-- __eq/__lt/__le: == < <=
-- __band/__bor/__bxor/__bnot/__shl/__shr: 位运算
-- rawget/rawset/rawequal/rawlen: 绕过元方法, 直接操作原始 table
-- 弱表: setmetatable(t, {__mode = "k"}) 弱键, "v" 弱值, "kv" 都弱
```

## 模块

```lua
local M = {} -- 模块本身就是普通 table
-- 想导出的名字放进 M
-- 不想导出的名字保持 local

local function hidden(x)
    return x * x -- 只在当前文件可见
end

function M.square(x) -- 等价于 M.square = function(x)
    return hidden(x)
end

return M -- require("mathx") 得到的就是这个返回值
```

```lua
local mathx = require("mathx") -- 按 package.path 搜索 mathx.lua
-- 第一次 require 会执行整个文件
-- 文件的 return 值会缓存到 package.loaded

print(mathx.square(4)) -- 调用模块 table 上导出的函数

local again = require("mathx") -- 第二次 require 不再执行文件

package.loaded.mathx = nil -- 清掉缓存后可重新 require, 调试时偶尔用
```

## 环境

```lua
local env = {print = print, x = 1} -- 给 chunk 准备一个独立环境

local chunk = assert(load(
    "print(x); y = 2", -- 这段代码里没有 local 的名字都走 _ENV
    "demo", -- chunk 名字, 常用于报错信息
    "t", -- 只加载文本 chunk
    env -- 把 env 作为这段代码的 _ENV
))

chunk() -- 打印 env.x, 然后写入 env.y
print(env.y) -- 2, 全局写入其实写进当前 _ENV
```

## 协程

```lua
local co = coroutine.create(function()
    coroutine.yield(1) -- 暂停当前协程, 并把 1 作为 resume 的返回值交回主流程
    return 2 -- 协程结束时, 2 也会交回 resume
end)

local ok1, v1 = coroutine.resume(co) -- true, 1

local ok2, v2 = coroutine.resume(co) -- true, 2
local state = coroutine.status(co) -- dead, 已经 return 完
```

```lua
local function range(n)
    return coroutine.wrap(function() -- wrap 返回一个普通函数, 每次调用都会 resume 协程
        for i = 1, n do
            coroutine.yield(i) -- 每次 yield 一个迭代值
        end
    end)
end

for x in range(3) do -- 直到 wrap 返回的函数返回 nil 时结束迭代
    print(x) -- 1, 2, 3
end
```

## 错误处理

```lua
local function read_config(path)
    local f, err = io.open(path) -- io.open 失败时返回 nil, err
    if not f then
        return nil, err -- 可预期失败优先返回 nil, err
    end

    local s = f:read("*a") -- "*a" 表示读取全部内容
    f:close()
    return s -- 成功时只返回结果
end

local ok, result = pcall(function()
    error("bad") -- 抛出错误
end)
-- pcall 捕获错误
-- 成功: true, 返回值...
-- 失败: false, 错误值

local ok2, result2 = xpcall(function()
    error("bad")
end, debug.traceback) -- xpcall 可指定错误处理函数
-- debug.traceback 会生成调用栈
```
