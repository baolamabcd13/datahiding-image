from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QTextEdit, QFileDialog, QFrame)
from PyQt6.QtCore import Qt
from ..widgets.image_viewer import ImageViewer

class HideTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("Hide Secret Message")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2d3436;
            }
        """)
        layout.addWidget(title)

        # Main content container with horizontal layout
        content = QFrame()
        content.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
            }
        """)
        main_layout = QHBoxLayout(content)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Left section (Original Image)
        left_section = QVBoxLayout()
        original_label = QLabel("Original Image")
        original_label.setStyleSheet("font-weight: bold; color: #2d3436;")
        left_section.addWidget(original_label)
        
        self.original_viewer = ImageViewer()
        left_section.addWidget(self.original_viewer)
        
        self.load_btn = QPushButton("Upload Image")
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
        main_layout.addLayout(left_section)

        # Middle section (Message and Process)
        middle_section = QVBoxLayout()
        msg_label = QLabel("Secret Message")
        msg_label.setStyleSheet("font-weight: bold; color: #2d3436;")
        middle_section.addWidget(msg_label)

        self.msg_input = QTextEdit()
        self.msg_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e1e4e8;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }
            QTextEdit:focus {
                border-color: #0066ff;
            }
        """)
        self.msg_input.setFixedHeight(80)
        middle_section.addWidget(self.msg_input)

        # Process button and indicator
        self.hide_btn = QPushButton("Hide Message")
        self.hide_btn.setStyleSheet("""
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
        middle_section.addWidget(self.hide_btn)

        process_indicator = QLabel("⟶")
        process_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        process_indicator.setStyleSheet("font-size: 24px; color: #0066ff;")
        middle_section.addWidget(process_indicator)
        
        middle_section.addStretch()
        main_layout.addLayout(middle_section)

        # Right section (Stego Image)
        right_section = QVBoxLayout()
        stego_label = QLabel("Stego Image")
        stego_label.setStyleSheet("font-weight: bold; color: #2d3436;")
        right_section.addWidget(stego_label)
        
        self.stego_viewer = ImageViewer()
        right_section.addWidget(self.stego_viewer)
        
        self.save_btn = QPushButton("Save Image")
        self.save_btn.setStyleSheet("""
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
        right_section.addWidget(self.save_btn)
        right_section.addStretch()
        main_layout.addLayout(right_section)

        layout.addWidget(content)

        # Connect buttons
        self.load_btn.clicked.connect(self.load_image)
        self.hide_btn.clicked.connect(self.hide_message)
        self.save_btn.clicked.connect(self.save_image)

        self.setLayout(layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.original_viewer.load_image(file_name)

    def hide_message(self):
        if self.original_viewer.get_image_path():
            # TODO: Implement hiding logic
            self.stego_viewer.load_image(self.original_viewer.get_image_path())

    def save_image(self):
        if self.stego_viewer.get_image_path():
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save Image", "", "PNG Files (*.png)")
            if file_name:
                # TODO: Implement save logic
                pass 