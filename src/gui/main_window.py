from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, 
                           QVBoxLayout, QPushButton, QLabel, 
                           QStackedWidget, QApplication, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from .tabs.hide_tab import HideTab
from .tabs.extract_tab import ExtractTab
from .tabs.analysis_tab import AnalysisTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steganography")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)  # Thêm kích thước tối thiểu
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
        """)

        # Create main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create header with fixed height
        header = QWidget()
        header.setFixedHeight(110)  # Cố định chiều cao header
        header.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom: 1px solid #e1e4e8;
            }
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        # App title bar with fixed height
        title_bar = QWidget()
        title_bar.setFixedHeight(50)  # Cố định chiều cao title bar
        title_bar.setStyleSheet("background-color: #1a1a1a;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(25, 0, 25, 0)

        title = QLabel("Steganography")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
            }
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()

        version = QLabel("v1.0.0")
        version.setStyleSheet("color: #6e7582; font-size: 14px;")
        title_layout.addWidget(version)

        header_layout.addWidget(title_bar)

        # Navigation tabs with fixed height
        nav_container = QWidget()
        nav_container.setFixedHeight(60)  # Cố định chiều cao nav container
        nav_container.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
            }
        """)
        nav_layout = QHBoxLayout(nav_container)
        nav_layout.setContentsMargins(20, 0, 20, 0)
        nav_layout.setSpacing(5)

        self.nav_buttons = []
        nav_data = [
            ("🔒 Hide Message", "Encrypt and hide your message"),
            ("🔓 Extract Message", "Extract hidden message"),
            ("📊 Analysis", "Analyze image statistics")
        ]

        for text, tooltip in nav_data:
            btn = QPushButton(text)
            btn.setFixedHeight(45)  # Cố định chiều cao button
            btn.setMinimumWidth(150)  # Cố định chiều rộng tối thiểu
            btn.setToolTip(tooltip)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 0px 30px;
                    color: #8b949e;
                    font-size: 14px;
                    font-weight: 500;
                    border: none;
                    border-bottom: 2px solid transparent;
                    background-color: transparent;
                }
                QPushButton:hover {
                    color: white;
                    background-color: #2d2d2d;
                }
                QPushButton[Active=true] {
                    color: white;
                    border-bottom: 2px solid #0066ff;
                }
                QToolTip {
                    background-color: #2d2d2d;
                    color: white;
                    border: none;
                    padding: 8px;
                    border-radius: 6px;
                }
            """)
            self.nav_buttons.append(btn)
            nav_layout.addWidget(btn)

        nav_layout.addStretch()
        header_layout.addWidget(nav_container)
        layout.addWidget(header)

        # Content area
        content_area = QWidget()
        content_area.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
            }
        """)
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Create stacked widget for content
        self.stack = QStackedWidget()
        
        # Add pages to stack
        self.stack.addWidget(HideTab())
        self.stack.addWidget(ExtractTab())
        self.stack.addWidget(AnalysisTab())
        content_layout.addWidget(self.stack)
        layout.addWidget(content_area)

        # Connect buttons
        for i, btn in enumerate(self.nav_buttons):
            btn.clicked.connect(lambda checked, index=i: self.switch_page(index))

        # Set initial page
        self.nav_buttons[0].setProperty("Active", True)
        self.nav_buttons[0].setStyleSheet("")

    def switch_page(self, index):
        # Update button styles
        for i, btn in enumerate(self.nav_buttons):
            active = (i == index)
            btn.setProperty("Active", active)
            btn.setStyleSheet("")  # Force style refresh
        
        # Switch page
        self.stack.setCurrentIndex(index)

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main() 