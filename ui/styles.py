"""
界面样式管理模块
"""

import tkinter as tk
from tkinter import ttk
from config.settings import settings


class StyleManager:
    """样式管理器"""
    
    def __init__(self):
        self.style = ttk.Style()
        self._setup_styles()
    
    def _setup_styles(self):
        """设置样式"""
        # 使用更简单的样式配置，确保透明背景
        self.style.configure(
            "Battery.TLabel",
            background=settings.colors['background'],
            foreground=settings.colors['text_normal'],
            font=settings.fonts['percentage']
        )
        
        self.style.configure(
            "Status.TLabel",
            background=settings.colors['background'],
            foreground=settings.colors['text_secondary'],
            font=settings.fonts['status']
        )
        
        self.style.configure(
            "Time.TLabel",
            background=settings.colors['background'],
            foreground=settings.colors['text_time'],
            font=settings.fonts['time']
        )
        
        self.style.configure(
            "TFrame",
            background=settings.colors['background']
        )
    
    def get_color(self, color_name: str) -> str:
        """获取颜色"""
        return settings.colors.get(color_name, 'white')
    
    def get_font(self, font_name: str) -> tuple:
        """获取字体"""
        return settings.fonts.get(font_name, ('Arial', 10))


# 全局样式管理器实例
style_manager = StyleManager()