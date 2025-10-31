"""
配置设置模块
"""

class Settings:
    """程序配置类"""
    
    def __init__(self):
        # 窗口设置 - 调整为更小的窗口，适应更大的字体
        self.window_width = 180
        self.window_height = 80
        self.window_position = "+100+50"  # x+y位置
        self.default_alpha = 0.8  # 默认透明度
        self.min_alpha = 0.3      # 最小透明度
        self.max_alpha = 1.0      # 最大透明度
        
        # 更新设置
        self.update_interval = 5  # 更新间隔(秒)
        
        # 颜色设置
        self.colors = {
            'background': 'black',
            'text_normal': 'white',
            'text_secondary': 'lightgray',
            'text_time': 'lightblue',
            'level_high': 'lightgreen',      # >70%
            'level_medium': 'yellow',        # 30-70%
            'level_low': 'orange',           # 15-30%
            'level_critical': 'red',         # <15%
        }
        
        # 字体设置 - 更新百分比字体大小
        self.fonts = {
            'percentage': ('Arial', 24, 'bold'),  # 增大字体
            'status': ('Arial', 10),
            'time': ('Arial', 9),
        }
        
        # 电池级别阈值
        self.battery_levels = {
            'high': 70,
            'medium': 30,
            'low': 15,
        }


# 全局配置实例
settings = Settings()