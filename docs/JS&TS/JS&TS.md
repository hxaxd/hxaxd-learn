# JS&TS

## 参考资料

- Codex

## 总览

- 浏览器里的 JavaScript = ECMAScript + DOM/BOM/Web API
- Node.js 里的 JavaScript = ECMAScript + 文件系统/网络/进程等服务端 API
- TypeScript 是 JavaScript 的超集, 核心价值是给 JavaScript 加上静态类型检查
- TypeScript 的类型默认只在编译期存在, 运行时执行的仍然是 JavaScript

## 环境与工具

### package.json

```json
{
  "name": "demo",
  "version": "0.1.0",
  "type": "module",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "tsc --noEmit && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "check": "tsc --noEmit",
    "format": "biome format --write .",
    "lint": "biome check ."
  },
  "dependencies": {
    "axios": "^1.0.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "typescript": "^5.0.0",
    "vite": "^7.0.0",
    "vitest": "^3.0.0"
  }
}
```

- `"type": "module"` 表示 `.js` 文件默认按 ESM 解释
    - 如果没有 `"type": "module"`, Node.js 通常把 `.js` 当作 CommonJS
    - `.mjs` 总是 ESM
    - `.cjs` 总是 CommonJS
- `"scripts"` 里的命令可以通过 `npm run name` 或 `pnpm name` 执行

### TypeScript 工具

```bash
npm install -D typescript tsx @types/node
npx tsc --init # 生成 tsconfig.json
npx tsc --noEmit # 检查类型, 不输出 JS
npx tsc --watch --noEmit # 持续检查类型, 不输出 JS
npx tsx src/index.ts # 直接运行 TS 文件, 适合脚本和开发期命令
```

## JS 语言基础

### 模块

#### ESM

```js
// math.js
export const PI = 3.14;

export function add(a, b) {
    return a + b;
}

export default function square(x) {
    return x * x;
}
```

```js
// main.js
import square, { PI, add } from "./math.js";
import * as math from "./math.js";

console.log(square(3), PI, add(1, 2), math.PI);
```

- `export` 导出命名成员
- `export default` 导出默认成员
- `import { a }` 部分导入
- `import a` 默认导入
- `import * as a` 命名空间导入

动态导入:

```js
const mod = await import("./heavy.js");
mod.run();
```

#### CommonJS

```js
// math.cjs
function add(a, b) {
    return a + b;
}

module.exports = { add };
```

```js
// main.cjs
const { add } = require("./math.cjs");
console.log(add(1, 2));
```

- CommonJS 是运行时加载, ESM 是静态模块结构

## 异步编程

### 回调

```js
setTimeout(() => {
    console.log("later");
}, 1000);
```

### Promise

```js
const p = new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve("ok");
 // reject(new Error("bad"));
    }, 1000);
});

p.then((value) => {
    console.log(value);
}).catch((err) => {
    console.error(err);
}).finally(() => {
    console.log("done");
});
```

### async/await

```js
async function loadUser() {
    try {
        const res = await fetch("/api/user");

        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);
        }

        const data = await res.json();
        return data;
    } catch (err) {
        console.error(err);
        throw err;
    }
}
```

- `async/await` 是 Promise 的同步写法

### Promise 组合

```js
const [user, posts] = await Promise.all([ // 全部成功才成功, 任意失败就失败
    fetchJson("/api/user"),
    fetchJson("/api/posts"),
]);

const results = await Promise.allSettled(tasks.map((task) => task())); // 等全部结束, 不管成功失败

const first = await Promise.race([ // 第一个 settled 的结果
    fetchJson("/api/user"),
    fetchJson("/api/posts"),
]);

const firstSuccess = await Promise.any([ // 第一个 fulfilled 的结果
    fetchJson("/api/user"),
    fetchJson("/api/posts"),
]);
```

### 事件循环

- JS 主执行线程一次只执行一个调用栈
    - 异步 I/O 完成后, 回调会进入任务队列
    - Promise 回调属于 microtask
- `setTimeout` 等属于 task
    - 每次执行完 task 后, 会先清空 microtask 队列, 再进入下一轮 task

## 网络请求

### ajax 与 XHR

- 太老了

### fetch

```js
const res = await fetch("/api/user");
if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
}

const data = await res.json();
```

- `fetch` 基于 Promise
- `res.json()` 本身也是异步

### axios

```js
import axios from "axios";

const client = axios.create({
    baseURL: "/api",
    timeout: 5000,
});

client.interceptors.request.use((config) => {
    config.headers.Authorization = `Bearer ${getToken()}`;
    return config;
});

client.interceptors.response.use(
    (res) => res.data,
    (err) => Promise.reject(err),
);

const user = await client.get("/user");
```

## TypeScript 基础

### 类型系统

- TypeScript 在编译期检查 JavaScript
- TypeScript 类型不会自动变成运行时校验
- `string`: 字符串
- `number`: 数字
- `boolean`: 布尔
- `bigint`: 大整数
- `symbol`: 唯一标识
- `null` 和 `undefined`: 空值
    - `typeof null` 是 `"object"`
- `any`: 跳过类型检查, 会污染后续代码
- `unknown`: 安全版 any, 使用前必须缩小类型
- `never`: 永远不会出现的值
- `void`: 函数没有有意义返回值

### 数组与元组

```ts
const names: Array<string> = ["Ada", "Grace"];

const point: [number, number] = [10, 20];
const entry: readonly [string, number] = ["age", 20]; // 禁止修改
```

