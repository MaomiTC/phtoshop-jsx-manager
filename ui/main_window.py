from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QListWidget, QLabel, QFileDialog, 
                           QMessageBox, QSplitter, QTextEdit, QGroupBox,
                           QListWidgetItem, QToolBar, QLineEdit, QMenu,
                           QComboBox, QToolButton, QSizePolicy, QStatusBar)
from PyQt6.QtCore import Qt, QDir, QSize, QUrl
from PyQt6.QtGui import QIcon, QFont, QAction, QKeySequence, QShortcut, QDesktopServices, QPixmap, QCursor
import os
import json
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self, ps_controller):
        super().__init__()
        self.ps_controller = ps_controller
        self.script_paths = {}
        self.folder_paths = set()  # 添加文件夹路径集合
        self.settings_file = Path('settings.json')
        self.load_settings()  # 只加载脚本列表
        self.init_ui()
        self.script_history = []
        self.current_folder = ""

    def load_settings(self):
        """加载设置和文件夹路径"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.script_paths = settings.get('scripts', {})
                    self.folder_paths = set(settings.get('folders', []))  # 加载文件夹路径
            except Exception as e:
                print(f"加载设置失败: {e}")

    def save_settings(self):
        """保存设置和文件夹路径"""
        try:
            settings = {
                'scripts': self.script_paths,
                'folders': list(self.folder_paths)  # 保存文件夹路径
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存设置失败: {e}")

    def init_ui(self):
        self.setWindowTitle('Photoshop JSX manager')
        self.setGeometry(100, 100, 1200, 800)
        
        # 纯深色主题样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QPushButton {
                color: #ffffff;
                border: 1px solid #333333;
                padding: 8px 16px;
                border-radius: 6px;
                background-color: #2d2d2d;
                font-weight: 500;
                min-height: 32px;
            }
            QPushButton:hover {
                background-color: #383838;
                border-color: #444444;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
            QListWidget {
                border: 1px solid #333333;
                border-radius: 8px;
                background-color: #242424;
                padding: 8px;
                outline: none;
            }
            QListWidget::item {
                padding: 12px;
                margin: 2px 4px;
                border-radius: 6px;
                color: #ffffff;
            }
            QListWidget::item:selected {
                background-color: #3a3a3a;
                color: #ffffff;
                font-weight: 500;
                outline: none;
            }
            QListWidget::item:hover {
                background-color: #2a2a2a;
            }
            QTextEdit {
                border: 1px solid #333333;
                border-radius: 8px;
                background-color: #242424;
                padding: 12px;
                font-family: "JetBrains Mono", "SF Mono", "Cascadia Code", monospace;
                font-size: 13px;
                line-height: 1.6;
                color: #ffffff;
            }
            QGroupBox {
                font-weight: 600;
                border: 1px solid #333333;
                border-radius: 10px;
                margin-top: 6px;
                padding: 16px;
                background-color: #242424;
                color: #ffffff;
            }
            QToolBar {
                border: none;
                background-color: #1a1a1a;
                border-bottom: 1px solid #333333;
                spacing: 8px;
                padding: 8px 16px;
            }
            QLineEdit {
                padding: 8px 16px;
                border: 1px solid #333333;
                border-radius: 20px;
                background-color: #242424;
                color: #ffffff;
                min-height: 36px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #4a4a4a;
                background-color: #2a2a2a;
            }
            QStatusBar {
                background-color: #1a1a1a;
                color: #888888;
                border-top: 1px solid #333333;
                padding: 4px;
            }
            QMenu {
                background-color: #242424;
                border: 1px solid #333333;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 24px;
                border-radius: 4px;
                color: #ffffff;
            }
            QMenu::item:selected {
                background-color: #3a3a3a;
            }
            QSplitter::handle {
                background-color: #333333;
                width: 1px;
            }
            QSplitter::handle:hover {
                background-color: #444444;
            }
        """)

        # 创建工具栏
        self.create_toolbar()

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # 创建左侧面板
        left_panel = self.create_left_panel()

        # 创建右侧面板
        right_panel = self.create_right_panel()

        # 添加分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        main_layout.addWidget(splitter)

        # 创建状态栏
        status_bar = self.statusBar()
        status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #1a1a1a;
                color: #888888;
                border-top: 1px solid #333333;
                padding: 4px;
            }
            QLabel {
                color: #888888;
            }
            QLabel[link=true] {
                color: #64B5F6;
            }
            QLabel[link=true]:hover {
                color: #90CAF9;
                text-decoration: underline;
            }
        """)

        # 创建状态栏小部件
        status_message = QLabel('就绪')
        author_label = QLabel('作者: ')
        author_link = QLabel('<a href="https://www.xiaohongshu.com/user/profile/59f1fcc411be101aba7f048f" style="color: #64B5F6; text-decoration: none;">猫咪老师Reimagined</a>')
        author_link.setOpenExternalLinks(True)
        
        status_bar.addWidget(status_message)
        status_bar.addPermanentWidget(author_label)
        status_bar.addPermanentWidget(author_link)

        # 保存状态消息标签的引用，以便后续更新
        self.status_message_label = status_message

        # 创建快捷键
        self.create_shortcuts()

        # 初始化时加载保存的脚本
        for file_name, file_path in self.script_paths.items():
            item = QListWidgetItem(file_name)
            self.script_list.addItem(item)

    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # 优化搜索框设计
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("猫咪老师 搜索脚本...")
        self.search_box.setMinimumWidth(280)
        self.search_box.textChanged.connect(self.filter_scripts)
        self.search_box.setStyleSheet("""
            QLineEdit {
                background-color: #242424;
                border: 1px solid #333333;
                border-radius: 18px;
                padding: 8px 16px 8px 36px;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #4a4a4a;
                background-color: #2a2a2a;
            }
            QLineEdit::placeholder {
                color: #666666;
            }
        """)
        
        search_layout.addWidget(self.search_box)
        toolbar.addWidget(search_widget)

        # 添加弹性空间
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        toolbar.addWidget(spacer)

        # 添加猫咪图标
        logo_label = QLabel()
        logo_pixmap = QPixmap("mao.png")
        
        # 直接使用原始图片大小或设置一个固定大小
        icon_size = 48  # 或者使用您想要的大小
        scaled_pixmap = logo_pixmap.scaled(icon_size, icon_size, 
                                         Qt.AspectRatioMode.KeepAspectRatio, 
                                         Qt.TransformationMode.SmoothTransformation)
        
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                margin-right: 12px;
            }
        """)
        logo_label.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # 添加点击事件
        def open_profile():
            QDesktopServices.openUrl(QUrl("https://www.xiaohongshu.com/user/profile/59f1fcc411be101aba7f048f"))
        
        logo_label.mousePressEvent = lambda _: open_profile()
        
        toolbar.addWidget(logo_label)

    def create_left_panel(self):
        left_panel = QGroupBox("脚本列表")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(15, 20, 15, 15)

        # 创建标题栏布局
        title_layout = QHBoxLayout()
        title_label = QLabel("脚本列表")
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        # 添加刷新按钮 - 新设计
        refresh_btn = QPushButton()
        refresh_btn.setFixedSize(24, 24)
        refresh_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                image: url(icons/refresh.png);  /* 如果使用图标 */
                color: #888888;
                font-size: 14px;
                padding: 0;
            }
            QPushButton:hover {
                color: #ffffff;
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)
        refresh_btn.setText("⟳")  # 使用 Unicode 字符作为刷新图标
        refresh_btn.clicked.connect(self.refresh_script_list)
        refresh_btn.setToolTip("刷新脚本列表")
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(refresh_btn)

        # 脚本列表
        self.script_list = QListWidget()
        self.script_list.setMinimumWidth(300)
        self.script_list.setSpacing(4)
        self.script_list.currentItemChanged.connect(self.on_script_selected)
        self.script_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.script_list.customContextMenuRequested.connect(self.show_context_menu)
        
        # 启用拖拽功能
        self.script_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.script_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.script_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.script_list.setDragEnabled(True)
        self.script_list.setAcceptDrops(True)
        self.script_list.dropEvent = self.handle_drop_event  # 自定义处理拖拽事件
        
        # 按钮工具栏
        button_toolbar = QHBoxLayout()
        button_toolbar.setSpacing(8)
        
        # 创建深色按钮
        buttons_data = [
            ('导入脚本', self.import_script),
            ('导入文件夹', self.import_folder),
            ('运行脚本', self.run_script),
            ('删除脚本', self.delete_script)
        ]
        
        for text, callback in buttons_data:
            btn = QPushButton(text)
            btn.setMinimumHeight(32)
            btn.clicked.connect(callback)
            button_toolbar.addWidget(btn)
        
        button_toolbar.addStretch()

        left_layout.addLayout(title_layout)  # 添加标题栏布局
        left_layout.addWidget(self.script_list)
        left_layout.addLayout(button_toolbar)

        return left_panel

    def create_right_panel(self):
        right_panel = QGroupBox("脚本编辑器")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(15, 20, 15, 15)

        # 编辑器工具栏
        editor_toolbar = QHBoxLayout()
        editor_toolbar.setSpacing(8)
        
        # 编辑器按钮 - 深色风格
        buttons_data = [
            ('保存', self.save_script),
            ('撤销', lambda: self.preview_text.undo()),
            ('重做', lambda: self.preview_text.redo())
        ]
        
        for text, callback in buttons_data:
            btn = QPushButton(text)
            btn.setMinimumHeight(32)
            btn.clicked.connect(callback)
            editor_toolbar.addWidget(btn)
        
        editor_toolbar.addStretch()

        # 创建编辑器
        self.preview_text = QTextEdit()
        self.preview_text.setFont(QFont("JetBrains Mono", 13))
        
        right_layout.addLayout(editor_toolbar)
        right_layout.addWidget(self.preview_text)

        return right_panel

    def create_shortcuts(self):
        # 创建快捷键
        try:
            save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
            save_shortcut.activated.connect(self.save_script)

            open_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
            open_shortcut.activated.connect(self.import_script)

            run_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
            run_shortcut.activated.connect(self.run_script)

            delete_shortcut = QShortcut(QKeySequence("Delete"), self)
            delete_shortcut.activated.connect(self.delete_script)
        except Exception as e:
            print(f"创建快捷键时出错: {str(e)}")

    def show_context_menu(self, position):
        menu = QMenu()
        run_action = menu.addAction("运行脚本")
        edit_action = menu.addAction("编辑脚本")
        delete_action = menu.addAction("删除脚本")
        
        action = menu.exec(self.script_list.mapToGlobal(position))
        if action == run_action:
            self.run_script()
        elif action == edit_action:
            self.edit_script()
        elif action == delete_action:
            self.delete_script()

    def filter_scripts(self, text):
        for i in range(self.script_list.count()):
            item = self.script_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def import_script(self):
        file_names, _ = QFileDialog.getOpenFileNames(
            self,
            "选择JSX脚本",
            "",
            "JSX Files (*.jsx);;All Files (*)"
        )
        for file_path in file_names:
            if file_path:
                self._add_script_to_list(file_path)

    def import_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择脚本文件夹",
            "",
            QFileDialog.Option.ShowDirsOnly
        )
        if folder_path:
            # 记录文件夹路径并扫描
            self.folder_paths.add(folder_path)
            self._scan_folder(folder_path)
            self.save_settings()

    def _scan_folder(self, folder_path):
        """扫描文件夹中的脚本"""
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.jsx'):
                        file_path = os.path.join(root, file)
                        self._add_script_to_list(file_path)
        except Exception as e:
            self.show_message("错误", f"扫描文件夹失败: {folder_path}\n{str(e)}", QMessageBox.Icon.Critical)

    def _add_script_to_list(self, file_path):
        """添加脚本到列表并保存设置"""
        file_name = os.path.basename(file_path)
        existing_items = self.script_list.findItems(file_name, Qt.MatchFlag.MatchExactly)
        if not existing_items:
            item = QListWidgetItem(file_name)
            self.script_list.addItem(item)
            self.script_paths[file_name] = file_path
            self.save_settings()  # 保存更新后的脚本列表
            self.status_message_label.setText(f'已导入: {file_name}')
        else:
            self.status_message_label.setText(f'脚本 {file_name} 已存在')

    def save_script(self):
        current_item = self.script_list.currentItem()
        if not current_item:
            self.show_message("警告", "请先选择一个脚本", QMessageBox.Icon.Warning)
            return

        file_name = current_item.text()
        file_path = self.script_paths.get(file_name)
        
        if not file_path:
            self.show_message("错误", "找不到脚本文件路径", QMessageBox.Icon.Critical)
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.preview_text.toPlainText())
            self.status_message_label.setText(f'已保存: {file_name}')
            self.show_message("成功", "脚本保存成功")
        except Exception as e:
            self.status_message_label.setText('保存失败')
            self.show_message("错误", f"保存脚本失败: {str(e)}", QMessageBox.Icon.Critical)

    def run_script(self):
        current_item = self.script_list.currentItem()
        if not current_item:
            self.show_message("警告", "请先选择一个脚本", QMessageBox.Icon.Warning)
            return

        file_name = current_item.text()
        file_path = self.script_paths.get(file_name)
        
        try:
            self.ps_controller.run_jsx_script(file_path)
            self.status_message_label.setText(f'成功执行脚本: {file_name}')
            self.show_message("成功", "脚本执行成功")
        except Exception as e:
            self.status_message_label.setText('执行失败')
            self.show_message("错误", f"脚本执行失败: {str(e)}", QMessageBox.Icon.Critical)

    def delete_script(self):
        current_item = self.script_list.currentItem()
        if not current_item:
            self.show_message("警告", "请先选择一个脚本", QMessageBox.Icon.Warning)
            return
        
        file_name = current_item.text()
        reply = self.show_question('确认删除', f'确定要从列表中删除脚本 "{file_name}" 吗？')
        
        if reply == QMessageBox.StandardButton.Yes:
            self.script_list.takeItem(self.script_list.row(current_item))
            self.script_paths.pop(file_name, None)
            self.preview_text.clear()
            self.status_message_label.setText(f'已删除: {file_name}')

    def on_script_selected(self, current, previous):
        if current:
            file_name = current.text()
            file_path = self.script_paths.get(file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.preview_text.setText(content)
            except Exception as e:
                self.preview_text.setText(f"无法读取文件内容: {str(e)}")

    def edit_script(self):
        # 添加编辑脚本的方法
        current_item = self.script_list.currentItem()
        if current_item:
            self.preview_text.setFocus()

    def closeEvent(self, event):
        """程序关闭时保存设置"""
        self.save_settings()
        super().closeEvent(event)

    def statusBar(self) -> QStatusBar:
        status_bar = super().statusBar()
        if not hasattr(self, '_status_message_label'):
            self._status_message_label = QLabel('就绪')
            status_bar.addWidget(self._status_message_label)
        return status_bar

    def setStatusMessage(self, message):
        """更新状态栏消息"""
        if hasattr(self, '_status_message_label'):
            self._status_message_label.setText(message)

    def handle_drop_event(self, event):
        # 调用原始的dropEvent以执行实际的项目移动
        QListWidget.dropEvent(self.script_list, event)
        
        # 更新脚本路径字典以保持顺序
        new_script_paths = {}
        for i in range(self.script_list.count()):
            item = self.script_list.item(i)
            file_name = item.text()
            if file_name in self.script_paths:
                new_script_paths[file_name] = self.script_paths[file_name]
        
        # 更新脚本路径字典
        self.script_paths = new_script_paths
        # 保存新的顺序
        self.save_settings() 

    def show_message(self, title, message, icon_type=QMessageBox.Icon.Information):
        """显示统一风格的深色消息框"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon_type)
        
        # 设置深色主题样式
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
                font-size: 13px;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
                min-height: 24px;
            }
            QPushButton:hover {
                background-color: #383838;
                border-color: #444444;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
        """)
        
        return msg_box.exec()

    def show_question(self, title, message):
        """显示统一风格的深色确认框"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        # 设置深色主题样式
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
                font-size: 13px;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
                min-height: 24px;
            }
            QPushButton:hover {
                background-color: #383838;
                border-color: #444444;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
        """)
        
        return msg_box.exec()

    def refresh_script_list(self):
        """刷新脚本列表，重新扫描所有已导入的文件夹"""
        try:
            # 保存当前选中的项目
            current_item = self.script_list.currentItem()
            current_file = current_item.text() if current_item else None
            
            # 清空列表
            self.script_list.clear()
            self.script_paths.clear()
            
            # 创建要移除的文件夹列表
            folders_to_remove = set()
            
            # 重新扫描所有已导入的文件夹
            for folder_path in self.folder_paths:
                if os.path.exists(folder_path):
                    self._scan_folder(folder_path)
                else:
                    folders_to_remove.add(folder_path)
            
            # 移除不存在的文件夹
            self.folder_paths -= folders_to_remove
            
            # 恢复之前选中的项目
            if current_file:
                items = self.script_list.findItems(current_file, Qt.MatchFlag.MatchExactly)
                if items:
                    self.script_list.setCurrentItem(items[0])
            
            self.save_settings()
            self.status_message_label.setText('脚本列表已刷新')
            self.show_message("成功", "脚本列表已刷新")
        except Exception as e:
            self.status_message_label.setText('刷新失败')
            self.show_message("错误", f"刷新脚本列表失败: {str(e)}", QMessageBox.Icon.Critical) 