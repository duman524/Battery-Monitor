"""
主程序入口 - PyQt5 版本
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from utils.helpers import check_system_compatibility, check_dependencies, show_error_message
from ui.overlay_window import BatteryOverlay


def main():
    """主函数"""
    
    # 检查系统兼容性
    if not check_system_compatibility():
        show_error_message("此程序仅支持Windows系统")
        return
    
    # 检查依赖
    if not check_dependencies():
        show_error_message("缺少必要的依赖库，请安装 psutil: pip install psutil")
        return
    
    try:
        # 创建应用
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        
        # 创建悬浮窗口
        overlay = BatteryOverlay()
        overlay.show()
        
        # 启动应用
        sys.exit(app.exec_())
        
    except Exception as e:
        show_error_message(f"程序运行出错: {e}")


if __name__ == "__main__":
    main()