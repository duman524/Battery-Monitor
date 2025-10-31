"""
主程序入口 - 系统托盘版本
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import QTimer, Qt
from ui.qt_overlay import BatteryOverlay
from ui.settings_window import SettingsWindow
from config_manager import ConfigManager
from utils.helpers import check_system_compatibility, check_dependencies, show_error_message


class BatteryApp:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.overlay = BatteryOverlay(self.config_manager)
        self.settings_window = None
        
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon()
        self.create_tray_icon()
        
        # 防止频繁切换的计时器
        self.last_toggle_time = 0
        self.toggle_cooldown = 300  # 300毫秒冷却时间
        
        # 启动时根据配置决定是否显示悬浮窗
        if self.config_manager.get_show_overlay():
            self.overlay.show()
        else:
            self.overlay.hide()

    def create_tray_icon(self):
        # 创建电池图标
        icon = self.create_battery_icon()
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("电池监控")
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        # 显示/隐藏悬浮窗
        show_overlay_action = QAction("显示/隐藏悬浮窗", self.tray_icon)
        show_overlay_action.triggered.connect(self.toggle_overlay)
        tray_menu.addAction(show_overlay_action)
        
        # 设置
        settings_action = QAction("设置", self.tray_icon)
        settings_action.triggered.connect(self.show_settings)
        tray_menu.addAction(settings_action)
        
        tray_menu.addSeparator()
        
        # 退出
        quit_action = QAction("退出", self.tray_icon)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # 托盘图标点击事件
        self.tray_icon.activated.connect(self.on_tray_activated)
    
    def create_battery_icon(self):
        """创建电池图标"""
        # 创建一个16x16的图标
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制电池外框
        painter.setPen(QColor(200, 200, 200))
        painter.setBrush(QColor(240, 240, 240))
        painter.drawRoundedRect(1, 4, 12, 8, 2, 2)
        
        # 绘制电池正极
        painter.setBrush(QColor(200, 200, 200))
        painter.drawRect(13, 6, 2, 4)
        
        # 获取电池电量
        try:
            import psutil
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                
                # 根据电量设置颜色
                if percent > 70:
                    color = QColor(0, 200, 0)  # 绿色
                elif percent > 30:
                    color = QColor(255, 200, 0)  # 黄色
                elif percent > 15:
                    color = QColor(255, 140, 0)  # 橙色
                else:
                    color = QColor(255, 0, 0)  # 红色
                
                # 绘制电量
                width = max(1, int(10 * percent / 100))
                painter.setBrush(color)
                painter.setPen(Qt.NoPen)
                painter.drawRoundedRect(2, 5, width, 6, 1, 1)
        except:
            pass
        
        painter.end()
        
        return QIcon(pixmap)
    
    def on_tray_activated(self, reason):
        """托盘图标激活事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_overlay()
    
    def toggle_overlay(self):
        """切换悬浮窗显示状态 - 添加防抖处理"""
        import time
        current_time = int(time.time() * 1000)
        
        # 防止频繁切换
        if current_time - self.last_toggle_time < self.toggle_cooldown:
            return
            
        self.last_toggle_time = current_time
        
        try:
            if self.overlay.isVisible():
                self.overlay.hide()
            else:
                self.overlay.show()
        except Exception as e:
            print(f"切换悬浮窗时出错: {e}")
    
    def show_settings(self):
        """显示设置窗口"""
        if self.settings_window is None:
            self.settings_window = SettingsWindow(self.config_manager)
        self.settings_window.show()
    
    def quit_app(self):
        """退出应用程序"""
        self.overlay.monitoring = False
        QApplication.quit()


def main():
    # 检查系统兼容性
    if not check_system_compatibility():
        show_error_message("此程序仅支持Windows系统")
        return
    
    # 检查依赖
    if not check_dependencies():
        show_error_message("缺少必要的依赖库，请安装 psutil: pip install psutil")
        return
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # 设置应用程序属性，避免在任务栏显示
    app.setAttribute(Qt.AA_DontShowIconsInMenus, False)
    
    battery_app = BatteryApp()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()