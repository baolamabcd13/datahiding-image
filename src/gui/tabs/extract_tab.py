from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QTextEdit, QFileDialog, QFrame)
from PyQt6.QtCore import Qt
from ..widgets.image_viewer import ImageViewer

class ExtractTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("Extract Hidden Message")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2d3436;
            }
        """)
        layout.addWidget(title)

        # Content container
        content = QFrame()
        content.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
            }
        """)
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # Left section (Stego Image)
        left_section = QVBoxLayout()
        stego_label = QLabel("Stego Image")
        stego_label.setStyleSheet("font-weight: bold; color: #2d3436;")
        left_section.addWidget(stego_label)
        
        self.image_viewer = ImageViewer()  # Removed title parameter
        left_section.addWidget(self.image_viewer)
        
        self.load_btn = QPushButton("Load Stego Image")
        self.load_btn.setStyleSheet("""
            QPushButton {
                background-color: #0066ff;
                color: white;
                border-radius: 6px;
                padding: 8px 15px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0052cc;
            }
        """)
        left_section.addWidget(self.load_btn)
        left_section.addStretch()
        content_layout.addLayout(left_section)

        # Right section (Extracted Message)
        right_section = QVBoxLayout()
        msg_label = QLabel("Extracted Message")
        msg_label.setStyleSheet("font-weight: bold; color: #2d3436;")
        right_section.addWidget(msg_label)

        self.msg_output = QTextEdit()
        self.msg_output.setReadOnly(True)
        self.msg_output.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e1e4e8;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
                background-color: #f8f9fa;
            }
        """)
        self.msg_output.setMinimumHeight(200)
        right_section.addWidget(self.msg_output)

        self.extract_btn = QPushButton("Extract Message")
        self.extract_btn.setStyleSheet("""
            QPushButton {
                background-color: #0066ff;
                color: white;
                border-radius: 6px;
                padding: 8px 15px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0052cc;
            }
        """)
        right_section.addWidget(self.extract_btn)
        right_section.addStretch()
        content_layout.addLayout(right_section)

        layout.addWidget(content)

        # Connect buttons
        self.load_btn.clicked.connect(self.load_image)
        self.extract_btn.clicked.connect(self.extract_message)

        self.setLayout(layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Stego Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.image_viewer.load_image(file_name)

    def extract_message(self):
        if self.image_viewer.get_image_path():
            # TODO: Implement extraction logic
            self.msg_output.setText("Extracted message will appear here...") 