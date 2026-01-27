local wezterm = require 'wezterm'
local act = wezterm.action

-- 创建配置对象
local config = wezterm.config_builder()

-- ==================== 1. 极致视觉（清纯、高级感） ====================

config.color_scheme = "Tokyo Night"

-- 窗口背景
config.window_background_opacity = 0.85
config.macos_window_background_blur = 30

-- RESIZE: 允许调整大小
config.window_decorations = "RESIZE"

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
  { family = "PingFang SC", weight = "Regular" },
})
config.font_size = 14.5
config.line_height = 1.2

-- ==================== 2. 实用功能配置 ====================

config.default_prog = { '/bin/zsh', '--login' }
config.window_close_confirmation = 'NeverPrompt'
config.scrollback_lines = 5000
config.send_composed_key_when_left_alt_is_pressed = false

-- 鼠标绑定
config.mouse_bindings = {
  {
    event = { Up = { streak = 1, button = 'Left' } },
    mods = 'CMD',
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
  { key = 'p', mods = 'CMD', action = act.ShowLauncherArgs { flags = 'FUZZY|TABS|LAUNCH_MENU_ITEMS|WORKSPACES' } },
  { key = 'f', mods = 'CMD', action = act.Search { CaseSensitiveString = "" } },

  -- 分屏管理
  { key = 'd', mods = 'CMD', action = act.SplitHorizontal { domain = 'CurrentPaneDomain' } },
  { key = 'D', mods = 'CMD|SHIFT', action = act.SplitVertical { domain = 'CurrentPaneDomain' } },
  { key = 'LeftArrow', mods = 'CMD', action = act.ActivatePaneDirection 'Left' },
  { key = 'RightArrow', mods = 'CMD', action = act.ActivatePaneDirection 'Right' },
  { key = 'UpArrow', mods = 'CMD', action = act.ActivatePaneDirection 'Up' },
  { key = 'DownArrow', mods = 'CMD', action = act.ActivatePaneDirection 'Down' },
  { key = 'z', mods = 'CMD', action = act.TogglePaneZoomState },

  -- 标签页管理
  { key = 't', mods = 'CMD', action = act.SpawnTab 'DefaultDomain' },
  { key = 'w', mods = 'CMD', action = act.CloseCurrentTab { confirm = false } },
  { key = '[', mods = 'CMD', action = act.ActivateTabRelative(-1) },
  { key = ']', mods = 'CMD', action = act.ActivateTabRelative(1) },

  -- 字体缩放
  { key = '=', mods = 'CMD', action = act.IncreaseFontSize },
  { key = '-', mods = 'CMD', action = act.DecreaseFontSize },
  { key = '0', mods = 'CMD', action = act.ResetFontSize },

  -- 剪贴板
  { key = 'c', mods = 'CMD', action = act.CopyTo 'Clipboard' },
  { key = 'v', mods = 'CMD', action = act.PasteFrom 'Clipboard' },
}

-- ==================== 4. 渲染引擎优化 ====================
config.front_end = "WebGpu" 

return config