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
)

source $ZSH/oh-my-zsh.sh

# ==================== 3. 2025 墙裂推荐的现代插件初始化 ====================

# [zoxide] - 现代化的 cd，它能记住你常去的目录
eval "$(zoxide init zsh)"

# ==================== 4. 实用别名 (Alias) ====================
alias cls='clear'
alias ..='cd ..'
alias ...='cd ../..'
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
