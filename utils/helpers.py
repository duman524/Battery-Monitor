"""
工具函数模块
"""

import platform
import sys


def check_system_compatibility():
    """
    检查系统兼容性
    
    Returns:
        bool: 如果系统兼容返回True，否则返回False
    """
    return platform.system() == "Windows"


def check_dependencies():
    """
    检查依赖是否安装
    
    Returns:
        bool: 如果所有依赖都可用返回True，否则返回False
    """
    try:
        import psutil
        return True
    except ImportError:
        return False


def show_error_message(message):
    """
    显示错误信息
    
    Args:
        message: 错误消息
    """
    print(f"错误: {message}")
    # 对于 PyQt5 版本，我们可以使用消息框
    try:
        from PyQt5.QtWidgets import QMessageBox, QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("错误")
        msg.exec_()
    except:
        # 如果 PyQt5 不可用，回退到控制台输出
        print(f"错误: {message}")