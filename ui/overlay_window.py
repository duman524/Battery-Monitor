"""
PyQt5 悬浮窗口模块
"""

import sys
import threading
import time
from PyQt5.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, 
                             QMenu, QAction, QApplication)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QMouseEvent, QLinearGradient, QPalette, QColor, QCursor
from config.settings import settings
from core.battery_reader import battery_reader
from core.data_processor import data_processor


class BatteryOverlay(QMainWindow):
    """电池监控悬浮窗口 - PyQt5 版本"""
    
    update_signal = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.create_widgets()
        
        # 连接信号
        self.update_signal.connect(self.update_display)
        
        # 监控状态
        self.monitoring = True
        self.start_monitoring()
        
        # 自动更新定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.manual_refresh)
        self.timer.start(settings.update_interval * 1000)
    
    def setup_window(self):
        """设置窗口属性"""
        self.setWindowTitle("电池电量显示器")
        # 调整窗口大小以适应更大的字体
        self.setGeometry(100, 50, 180, 80)
        
        # 设置窗口属性 - 完全透明
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )
        
        # 设置完全透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        
        # 设置初始透明度
        self.setWindowOpacity(settings.default_alpha)
        
        # 启用鼠标跟踪
        self.setMouseTracking(True)
    
    def create_widgets(self):
        """创建界面组件"""
        # 中央部件 - 完全透明
        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        central_widget.setMouseTracking(True)  # 启用鼠标跟踪
        self.setCentralWidget(central_widget)
        
        # 布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # 移除边距
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignCenter)
        
        # 电量百分比显示 - 使用更大的字体
        self.percentage_label = QLabel("---%")
        self.percentage_label.setAlignment(Qt.AlignCenter)
        self.percentage_label.setStyleSheet("background: transparent;")
        # 使用更大的字体
        self.percentage_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.percentage_label.setMouseTracking(True)  # 启用鼠标跟踪
        layout.addWidget(self.percentage_label)
        
        # 设置鼠标悬停效果
        self.percentage_label.enterEvent = self.on_text_hover_enter
        self.percentage_label.leaveEvent = self.on_text_hover_leave
    
    def on_text_hover_enter(self, event):
        """鼠标悬停在文字上时"""
        self.setCursor(Qt.SizeAllCursor)  # 设置为可移动光标
    
    def on_text_hover_leave(self, event):
        """鼠标离开文字时"""
        self.setCursor(Qt.ArrowCursor)  # 恢复默认光标
    
    def start_monitoring(self):
        """开始监控电池状态"""
        def monitor_loop():
            while self.monitoring:
                try:
                    battery_data = battery_reader.get_battery_info()
                    if battery_data:
                        processed_data = data_processor.process_battery_data(battery_data)
                        self.update_signal.emit(processed_data)
                    
                    time.sleep(settings.update_interval)
                    
                except Exception as e:
                    print(f"监控电池状态时出错: {e}")
                    time.sleep(10)
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def update_display(self, data: dict):
        """更新显示"""
        # 根据充电状态设置电量文字样式
        if data['plugged']:
            # 充电状态：渐变色（上纯下白）
            self.apply_gradient_text(data['color'])
        else:
            # 不充电状态：纯色
            self.percentage_label.setStyleSheet(
                f"color: {data['color']}; "
                "background: transparent;"
            )
        
        # 更新百分比文本
        self.percentage_label.setText(f"{data['percent']}%")
    
    def apply_gradient_text(self, base_color):
        """应用渐变色文本效果"""
        # 创建渐变色
        gradient = QLinearGradient(0, 0, 0, self.percentage_label.height())
        
        # 将十六进制颜色转换为QColor
        if base_color.startswith('#'):
            base_qcolor = QColor(base_color)
        else:
            # 处理颜色名称
            color_map = {
                'lightgreen': QColor(144, 238, 144),
                'yellow': QColor(255, 255, 0),
                'orange': QColor(255, 165, 0),
                'red': QColor(255, 0, 0),
                'white': QColor(255, 255, 255)
            }
            base_qcolor = color_map.get(base_color, QColor(255, 255, 255))
        
        # 设置渐变色：顶部为纯色，底部为白色
        gradient.setColorAt(0, base_qcolor)  # 顶部
        gradient.setColorAt(1, QColor(255, 255, 255))  # 底部
        
        # 创建调色板并设置文本刷
        palette = self.percentage_label.palette()
        palette.setBrush(QPalette.WindowText, gradient)
        self.percentage_label.setPalette(palette)
    
    def manual_refresh(self):
        """手动刷新"""
        try:
            battery_data = battery_reader.get_battery_info()
            if battery_data:
                processed_data = data_processor.process_battery_data(battery_data)
                self.update_display(processed_data)
        except Exception as e:
            print(f"手动刷新时出错: {e}")
    
    def set_transparency(self, alpha: float):
        """设置透明度"""
        self.setWindowOpacity(alpha)
    
    def quit_app(self):
        """退出应用程序"""
        self.monitoring = False
        QApplication.quit()
    
    # 鼠标事件处理
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        elif event.button() == Qt.RightButton:
            self.show_context_menu(event.globalPos())
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件"""
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def wheelEvent(self, event):
        """鼠标滚轮事件 - 调整透明度"""
        delta = event.angleDelta().y()
        current_alpha = self.windowOpacity()
        
        if delta > 0:  # 向上滚动
            new_alpha = min(1.0, current_alpha + 0.1)
        else:  # 向下滚动
            new_alpha = max(0.1, current_alpha - 0.1)
        
        self.setWindowOpacity(new_alpha)
    
    def show_context_menu(self, pos):
        """显示右键菜单"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: rgba(0, 0, 0, 200);
                color: white;
                border: 1px solid #555;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: rgba(255, 255, 255, 50);
            }
        """)
        
        refresh_action = QAction("刷新", self)
        refresh_action.triggered.connect(self.manual_refresh)
        menu.addAction(refresh_action)
        
        transparency_menu = menu.addMenu("透明度")
        
        transparency_high = QAction("高 (90%)", self)
        transparency_high.triggered.connect(lambda: self.set_transparency(0.9))
        transparency_menu.addAction(transparency_high)
        
        transparency_medium = QAction("中 (70%)", self)
        transparency_medium.triggered.connect(lambda: self.set_transparency(0.7))
        transparency_menu.addAction(transparency_medium)
        
        transparency_low = QAction("低 (40%)", self)
        transparency_low.triggered.connect(lambda: self.set_transparency(0.4))
        transparency_menu.addAction(transparency_low)
        
        menu.addSeparator()
        
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)
        
        menu.exec_(pos)