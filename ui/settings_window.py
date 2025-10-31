"""
设置窗口模块
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QCheckBox, QSpinBox, QPushButton, 
                             QApplication, QFontComboBox, QGroupBox)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor
from config_manager import ConfigManager


class SettingsWindow(QWidget):
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        self.init_ui()
        self.setup_theme()
        
    def init_ui(self):
        self.setWindowTitle("电池悬浮窗设置")
        self.setFixedSize(450, 400)
        
        layout = QVBoxLayout()
        
        # 字体设置组
        font_group = QGroupBox("字体设置")
        font_layout = QVBoxLayout()
        
        # 字体选择
        font_family_layout = QHBoxLayout()
        font_family_layout.addWidget(QLabel("字体:"))
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont(self.config_manager.config["font_family"]))
        font_family_layout.addWidget(self.font_combo)
        font_layout.addLayout(font_family_layout)
        
        # 字体大小
        font_size_layout = QHBoxLayout()
        font_size_layout.addWidget(QLabel("字体大小:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(10, 72)
        self.font_size_spin.setValue(self.config_manager.config["font_size"])
        font_size_layout.addWidget(self.font_size_spin)
        font_layout.addLayout(font_size_layout)
        
        # 粗体和斜体
        style_layout = QHBoxLayout()
        self.bold_check = QCheckBox("粗体")
        self.bold_check.setChecked(self.config_manager.config["font_bold"])
        style_layout.addWidget(self.bold_check)
        
        self.italic_check = QCheckBox("斜体")
        self.italic_check.setChecked(self.config_manager.config["font_italic"])
        style_layout.addWidget(self.italic_check)
        style_layout.addStretch()
        font_layout.addLayout(style_layout)
        
        # 预览
        self.preview_label = QLabel("预览: 88%")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.update_preview()
        font_layout.addWidget(self.preview_label)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        # 显示设置组
        display_group = QGroupBox("显示设置")
        display_layout = QVBoxLayout()
        self.show_overlay_check = QCheckBox("显示电量悬浮窗")
        self.show_overlay_check.setChecked(self.config_manager.config["show_overlay"])
        display_layout.addWidget(self.show_overlay_check)
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.apply_btn = QPushButton("应用")
        self.apply_btn.clicked.connect(self.apply_settings)
        button_layout.addWidget(self.apply_btn)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_btn)
        
        self.reset_btn = QPushButton("重置")
        self.reset_btn.clicked.connect(self.reset_settings)
        button_layout.addWidget(self.reset_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 连接信号
        self.font_combo.currentFontChanged.connect(self.update_preview)
        self.font_size_spin.valueChanged.connect(self.update_preview)
        self.bold_check.stateChanged.connect(self.update_preview)
        self.italic_check.stateChanged.connect(self.update_preview)
    
    def setup_theme(self):
        """根据系统设置主题"""
        settings = QSettings()
        # 检查系统是否使用深色模式
        try:
            system_theme = settings.value("HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize\\AppsUseLightTheme", 1, type=int)
            
            if system_theme == 0:  # 深色模式
                self.set_dark_theme()
            else:  # 浅色模式
                self.set_light_theme()
        except:
            # 如果无法获取系统主题，使用浅色主题作为默认
            self.set_light_theme()
    
    def set_dark_theme(self):
        """设置深色主题"""
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QGroupBox {
                border: 1px solid #555;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
            QPushButton {
                background-color: #555;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 3px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QPushButton:pressed {
                background-color: #444;
            }
            QComboBox, QSpinBox, QFontComboBox {
                background-color: #555;
                color: white;
                border: 1px solid #777;
                padding: 5px;
                border-radius: 3px;
            }
            QCheckBox {
                spacing: 5px;
                color: #ffffff;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #555;
                border: 1px solid #777;
                border-radius: 2px;
            }
            QCheckBox::indicator:checked {
                background-color: #0078d7;
                border: 1px solid #0078d7;
                border-radius: 2px;
            }
            QLabel {
                color: #ffffff;
            }
        """)
    
    def set_light_theme(self):
        """设置浅色主题"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                color: #000000;
            }
            QGroupBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #000000;
            }
            QPushButton {
                background-color: #e0e0e0;
                color: black;
                border: 1px solid #aaa;
                padding: 8px 15px;
                border-radius: 3px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
            QComboBox, QSpinBox, QFontComboBox {
                background-color: white;
                color: black;
                border: 1px solid #aaa;
                padding: 5px;
                border-radius: 3px;
            }
            QCheckBox {
                spacing: 5px;
                color: #000000;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
            QCheckBox::indicator:unchecked {
                background-color: white;
                border: 1px solid #aaa;
                border-radius: 2px;
            }
            QCheckBox::indicator:checked {
                background-color: #0078d7;
                border: 1px solid #0078d7;
                border-radius: 2px;
            }
            QLabel {
                color: #000000;
            }
        """)
    
    def update_preview(self):
        """更新预览"""
        font = QFont()
        font.setFamily(self.font_combo.currentFont().family())
        font.setPointSize(self.font_size_spin.value())
        font.setBold(self.bold_check.isChecked())
        font.setItalic(self.italic_check.isChecked())
        
        self.preview_label.setFont(font)
    
    def apply_settings(self):
        """应用设置"""
        # 保存字体设置
        font_family = self.font_combo.currentFont().family()
        font_size = self.font_size_spin.value()
        bold = self.bold_check.isChecked()
        italic = self.italic_check.isChecked()
        self.config_manager.set_font(font_family, font_size, bold, italic)
        
        # 保存显示设置
        show_overlay = self.show_overlay_check.isChecked()
        self.config_manager.set_show_overlay(show_overlay)
        
        self.close()
    
    def reset_settings(self):
        """重置设置"""
        self.font_combo.setCurrentFont(QFont(self.config_manager.default_config["font_family"]))
        self.font_size_spin.setValue(self.config_manager.default_config["font_size"])
        self.bold_check.setChecked(self.config_manager.default_config["font_bold"])
        self.italic_check.setChecked(self.config_manager.default_config["font_italic"])
        self.show_overlay_check.setChecked(self.config_manager.default_config["show_overlay"])
        self.update_preview()