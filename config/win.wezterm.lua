local wezterm = require 'wezterm'
local act = wezterm.action

-- 创建配置对象
local config = wezterm.config_builder()

-- ==================== 1. 极致视觉（清纯、高级感） ====================

config.color_scheme = "Tokyo Night"

-- 窗口背景
config.window_background_opacity = 0.85
config.macos_window_background_blur = 30
config.background = {
  {
    source = {
      File = '', -- 在这里填写你的背景图片路径
    },
    hsb = {
      hue = 1.0,
      saturation = 1.0,
      brightness = 1.0,
    },
  },
}

-- RESIZE: 允许调整大小
config.window_decorations = "INTEGRATED_BUTTONS|RESIZE"

-- 【关键建议】标签栏样式
-- 如果追求“高级感”，建议开启 Fancy Tab Bar，因为非 Fancy 模式看起来像 DOS 界面
config.use_fancy_tab_bar = true 
config.tab_bar_at_bottom = false
config.hide_tab_bar_if_only_one_tab = false

-- 字体配置
config.font = wezterm.font_with_fallback({
  { 
    family = "Monaspace Radon NF", 
    weight = "Regular",
    harfbuzz_features = { "calt", "liga", "dlig", "ss01", "ss02", "ss03", "ss04", "ss05", "ss06", "ss07", "ss08" },
  },
})
config.font_size = 14.5
config.line_height = 1.2

-- ==================== 2. 实用功能配置 ====================

config.default_prog = { 'wsl' }
config.window_close_confirmation = 'NeverPrompt'
config.scrollback_lines = 5000
config.send_composed_key_when_left_alt_is_pressed = false

-- WSL 配置
config.wsl_domains = {
  {
    name = 'wsl:ubuntu',
    distribution = 'Ubuntu',
  },
}

-- 菜单启动项
config.launch_menu = {
    {
      label = 'PowerShell',
      args = { 'pwsh.exe' },
    },
    {
      label = 'CTRL',
      args = { 'cmd.exe' },
    },
    {
      label = 'PowerShell (SUDO)',
      args = { 'sudo', 'pwsh.exe' },
    },
    {
      label = 'CTRL (SUDO)',
      args = { 'sudo', 'cmd.exe' },
    },
}

-- SSH 远程域配置
-- config.ssh_domains = {
--   {
--     name = "",
--     remote_address = "",
--     username = "root",
--   },

-- 鼠标绑定
config.mouse_bindings = {
  {
    event = { Up = { streak = 1, button = 'Left' } },
    mods = 'CTRL',
    action = act.OpenLinkAtMouseCursor,
  },
}

-- 非活动窗口标签透明度调整
config.inactive_pane_hsb = {
  saturation = 0.9, -- 饱和度稍微降低
  brightness = 0.6, -- 亮度降低，让当前窗口像聚光灯一样亮
}

-- ==================== 3. 强悍的快捷键 ====================

config.keys = {
  -- 搜索与启动
  { key = 'p', mods = 'CTRL', action = act.ShowLauncherArgs { flags = 'FUZZY|TABS|LAUNCH_MENU_ITEMS|WORKSPACES' } },
  { key = 'f', mods = 'CTRL', action = act.Search { CaseSensitiveString = "" } },

  -- 全屏切换
  { key = 'F11', mods = 'NONE', action = act.ToggleFullScreen },

  -- 分屏管理
  { key = 'd', mods = 'CTRL', action = act.SplitHorizontal { domain = 'CurrentPaneDomain' } },
  { key = 'D', mods = 'CTRL|SHIFT', action = act.SplitVertical { domain = 'CurrentPaneDomain' } },
  { key = 'LeftArrow', mods = 'CTRL', action = act.ActivatePaneDirection 'Left' },
  { key = 'RightArrow', mods = 'CTRL', action = act.ActivatePaneDirection 'Right' },
  { key = 'UpArrow', mods = 'CTRL', action = act.ActivatePaneDirection 'Up' },
  { key = 'DownArrow', mods = 'CTRL', action = act.ActivatePaneDirection 'Down' },
  { key = 'z', mods = 'CTRL', action = act.TogglePaneZoomState },

  -- 标签页管理
  { key = 't', mods = 'CTRL', action = act.SpawnTab 'DefaultDomain' },
  { key = 'w', mods = 'CTRL', action = act.CloseCurrentTab { confirm = false } },
  { key = '[', mods = 'CTRL', action = act.ActivateTabRelative(-1) },
  { key = ']', mods = 'CTRL', action = act.ActivateTabRelative(1) },

  -- 字体缩放
  { key = '=', mods = 'CTRL', action = act.IncreaseFontSize },
  { key = '-', mods = 'CTRL', action = act.DecreaseFontSize },

  -- 剪贴板
  { key = 'c', mods = 'CTRL|SHIFT', action = act.CopyTo 'Clipboard' },
  { key = 'v', mods = 'CTRL|SHIFT', action = act.PasteFrom 'Clipboard' },
}

-- ==================== 4. 渲染引擎优化 ====================
config.front_end = "WebGpu" 

return config