# Nginx

## 参考资料

## 概念

- Nginx 是一个开源的 WEB 服务器, 它可以作为负载均衡器, 缓存服务器, 反向代理服务器等角色使用
- 反向代理的作用是将客户端的请求转发给后端的服务器, 然后将后端服务器的响应返回给客户端 这样可以实现负载均衡 (多个实际服务器), 并隐藏后端服务器的 IP 地址
    - 可以配置轮询, 加权轮询, ip_hash 等策略
- Nginx 采用主从架构, 一个 Master 进程和多个 Worker 进程 (配置文件中指定)
- 通过虚拟主机的方式实现一服务器可以提供多个网站
- 配置 SSL 证书实现 https 访问

## 命令

```bash
nginx -s signal # 发送信号给 nginx 进程
# 常用信号
# stop 快速停止 nginx 服务器
# quit 正常停止 nginx 服务器
# reload 重新加载配置文件, 新配置生效
# reopen 重新打开日志文件

ngingx -t  # 检查配置文件状态

ps aux|grep nginx  # 查看 nginx 进程
```

## 配置文件

- conf 目录下的 nginx.conf, 默认配置的 nginx 监听的端口为 80

```text
# 最外层是一些全局配置

events {
    # 网络连接配置
}

http {
    # 可以配置多个 server 块, 每一个都是一个虚拟主机

    include path; # 引入其他配置文件

    # 可以配置证书, 实现 https 访问

    # 反向代理
    upstream 代理名字 {
        # 配置...
        ip_hash; # 开启 ip_hash 模式
        # 用户的请求根据其 ip 地址进行 hash 计算, 然后将请求分配到固定的后端服务器

        server 服务器地址 weight = 10;
        server 服务器地址 weight = 20;
    }

    server {
        # 配置...

        server_name 域名; # 配置域名

        # 配置 http 请求重定向到 https

        # 匹配 url 路径
        location / { # 匹配根路径
        root 相对路径; # 文件的目录
        index 默认索引文件.html;        
        }

        location /name { 
            proxy_pass http://代理名字;
        }
    }
}
```

## 防火墙

- 若无法访问, 可能是防火墙没有开启端口
- firwall-cmd: 是 Linux 提供的操作 firewall 的一个工具
- --permanent: 表示设置为持久
- --add-port: 标识添加的端口

```bash
service firewalld start # 启动防火墙
service firewalld restart # 重启防火墙
service firewalld stop # 停止防火墙
firewall-cmd --list-all # 查看防火墙规则
firewall-cmd --query-port=8080/tcp # 查询端口是否开放
firewall-cmd --permanent --add-port=80/tcp # 开放 80 端口
firewall-cmd --permanent --remove-port=8080/tcp # 移除端口
firewall-cmd --reload # 重启防火墙 ( 修改配置后要重启防火墙 )
```

## 替代方案

### Caddy

- 与 Nginx 相比, Caddy 的最大优势在于其开箱即用的自动化特性, 尤其是自动配置和管理 SSL 证书(通过 Let's Encrypt)
- Caddy 采用单进程架构, 通过内置的 Go runtime 实现高并发处理能力, 无需手动配置 worker 进程

#### 配置示例

```caddy
# 基本静态站点服务
example.com {
    root * /var/www/html
    file_server
}

# 反向代理配置
api.example.com {
    reverse_proxy 127.0.0.1:8080
}

# 多个后端的负载均衡
service.example.com {
    reverse_proxy 192.168.1.10:8080 192.168.1.11:8080 {
        lb_policy round_robin
    }
}
```

#### 常用命令

```bash
caddy run            # 启动 Caddy 服务器
caddy stop           # 停止 Caddy 服务器
caddy reload         # 重新加载配置文件
caddy validate       # 验证配置文件的正确性
caddy adapt --config Caddyfile --pretty # 将 Caddyfile 转换为 JSON 格式配置（用于高级配置）
```
