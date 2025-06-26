import sys
import os
import shutil
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QFrame, QSizePolicy, QSpacerItem, QFileDialog, QDialog, QTabWidget, QComboBox, QLineEdit, QListWidget, QListWidgetItem, QMessageBox,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QSlider, QGridLayout, QListView, QStyle, QStyledItemDelegate, QStyleOptionViewItem, QStyleOptionButton
)
from PyQt6.QtGui import QFont, QPixmap, QIcon, QBrush, QColor
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QDateTime

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, ev):
        self.clicked.emit()
        super().mousePressEvent(ev)

class SortlifyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.theme_mode = "dark"
        self.accent_color = "blue"
        self.custom_rules = []  # Each rule: (contains_text, target_category)
        # User-editable category-extension mapping
        self.builtin_categories = [
            "Documents", "Images", "Videos", "Audio", "Archives", "Code", "Other"
        ]
        self.category_map = {
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".rtf"],
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".heic"],
            "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm", ".mpeg"],
            "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
            "Code": [".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs", ".html", ".css", ".json", ".xml", ".sh", ".bat", ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".m", ".pl", ".lua", ".sql"],
            "Other": []
        }
        self.setWindowTitle("Sortlify")
        self.setMinimumSize(900, 700)
        self.setStyleSheet(self.get_stylesheet())
        self.init_ui()

    def init_ui(self):
        # Central widget and main layout
        central = QWidget()
        central.setObjectName("CentralWidget")
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar with filters
        sidebar = QWidget()
        sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(24, 24, 24, 24)
        sidebar_layout.setSpacing(16)
        logo = QLabel("\u25A0  Sortlify")
        logo.setObjectName("Logo")
        sidebar_layout.addWidget(logo)
        sidebar_layout.addSpacing(16)
        sidebar_layout.addWidget(QLabel("<b>Filters</b>"))
        # File type filter
        sidebar_layout.addWidget(QLabel("Type:"))
        self.type_filter = QComboBox()
        self.type_filter.addItem("All")
        for cat in self.category_map:
            self.type_filter.addItem(cat)
        self.type_filter.currentTextChanged.connect(self.apply_filters)
        sidebar_layout.addWidget(self.type_filter)
        # Size filter
        sidebar_layout.addWidget(QLabel("Size (MB):"))
        self.size_filter = QComboBox()
        self.size_filter.addItems(["All", "<10", "10-100", ">100"])
        self.size_filter.currentTextChanged.connect(self.apply_filters)
        sidebar_layout.addWidget(self.size_filter)
        # Date modified filter
        sidebar_layout.addWidget(QLabel("Modified:"))
        self.date_filter = QComboBox()
        self.date_filter.addItems(["All", "Today", "Last 7 Days", "Last Month", "Older"])
        self.date_filter.currentTextChanged.connect(self.apply_filters)
        sidebar_layout.addWidget(self.date_filter)
        sidebar_layout.addStretch()
        sidebar.setFixedWidth(180)

        # Main content area
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Top bar
        topbar = QWidget()
        topbar.setObjectName("TopBar")
        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(32, 16, 32, 16)
        topbar_layout.setSpacing(16)
        title = QLabel("Dashboard")
        title.setObjectName("TopBarTitle")
        topbar_layout.addWidget(title)
        topbar_layout.addStretch()
        settings_btn = QPushButton("⚙️")
        settings_btn.setObjectName("SettingsButton")
        settings_btn.setFixedSize(32, 32)
        settings_btn.clicked.connect(self.open_settings_dialog)
        topbar_layout.addWidget(settings_btn)

        # View toggle
        self.view_toggle = QPushButton()
        self.view_toggle.setObjectName("ViewToggleButton")
        self.view_toggle.setCheckable(True)
        self.view_toggle.setChecked(False)
        self.view_toggle.setFixedSize(32, 32)
        style = self.style()
        if style:
            self.list_icon = style.standardIcon(QStyle.StandardPixmap.SP_FileDialogListView)
            self.grid_icon = style.standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
            self.view_toggle.setIcon(self.grid_icon)
        self.view_toggle.setIconSize(QSize(20, 20))
        self.view_toggle.setToolTip("Switch to Grid View")
        self.view_toggle.clicked.connect(self.toggle_view)
        topbar_layout.addWidget(self.view_toggle)

        # Main dashboard area
        dashboard = QWidget()
        dashboard_layout = QVBoxLayout(dashboard)
        dashboard_layout.setContentsMargins(24, 16, 24, 16)
        dashboard_layout.setSpacing(12)
        # Browse button
        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("StartButton")
        browse_btn.clicked.connect(self.browse_folder)
        dashboard_layout.addWidget(browse_btn)
        # File explorer view
        self.file_table = QTableWidget()
        self.file_table.setColumnCount(4)
        self.file_table.setHorizontalHeaderLabels(["Name", "Size", "Type", "Modified Date"])
        self.file_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.file_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        header = self.file_table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            header.sectionClicked.connect(self.sort_by_column)
        dashboard_layout.addWidget(self.file_table)
        # Placeholder for grid view
        self.grid_view = QListWidget()
        self.grid_view.setViewMode(QListView.ViewMode.IconMode)
        self.grid_view.setIconSize(QSize(96, 96))
        self.grid_view.setResizeMode(QListView.ResizeMode.Adjust)
        self.grid_view.setSpacing(16)
        self.grid_view.setVisible(False)
        dashboard_layout.addWidget(self.grid_view)
        # Results Summary
        summary_heading = QLabel("Results Summary")
        summary_heading.setObjectName("Subheading")
        dashboard_layout.addWidget(summary_heading)
        summary_desc = QLabel("After organizing, Sortlify will display the number of files moved and any errors encountered.")
        summary_desc.setWordWrap(True)
        dashboard_layout.addWidget(summary_desc)
        summary_box = QFrame()
        summary_box.setObjectName("SummaryBox")
        summary_box.setMinimumHeight(120)
        summary_box_layout = QVBoxLayout(summary_box)
        summary_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.summary_label = QLabel("<b>No files organized yet</b>\nStart organizing your files to see the results summary here.")
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_box_layout.addWidget(self.summary_label)
        dashboard_layout.addWidget(summary_box)
        note = QLabel("<span style='color:#888'>Note: Sortlify moves files to their respective categories, ensuring a safe and organized file system.</span>")
        note.setWordWrap(True)
        dashboard_layout.addWidget(note)
        dashboard_layout.addStretch()
        # Assemble layouts
        content_layout.addWidget(topbar)
        content_layout.addWidget(dashboard)
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)
        self.setCentralWidget(central)
        # Load files for explorer
        self.current_folder = None
        self.file_data = []

    def get_stylesheet(self):
        accent = {
            "blue": "#2563eb",
            "green": "#22c55e",
            "orange": "#f59e42",
            "purple": "#a259ec",
            "red": "#ef4444"
        }.get(self.accent_color, "#2563eb")
        if self.theme_mode == "light":
            bg = "#f5f6fa"
            fg = "#181e25"
            sidebar_bg = "#e9eaf0"
            border = "#d1d5db"
            summary_bg = "#fff"
            help_bg = "#e0e7ef"
        else:
            bg = "#181e25"
            fg = "#f5f6fa"
            sidebar_bg = "#14181f"
            border = "#232a34"
            summary_bg = "#181e25"
            help_bg = "#232a34"
        return f"""
        #MainWindow, #CentralWidget {{
            background: {bg};
        }}
        QWidget {{
            background: transparent;
            color: {fg};
            font-family: 'Be Vietnam Pro', Arial, sans-serif;
            font-size: 15px;
        }}
        #Sidebar {{
            background: {sidebar_bg};
            border-right: 1px solid {border};
        }}
        #Logo {{
            font-size: 20px;
            font-weight: bold;
            color: {fg};
        }}
        #TopBar {{
            background: transparent;
        }}
        #TopBarTitle {{
            font-size: 18px;
            font-weight: 600;
        }}
        #SettingsButton {{
            font-size: 20px;
            border: none;
            background: transparent;
        }}
        #SettingsButton:hover {{
            background: #2a313c;
            border-radius: 4px;
        }}
        #ViewToggleButton {{
            border: none;
            background: transparent;
        }}
        #ViewToggleButton:hover {{
            background: #2a313c;
            border-radius: 4px;
        }}
        #Heading {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        #Subheading {{
            font-size: 20px;
            font-weight: 600;
            margin-top: 16px;
            margin-bottom: 4px;
        }}
        #CategoryCheckBox {{
            spacing: 12px;
            font-size: 16px;
            margin-left: 8px;
        }}
        #StartButton {{
            background: {accent};
            color: #fff;
            border-radius: 8px;
            padding: 10px 24px;
            font-size: 16px;
            font-weight: 600;
            margin-top: 16px;
            margin-bottom: 16px;
        }}
        #StartButton:hover {{
            background: #1e40af;
        }}
        #SummaryBox {{
            border: 2px dashed {border};
            border-radius: 12px;
            background: {summary_bg};
            margin-top: 8px;
            margin-bottom: 8px;
        }}
        """

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Organize")
        if folder:
            self.current_folder = folder
            self.load_files(folder)
            self.apply_filters()

    def load_files(self, folder):
        self.file_data = []
        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            if os.path.isfile(path):
                stat = os.stat(path)
                size_mb = stat.st_size / (1024 * 1024)
                mtime = QDateTime.fromSecsSinceEpoch(int(stat.st_mtime))
                ext = os.path.splitext(file)[1].lower()
                # Find category
                category = None
                for cat, exts in self.category_map.items():
                    if ext in exts:
                        category = cat
                        break
                if not category:
                    category = "Other"
                self.file_data.append({
                    "name": file,
                    "size": size_mb,
                    "type": category,
                    "ext": ext,
                    "mtime": mtime,
                    "path": path
                })

    def apply_filters(self):
        # Filter by type
        type_val = self.type_filter.currentText() if hasattr(self, 'type_filter') else "All"
        size_val = self.size_filter.currentText() if hasattr(self, 'size_filter') else "All"
        date_val = self.date_filter.currentText() if hasattr(self, 'date_filter') else "All"
        filtered = []
        now = QDateTime.currentDateTime()
        for f in self.file_data:
            # Type
            if type_val != "All" and f["type"] != type_val:
                continue
            # Size
            if size_val == "<10" and f["size"] >= 10:
                continue
            if size_val == "10-100" and (f["size"] < 10 or f["size"] > 100):
                continue
            if size_val == ">100" and f["size"] <= 100:
                continue
            # Date
            days_ago = f["mtime"].daysTo(now)
            if date_val == "Today" and days_ago > 0:
                continue
            if date_val == "Last 7 Days" and days_ago > 7:
                continue
            if date_val == "Last Month" and days_ago > 31:
                continue
            if date_val == "Older" and days_ago <= 31:
                continue
            filtered.append(f)
        self.show_files(filtered)

    def show_files(self, files):
        if not self.view_toggle.isChecked():
            # List view
            self.file_table.setVisible(True)
            self.grid_view.setVisible(False)
            self.file_table.setRowCount(len(files))
            for row, f in enumerate(files):
                self.file_table.setItem(row, 0, QTableWidgetItem(f["name"]))
                self.file_table.setItem(row, 1, QTableWidgetItem(f"{f['size']:.2f} MB"))
                self.file_table.setItem(row, 2, QTableWidgetItem(f["type"]))
                self.file_table.setItem(row, 3, QTableWidgetItem(f["mtime"].toString("yyyy-MM-dd HH:mm")))
        else:
            # Grid/thumbnail view
            self.file_table.setVisible(False)
            self.grid_view.setVisible(True)
            self.grid_view.clear()
            for f in files:
                item = QListWidgetItem()
                item.setText(f["name"])
                if f["type"] in ["Images", "Videos"] and os.path.splitext(f["name"])[1].lower() in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".heic"]:
                    pixmap = QPixmap(f["path"])
                    if not pixmap.isNull():
                        item.setIcon(QIcon(pixmap.scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)))
                else:
                    style = self.style() if hasattr(self, 'style') else None
                    if style is not None:
                        item.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_FileIcon))
                item.setToolTip(f"Size: {f['size']:.2f} MB\nType: {f['type']}\nModified: {f['mtime'].toString('yyyy-MM-dd HH:mm')}")
                self.grid_view.addItem(item)

    def sort_by_column(self, col):
        if not hasattr(self, 'file_data') or not self.file_data:
            return
        key_map = {0: "name", 1: "size", 2: "type", 3: "mtime"}
        key = key_map.get(col, "name")
        reverse = getattr(self, '_sort_reverse', False)
        self.file_data.sort(key=lambda f: f[key], reverse=reverse)
        self._sort_reverse = not reverse
        self.apply_filters()

    def toggle_view(self):
        style = self.style()
        if not style:
            return
        if self.view_toggle.isChecked():
            self.view_toggle.setIcon(self.list_icon)
            self.view_toggle.setToolTip("Switch to List View")
        else:
            self.view_toggle.setIcon(self.grid_icon)
            self.view_toggle.setToolTip("Switch to Grid View")
        self.apply_filters()

    def open_settings_dialog(self, event=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.setModal(True)
        dialog.setMinimumSize(500, 400)
        layout = QVBoxLayout(dialog)
        tabs = QTabWidget()
        # Theme & Color Tab
        theme_tab = QWidget()
        theme_layout = QVBoxLayout(theme_tab)
        theme_layout.addWidget(QLabel("Theme:"))
        theme_combo = QComboBox()
        theme_combo.addItems(["Light", "Dark"])
        theme_combo.setCurrentText(self.theme_mode.capitalize())
        theme_layout.addWidget(theme_combo)
        theme_layout.addWidget(QLabel("Accent Color:"))
        color_combo = QComboBox()
        color_combo.addItems(["Blue", "Green", "Orange", "Purple", "Red"])
        color_combo.setCurrentText(self.accent_color.capitalize())
        theme_layout.addWidget(color_combo)
        theme_layout.addStretch()
        def apply_theme():
            self.theme_mode = theme_combo.currentText().lower()
            self.accent_color = color_combo.currentText().lower()
            self.setStyleSheet(self.get_stylesheet())
        theme_combo.currentTextChanged.connect(apply_theme)
        color_combo.currentTextChanged.connect(apply_theme)
        tabs.addTab(theme_tab, "Theme & Color")
        # Custom Rules Tab
        rules_tab = QWidget()
        rules_layout = QVBoxLayout(rules_tab)
        rules_layout.addWidget(QLabel("Add a custom rule:"))
        rule_input_layout = QHBoxLayout()
        contains_edit = QLineEdit()
        contains_edit.setPlaceholderText("If filename contains...")
        target_edit = QLineEdit()
        target_edit.setPlaceholderText("Move to category...")
        add_rule_btn = QPushButton("Add Rule")
        rule_input_layout.addWidget(contains_edit)
        rule_input_layout.addWidget(target_edit)
        rule_input_layout.addWidget(add_rule_btn)
        rules_layout.addLayout(rule_input_layout)
        rules_list = QListWidget()
        for contains, target in self.custom_rules:
            rules_list.addItem(f"If filename contains '{contains}', move to '{target}'")
        rules_layout.addWidget(rules_list)
        def add_rule():
            contains = contains_edit.text().strip()
            target = target_edit.text().strip()
            if contains and target:
                self.custom_rules.append((contains, target))
                rules_list.addItem(f"If filename contains '{contains}', move to '{target}'")
                contains_edit.clear()
                target_edit.clear()
            else:
                QMessageBox.warning(dialog, "Input Error", "Both fields are required.")
        add_rule_btn.clicked.connect(add_rule)
        def remove_rule():
            row = rules_list.currentRow()
            if row >= 0:
                rules_list.takeItem(row)
                del self.custom_rules[row]
        rules_list.itemDoubleClicked.connect(lambda _: remove_rule())
        rules_layout.addWidget(QLabel("(Double-click a rule to delete it.)"))
        rules_layout.addStretch()
        tabs.addTab(rules_tab, "Custom Rules")
        # Category Extensions Tab
        cat_tab = QWidget()
        cat_layout = QVBoxLayout(cat_tab)
        cat_layout.addWidget(QLabel("Edit category extensions:"))
        cat_list = QListWidget()
        for cat in self.category_map:
            cat_list.addItem(cat)
        cat_layout.addWidget(cat_list)
        ext_list = QListWidget()
        cat_layout.addWidget(QLabel("Extensions for selected category:"))
        cat_layout.addWidget(ext_list)
        ext_input_layout = QHBoxLayout()
        ext_edit = QLineEdit()
        ext_edit.setPlaceholderText("Add extension (e.g. .exe)")
        add_ext_btn = QPushButton("Add Extension")
        ext_input_layout.addWidget(ext_edit)
        ext_input_layout.addWidget(add_ext_btn)
        cat_layout.addLayout(ext_input_layout)
        del_ext_btn = QPushButton("Remove Selected Extension")
        cat_layout.addWidget(del_ext_btn)
        # Add/remove category
        cat_input_layout = QHBoxLayout()
        cat_name_edit = QLineEdit()
        cat_name_edit.setPlaceholderText("New category name")
        add_cat_btn = QPushButton("Add Category")
        del_cat_btn = QPushButton("Remove Selected Category")
        cat_input_layout.addWidget(cat_name_edit)
        cat_input_layout.addWidget(add_cat_btn)
        cat_input_layout.addWidget(del_cat_btn)
        cat_layout.addLayout(cat_input_layout)
        cat_layout.addStretch()
        tabs.addTab(cat_tab, "Category Extensions")
        # Logic for category/extensions editing
        def refresh_ext_list():
            ext_list.clear()
            cat_item = cat_list.currentItem()
            cat = cat_item.text() if cat_item is not None else None
            if cat and cat in self.category_map:
                for ext in self.category_map[cat]:
                    ext_list.addItem(ext)
        def on_cat_selected():
            refresh_ext_list()
        cat_list.currentItemChanged.connect(lambda *_: on_cat_selected())
        def add_extension():
            cat_item = cat_list.currentItem()
            cat = cat_item.text() if cat_item is not None else None
            ext = ext_edit.text().strip()
            if cat and ext and ext.startswith('.') and ext not in self.category_map[cat]:
                self.category_map[cat].append(ext)
                refresh_ext_list()
                ext_edit.clear()
        add_ext_btn.clicked.connect(add_extension)
        def remove_extension():
            cat_item = cat_list.currentItem()
            cat = cat_item.text() if cat_item is not None else None
            ext_item = ext_list.currentItem()
            if cat and ext_item:
                ext = ext_item.text()
                if ext in self.category_map[cat]:
                    self.category_map[cat].remove(ext)
                    refresh_ext_list()
        del_ext_btn.clicked.connect(remove_extension)
        def add_category():
            name = cat_name_edit.text().strip()
            if name and name not in self.category_map:
                self.category_map[name] = []
                cat_list.addItem(name)
                cat_name_edit.clear()
        add_cat_btn.clicked.connect(add_category)
        def remove_category():
            cat_item = cat_list.currentItem()
            cat = cat_item.text() if cat_item is not None else None
            if cat and cat not in self.builtin_categories:
                idx = cat_list.currentRow()
                cat_list.takeItem(idx)
                del self.category_map[cat]
                ext_list.clear()
        del_cat_btn.clicked.connect(remove_category)
        # Select first category by default
        if cat_list.count() > 0:
            cat_list.setCurrentRow(0)
        layout.addWidget(tabs)
        btns = QHBoxLayout()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        btns.addStretch()
        btns.addWidget(close_btn)
        layout.addLayout(btns)
        dialog.exec()

def main():
    app = QApplication(sys.argv)
    window = SortlifyMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 