### 对象类型

```ts
type User = {
    readonly id: number;
    name: string;
    email?: string; // 可选属性
};

const user: User = {
    id: 1,
    name: "Ada",
};
```

```ts
type Dict = {
    [key: string]: string; // 索引签名
};

const headers: Dict = {
    Accept: "application/json",
};
```

```ts
type Role = "admin" | "user";
type PermissionMap = Record<Role, string[]>;

// PermissionMap = {
//     admin: string[];
//     user: string[];
// };
```

### interface 与 type

```ts
interface User {
    id: number;
    name: string;
}

type Point = {
    x: number;
    y: number;
};
```

### 联合类型

```ts
type ID = string | number; // 可以是字符串或数字

function printId(id: ID) {
    if (typeof id === "string") {
        console.log(id.toUpperCase());
    } else {
        console.log(id.toFixed(0));
    }
}
```

### 交叉类型

```ts
type Timestamped = {
    createdAt: string;
};

type User = {
    id: number;
    name: string;
};

type UserRecord = User & Timestamped; // 同时拥有 User 和 Timestamped 的属性
```

### 类型缩小

- TypeScript 根据运行时判断, 把宽类型收窄成更具体的类型; 这叫 narrowing
- 常见缩小方式:
    - `typeof`: `typeof x === "string"` 判断是否是某种原始类型
    - `instanceof`: 判断对象是否是某个类
    - `"key" in obj`: 判断对象是否有某个属性
    - `Array.isArray(...)`: 判断值是否是数组
    - `x !== null`: 排除 `null`, 常和 `typeof x === "object"` 搭配

### 类型断言

```ts
const input = document.querySelector("input") as HTMLInputElement | null; // 类型断言, 告诉 TS 这个值是 HTMLInputElement 或 null
const root = document.querySelector("#root")!; // 非空断言, 告诉 TS 这个值不可能是 null

const routes = ["home", "settings"] as const; // 收窄成字面量只读类型
type Route = (typeof routes)[number]; // "home" | "settings"
```

```ts
type Config = {
    mode: "dev" | "prod";
    port: number;
};

const config = {
    mode: "dev",
    port: 3000,
} satisfies Config; // satisfies 检查 config 是否满足 Config 类型, 但不会改变 config 的可能更精确类型
```

### 泛型

泛型是类型占位符, 调用时或推断时才确定具体类型.

```ts
function identity<T>(value: T): T {
    return value;
}

function getId<T extends { id: string | number }>(value: T) {
    return value.id;
}

type ApiResponse<T = unknown> = {
    code: number;
    data: T;
};
```

### 函数类型

```ts
type Handler = (event: MouseEvent) => void;

function greet(name: string, title?: string) { // 可选参数
    return title ? `${title} ${name}` : name;
}

function connect(port = 3000) { // 默认参数并且根据默认值推断类型
    return port;
}
```

```ts
// 函数重载
function parse(input: string): string[];
function parse(input: string[]): string;
function parse(input: string | string[]) {
    return Array.isArray(input) ? input.join(",") : input.split(",");
}
```

### 类与修饰符

```ts
// 类似 CPP
class User {
    protected role = "user";

    constructor(
        public readonly id: number, // 只读属性, 只能在构造函数里赋值
        public name: string,
        private token: string,
    ) {}
}

class Admin extends User {
    ban() {
        return this.role;
    }
}
```

```ts
abstract class Shape {
    abstract area(): number;
}
```

### 工具类型

- 基于已有类型生成新类型

```ts
type User = {
    id: number;
    name: string;
    email?: string;
};

type UserPatch = Partial<User>; // 把所有字段变可选: { id?: number; name?: string; email?: string }
type CompleteUser = Required<User>; // 把所有字段变必选: email 也必须有
type FrozenUser = Readonly<User>; // 把所有字段变只读: 不能重新赋值 user.name
type UserPreview = Pick<User, "id" | "name">; // 只保留指定字段: id, name
type UserPublic = Omit<User, "email">; // 排除指定字段: 去掉 email
type UserMap = Record<string, User>; // 构造键值表: 任意 string key -> User value
```

```ts
// 联合类型处理
type Role = "admin" | "user" | "guest";

type NormalRole = Exclude<Role, "admin">; // 从联合类型中排除: "user" | "guest"
type GuestRole = Extract<Role, "guest">; // 从联合类型中提取: "guest"
type RealUser = NonNullable<User | null | undefined>; // 排除 null 和 undefined: User
```

```ts
// 函数类型提取
async function fetchUser(id: string) {
    return { id, name: "Ada" };
}

type FetchUserParams = Parameters<typeof fetchUser>; // 参数元组: [id: string]
type FetchUserReturn = ReturnType<typeof fetchUser>; // 返回类型: Promise<{ id: string; name: string }>
type UserData = Awaited<FetchUserReturn>; // Promise 最终值: { id: string; name: string }
```

### 类型声明文件

```ts
// global.d.ts
declare global {
    interface Window {
        app: { version: string };
    }
}

export {};
```

### 枚举与字面量联合

```ts
type Direction = "up" | "down"; // 字面量联合类型, 不会有运行时代码 (不同于 enum)

const Direction = {
    Up: "up",
    Down: "down",
} as const; // 运行时对象, 字面量联合类型

type DirectionValue = (typeof Direction)[keyof typeof Direction];
```
