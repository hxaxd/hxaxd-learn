# MySQL 使用基础

## 参考资料

- MySQL 必知必会 - 跟前作几乎一样, 单拿出来比前作强, 因为有 MySQL 内容 - 4

### 使用 MySQL

- MySQL 除了本体外, 还提供了命令行工具, 图形化工具 (不好用), 以及数据库管理工具
    - 当然, 本质上都是 SQL 语句
- 想要使用这些工具必须连接到 MySQL 需要指定
    - 主机名 (本地是 localhost)
    - 端口号 (默认是 3306)
    - 用户名 (数据库可以创建不同权限的用户)
    - 密码 (可以没有)
- 下面列举一些图形化界面工具使用的语句 (全没用!!!)

```sql
SHOW DATABASES; -- 查看所有数据库

SHOW TABLES; -- 查看当前数据库中的所有表

SHOW COLUMNS FROM table_name; -- 查看表的所有列
DESCRIBE table_name; -- 同上

SHOW STATUS; -- 查看数据库的状态

SHOW CREATE TABLE table_name; -- 查看表的创建语句
SHOW CREATE DATABASE database_name; -- 查看数据库的创建语句

SHOW GRANTS; -- 查看用户的权限

SHOW ERRORS; -- 查看错误信息
SHOW WARNINGS; -- 查看警告信息
```

### 用正则表达式进行搜索

- `REGEXP` 的使用看起来很像 `LIKE`, 但请注意 `LIKE` 匹配的是整个字符串, 而 `REGEXP` 匹配的是模式 (子串)
- MySQL 的正则表达式不区分大小写
- `^` 指定后一个模式匹配字符串的开始
- `$` 指定前一个模式匹配字符串的结束
- `*` 匹配任意长度的字符
- `+` 匹配至少一个字符
- `?` 匹配零或一个字符
- `{n}` 匹配 n 个 `{n}` 前面的模式
- `{n, }` 匹配至少 n 个 `{n, }` 前面的模式
- `{n, m}` 匹配 n 到 m 个 `{n, m}` 前面的模式
- `[]` 匹配任意字符中的一个
- `[^]` 匹配任意字符中的一个 (取反)
- `|` 逻辑或, 连接两个模式
- `()` 分组
- `\\` 转义
- `[:classname:]` 匹配字符类
    - `[:alnum:]` 字母和数字
    - `[:alpha:]` 字母
    - `[:blank:]` 空格和制表符
    - `[:cntrl:]` 控制字符
    - `[:digit:]` 数字
    - `[:graph:]` 可打印字符
    - `[:lower:]` 小写字母

```sql
SELECT * FROM table_name WHERE column_name REGEXP '正则表达式'; -- 正则表达式搜索
```

### 全文本搜索

- MySQL 支持多种数据引擎, 其中 MyISAM 支持全文本搜索, 更常用的 InnoDB 不支持
- 没用的东西 (FOR WEB DEV)

```sql
-- 创建表时指定全文本搜索
FULLTEXT(列名)

-- 使用
SELECT * FROM table_name WHERE MATCH(column_name) AGAINST('搜索关键字'); -- 不区分大小写, 搜索子串
-- 注意, 全文本搜索会给结果按匹配度(子串出现的先后)排序

-- 查询拓展
SELECT * FROM table_name WHERE MATCH(column_name) AGAINST('搜索关键字' WITH QUERY EXPANSION);  -- 将结果作为关键字搜索

-- 布尔搜索
SELECT * FROM table_name WHERE MATCH(column_name) AGAINST('+搜索关键字 1 -搜索关键字 2' IN BOOLEAN MODE); -- 搜索 关键字 1 出现, 搜索 关键字 2 不出现
-- 有许多符号可以使用
```

### 创建和操纵表

- 表间可以混用引擎, 但不支持外键
- MYISAM 支持全文本搜索 InnoDB 支持事务处理, MEMORY 是存在于内存中的 MYISAM

```sql
CREATE TABLE 表名(列名 1 数据类型 NOT NULL, 列名 2 数据类型, ...)ENGINE=InnoDB; -- 指定引擎

列名 数据类型 NOT NULL AUTO_INCREMENT; -- 指定自增列 (行间值唯一)(有个全局变量, 每次自增 1 作为默认值)
-- 但也可以在 INSERT 中指定 (相当于改变变量值, 以此自增)

SELECT last_insert_id(); -- 获取最后一次插入的自增列的值
```

### 创建存储过程

- 参数名前的 `IN`, `OUT`, `INOUT` 指定参数的类型 (传入, 传出, 传入传出)
- MySQL 的变量名必须以 `@`开头
    - `SELECT ... INTO @变量名;` 赋值
    - `SET @变量名=值;` 赋值
    - `SELECT @变量名;` 查看值

```sql
CREATE PROCEDURE 存储过程名(IN 参数 1 数据类型, OUT 参数 2 数据类型, INOUT ...)COMMENT '注释' -- 会在 SHOW PROCEDURE STATUS 中显示
BEGIN
    -- 存储过程体
    IF 条件 THEN
        -- 语句
    END IF;
END;

CALL 存储过程名(123456, @AAAA, ...); -- 调用存储过程

DROP PROCEDURE 存储过程名; -- 删除存储过程

SHOW PROCEDURE STATUS; -- 查看所有存储过程的信息
```

