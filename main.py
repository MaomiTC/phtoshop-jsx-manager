import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow
from ps_controller import PhotoshopController

def resource_path(relative_path):
    """获取资源的绝对路径"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序图标
    app.setWindowIcon(QIcon(resource_path('ps-jsx.ico')))
    
    try:
        ps_controller = PhotoshopController()
        window = MainWindow(ps_controller)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "错误", f"启动失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 