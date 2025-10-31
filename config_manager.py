"""
配置管理器
"""

import json
import os
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QFont


class ConfigManager(QObject):
    config_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.config_file = "config.json"
        self.default_config = {
            "font_family": "Arial",
            "font_size": 24,
            "font_bold": True,
            "font_italic": False,
            "show_overlay": True,
            "window_position": [100, 50]
        }
        self.config = self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            return self.default_config.copy()
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
        self.config_changed.emit()
    
    def get_font(self):
        font = QFont()
        font.setFamily(self.config["font_family"])
        font.setPointSize(self.config["font_size"])
        font.setBold(self.config["font_bold"])
        font.setItalic(self.config["font_italic"])
        return font
    
    def set_font(self, font_family, font_size, bold, italic):
        self.config["font_family"] = font_family
        self.config["font_size"] = font_size
        self.config["font_bold"] = bold
        self.config["font_italic"] = italic
        self.save_config()
    
    def set_show_overlay(self, show):
        self.config["show_overlay"] = show
        self.save_config()
    
    def get_show_overlay(self):
        return self.config["show_overlay"]
    
    def set_window_position(self, pos):
        self.config["window_position"] = [pos.x(), pos.y()]
        self.save_config()
    
    def get_window_position(self):
        return self.config["window_position"]