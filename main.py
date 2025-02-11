import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from ui.main_window import MainWindow
from ps_controller import PhotoshopController

def main():
    app = QApplication(sys.argv)
    
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