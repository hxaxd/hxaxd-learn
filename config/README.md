# 终端配置

按目标系统选用，文件部署到对应用户目录。

| 系统 | 仓库文件 | 部署位置 |
| --- | --- | --- |
| macOS | `mac.wezterm.lua` | `~/.wezterm.lua` |
| Windows | `win.wezterm.lua` | `%USERPROFILE%/.wezterm.lua` |
| macOS | `mac.zshrc` | `~/.zshrc` |
| Linux | `linux.zshrc` | `~/.zshrc` |
| WSL | `wsl.zshrc` | `~/.zshrc` |

## zsh

- 使用 Oh My Zsh、Powerlevel10k，以及配置中的插件和命令工具。
- 三个系统各自保留完整配置，项目依赖由项目环境管理。
- Conda 按需在当前会话初始化或使用 `conda run`，不随 Shell 启动自动初始化。
- 首次使用运行 `p10k configure`，生成本机的 `~/.p10k.zsh`；个人布局在首次配置时选择，仓库不提供预设模板。
- macOS 按已有 Homebrew 安装位置定位 LLVM 与 ccache；WSL 过滤从 Windows 导入的临时 fnm 会话路径。