### 触发器

- 触发器是特殊的存储过程, 当它依托的表发生特定操作 (插入 / 更新) 时, 会自动执行
- `BEFORE`/`AFTER` 指定触发器在事件之前 / 之后执行
    - `BEFORE` 触发器如果执行失败, 则事件不会发生

```sql
CREATE TRIGGER 触发器名 BEFORE/AFTER INSERT/UPDATE/DELETE ON 表名 FOR EACH ROW 行为 -- FOR EACH ROW 表示行为针对每一行 INSERT/UPDATE/DELETE
-- 行为可以是语句 / BEGIN END 块

DROP TRIGGER 触发器名; -- 删除触发器
```

#### `INSERT`触发器

- 新行的信息可以通过 `NEW` 虚拟表访问
    - 可以修改新行的信息

#### `DELETE`触发器

- 旧行的信息可以通过 `OLD` 虚拟表访问
    - 不可修改旧行的信息

#### `UPDATE`触发器

- 上面俩的融合

### 字符集与校对顺序

- Cast ()/Convert () 可以临时转换字符串字符集

```sql
SHOW CHARACTER SET; -- 查看所有字符集

SHOW COLLATION; -- 查看所有校对顺序

CREATE TABLE 表名(列名 1 数据类型 DEFAULT CHARACTER SET 字符集 COLLATE 校对顺序, 列名 2 数据类型)DEFAULT CHARACTER SET 字符集 COLLATE 校对顺序; -- 指定列/全局字符集和校对顺序
```

### 用户管理

- MySQL 中有一个 mysql 数据库, 其中有一个 user 表, 它的 user 列存储了所有用户账号
- 用户名后可以加上 `@主机名`指定用户的主机名, 如果省略则表示用户可以从所有主机访问

```sql
CREATE USER 用户名 IDENTIFIED BY '密码'; -- 创建用户
RENAME USER 用户名 TO 新用户名; -- 重命名用户
DROP USER 用户名; -- 删除用户

SHOW GRANTS FOR 用户名; -- 查看用户的权限

GRANT 权限 1, 权限 2 ON 数据库.表 TO 用户名; -- 授予用户权限
REVOKE ALL 权限 FROM 用户名; -- 撤销用户权限
-- 可以是 ALL 或 ON ...

SET PASSWORD FOR 用户名=密码; -- 设置用户密码
```

### 数据库维护

- 备份的最佳方式还是使用备份工具
- `data` 目录中有许多日志文件
    - `hostname.err` 错误日志
    - `hostname.log` 查询日志
    - `hostname-slow.log` 慢语句日志 (用于记录执行时间超过 `long_query_time` 的语句)
    - `hostname-bin` 二进制日志
    - `FLUSH LOGS` 刷新缓存
    - 文件名可以指定

```sql
FLUSH TABLES; -- 刷新缓存

BACKUP TABLE 表名 TO '文件路径'; -- 备份表
SELECT * FROM 表名 INTO OUTFILE '文件路径'; -- 备份表
RESTORE TABLE 表名 FROM '文件路径'; -- 恢复表

ANALYZE TABLE 表名; -- 分析表状态
-- 类似的有许多, 不列举
```

### 性能优化

- 调整内存分配 / 缓冲区大小等
- 禁止低性能进程
- 编写高效的 SQL 语句 (`EXPLAIN` 可以查看 `SELECT` 语句的执行细节)
- 使用存储过程 / 触发器
- 建立正确的表结构
- 导入数据时关闭自动提交 / 索引
- 使用索引强化读性能 (但它会降低写性能)
- `UNION` > `OR`

#### 数据类型

- 字符串
    - `CHAR(1~255)` 定长字符串
    - `TEXT` 变长字符串 (最大 64K)
    - `MEDIUMTEXT` 变长字符串 (最大 16k)
    - `LONGTEXT` 变长字符串 (最大 4G)
    - `TINYTEXT` 变长字符串 (最大 255 字节)
    - `VARCHAR(n)` 变长字符串 (最大 n 字节, n 最大为 255)
    - `ENUM` 接受一个预定义的集合 (最多 64K 个值) 中的一个值
    - `SET` 接受一个预定义的集合 (最多 64 个值) 中的一个子集
    - 变长串慢且不支持索引
- 整数
    - `BIT` 1~64 位
    - `TINYINT` 1 字节
    - `SMALLINT` 2 字节
    - `MEDIUMINT` 3 字节
    - `INT` 4 字节
    - `BIGINT` 8 字节
    - 前加 `UNSIGNED` 为同字节无符号整数
- 浮点数
    - `REAL` 4 字节
    - `FLOAT` 单精度
    - `DOUBLE` 双精度
    - `DECIMAL(总位数, 小数位数)` 可变精度
- 布尔
    - `BOOL` 1bit
- 日期
    - `DATE`YYYY-MM-DD (1000-9999)
    - `TIME`HH:MM:SS
    - `DATETIME` 日期和时间
    - `TIMESTAMP` 小范围的 `DATETIME`
    - `YEAR` 2 位 (1970-2069) / 4 位 (1901-2155)
- 二进制
    - `BLOB`64K
    - `MEDIUMBLOB`16M
    - `LONGBLOB`4G
