# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# ==================== 1. Oh My Zsh 核心 ====================
export ZSH="$HOME/.oh-my-zsh"

# 皮肤：Powerlevel10k (目前地表最强)
ZSH_THEME="powerlevel10k/powerlevel10k"

# 插件选择：
# git: 基础
# extract: 输入 x 文件名，自动解压任何格式
# zoxide: 2025年替代 cd 的神器
# zsh-autosuggestions: 自动补全（不过时，必装）
# zsh-syntax-highlighting: 语法高亮（不过时，必装）
# sudo: 按两下 ESC 自动帮你在命令前加 sudo
plugins=(
    git 
    extract 
    zoxide 
    sudo
    zsh-autosuggestions 
    zsh-syntax-highlighting
    you-should-use
    thefuck
)

# [fzf] - 模糊搜索神器，按 Ctrl+R 搜历史记录快到飞起
# 2025年官方推荐：一行命令加载所有快捷键(R/T/C)和补全
source <(fzf --zsh) 

source $ZSH/oh-my-zsh.sh

# ==================== 3. 2025 墙裂推荐的现代插件初始化 ====================

# uv 自动补全
eval "$(uv generate-shell-completion zsh)"
# [zoxide] - 现代化的 cd，它能记住你常去的目录
# 安装：brew install zoxide
eval "$(zoxide init zsh)"

eval $(thefuck --alias)

# FZF 默认参数：加入预览窗格、圆角边框、Tokyo Night 配色
export FZF_DEFAULT_OPTS="--height 40% --layout=reverse --border --inline-info \
--color=bg+:#283457,bg:#16161e,spinner:#ff007c,hl:#bb9af7 \
--color=fg:#c0caf5,header:#ff007c,info:#7aa2f7,pointer:#7dcfff \
--color=marker:#9ece6a,fg+:#7dcfff,prompt:#7aa2f7,hl+:#bb9af7"

export FZF_DEFAULT_COMMAND='fd --type f --strip-cwd-prefix --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"

# 3. 专门为 Alt+C 配置目录搜索
# --type d: 只找文件夹
export FZF_ALT_C_COMMAND='fd --type d --hidden --strip-cwd-prefix --exclude .git'

# 4. 让补全功能也用 fd
_fzf_compgen_path() {
  fd --hidden --follow --exclude ".git" . "$1"
}
_fzf_compgen_dir() {
  fd --type d --hidden --follow --exclude ".git" . "$1"
}

# ==================== 4. 实用别名 (Alias) ====================
alias cls='clear'
alias ..='cd ..'
alias ...='cd ../..'
alias lg='lazygit'  # 如果你装了的话，非常推荐
alias cat='bat'     # 现代版的 cat (brew install bat)
alias lt='eza --tree --icons' # 树状显示目录结构
# 现代工具替换
alias df='duf'
alias du='dust'
alias top='btop'
alias ping='gping'
alias ps='procs'
alias dig='doggo'
alias hex='hexyl'

# 推荐安装 eza 代替 ls (brew install eza)
# 它能在终端显示非常漂亮的图标
alias ls='eza --icons --group-directories-first'
alias ll='eza -lh --icons --group-directories-first'

# ==================== 5. 结束标志 ====================
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
export PATH="/Users/hxaxd/.local/bin:$PATH"
export PATH="/opt/homebrew/opt/ccache/libexec:$PATH"

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/opt/homebrew/Caskroom/miniforge/base/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/opt/homebrew/Caskroom/miniforge/base/etc/profile.d/conda.sh" ]; then
        . "/opt/homebrew/Caskroom/miniforge/base/etc/profile.d/conda.sh"
    else
        export PATH="/opt/homebrew/Caskroom/miniforge/base/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

eval "$(fnm env --use-on-cd)"

# ==================== 修复 sudo 插件 Esc Esc 冲突 ====================

# 1. 显式重新绑定 sudo-command-line 到双击 Esc
# Oh My Zsh 的 sudo 插件定义了这个 widget 名为 sudo-command-line
bindkey -M emacs '\e\e' sudo-command-line
bindkey -M vicmd '\e\e' sudo-command-line
bindkey -M viins '\e\e' sudo-command-line

# 2. 缩短按键延迟 (关键!)
# Zsh 默认等待 0.4 秒来判断 Esc 后面是否还有后续按键。
# 调低到 10-15ms 可以让双击 Esc 响应极快，且不影响 fzf 的 Alt+C 等功能。
export KEYTIMEOUT=15
