from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QTextEdit, QFileDialog, QFrame, QComboBox,
                           QLineEdit, QApplication, QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt
from ..widgets.image_viewer import ImageViewer
from ..steganography.lsb import LSBSteganography
from ..steganography.dwt import DWTSteganography
from ..steganography.hybrid import HybridSteganography
import os

class ExtractTab(QWidget):
    def __init__(self):
        super().__init__()
        self.stego_methods = {
            'LSB': LSBSteganography(),
            'DWT': DWTSteganography(),
            'Hybrid': HybridSteganography()
        }
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Title area
        title_container = QWidget()
        title_container.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-bottom: 1px solid #3d3d3d;
            }
        """)
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(20, 12, 20, 12)

        title = QLabel("Extract Secret Message")
        title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: 500;
            }
        """)
        title_layout.addWidget(title)
        layout.addWidget(title_container)

        # Main content
        content = QWidget()
        content.setStyleSheet("QWidget { background-color: #1e1e1e; }")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(12)

        # Controls area
        controls = QWidget()
        controls.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-radius: 8px;
            }
        """)
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(12, 12, 12, 12)
        controls_layout.setSpacing(12)

        # Method selection
        method_layout = QHBoxLayout()
        method_label = QLabel("Method:")
        method_label.setStyleSheet("color: #ffffff; font-size: 12px;")
        self.method_combo = QComboBox()
        self.method_combo.addItems(['LSB', 'DWT', 'Hybrid'])
        self.method_combo.setStyleSheet("""
            QComboBox {
                background-color: #363636;
                color: #ffffff;
                padding: 5px 10px;
                border-radius: 3px;
                min-width: 90px;
                font-size: 12px;
                border: 1px solid #404040;
            }
            QComboBox:hover {
                background-color: #404040;
                border: 1px solid #4d4d4d;
            }
        """)
        method_layout.addWidget(method_label)
        method_layout.addWidget(self.method_combo)

        # Password input
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_label.setStyleSheet("color: #ffffff; font-size: 12px;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #363636;
                color: #ffffff;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
                border: 1px solid #404040;
            }
            QLineEdit:focus {
                border: 1px solid #0066ff;
            }
        """)
        self.password_input.setPlaceholderText("Required for DWT/Hybrid")
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)

        controls_layout.addLayout(method_layout)
        controls_layout.addLayout(password_layout)
        controls_layout.addStretch()
        content_layout.addWidget(controls)

        # Stego image area
        image_area = QWidget()
        image_area.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-radius: 8px;
            }
        """)
        image_layout = QVBoxLayout(image_area)
        image_layout.setContentsMargins(12, 12, 12, 12)
        image_layout.setSpacing(12)

        image_label = QLabel("Stego Image")
        image_label.setStyleSheet("color: #ffffff; font-size: 12px;")
        image_layout.addWidget(image_label)

        self.stego_viewer = ImageViewer()
        self.stego_viewer.setStyleSheet("""
            QWidget {
                background-color: #363636;
                border-radius: 3px;
                min-height: 200px;
            }
        """)
        image_layout.addWidget(self.stego_viewer)

        self.load_btn = QPushButton("Upload Stego Image")
        self.load_btn.setStyleSheet("""
            QPushButton {
                background-color: #363636;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 3px;
                padding: 5px 0px;
                font-size: 12px;
                min-height: 25px;
            }
            QPushButton:hover {
                background-color: #404040;
                border: 1px solid #4d4d4d;
            }
        """)
        image_layout.addWidget(self.load_btn)
        content_layout.addWidget(image_area)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 2px;
                background-color: #363636;
                height: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0066ff;
                border-radius: 2px;
            }
        """)
        self.progress_bar.hide()
        content_layout.addWidget(self.progress_bar)

        # Extract button
        self.extract_btn = QPushButton("Extract Message")
        self.extract_btn.setStyleSheet("""
            QPushButton {
                background-color: #0066ff;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                padding: 5px 0px;
                font-size: 12px;
                min-height: 25px;
            }
            QPushButton:hover {
                background-color: #0052cc;
            }
            QPushButton:disabled {
                background-color: #404040;
                color: #808080;
            }
        """)
        content_layout.addWidget(self.extract_btn)

        # Message output
        message_area = QWidget()
        message_area.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-radius: 8px;
            }
        """)
        message_layout = QVBoxLayout(message_area)
        message_layout.setContentsMargins(12, 12, 12, 12)
        message_layout.setSpacing(12)

        message_label = QLabel("Extracted Message")
        message_label.setStyleSheet("color: #ffffff; font-size: 12px;")
        message_layout.addWidget(message_label)

        self.message_output = QTextEdit()
        self.message_output.setReadOnly(True)
        self.message_output.setStyleSheet("""
            QTextEdit {
                background-color: #363636;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 3px;
                padding: 6px;
                font-size: 12px;
                min-height: 100px;
            }
        """)
        message_layout.addWidget(self.message_output)
        content_layout.addWidget(message_area)

        layout.addWidget(content)
        self.setLayout(layout)

        # Connect signals
        self.load_btn.clicked.connect(self.load_image)
        self.extract_btn.clicked.connect(self.extract_message)
        self.method_combo.currentTextChanged.connect(self.on_method_change)

    def show_dark_message(self, title, message, icon=QMessageBox.Icon.Information):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #363636;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 3px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
        """)
        msg.exec()

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Stego Image",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_name:
            self.stego_viewer.load_image(file_name)

    def on_method_change(self, method):
        if method == 'LSB':
            self.password_input.setEnabled(False)
            self.password_input.setPlaceholderText("Not required for LSB")
        else:
            self.password_input.setEnabled(True)
            self.password_input.setPlaceholderText("Required for DWT/Hybrid")

    def extract_message(self):
        if not self.stego_viewer.get_image_path():
            self.show_dark_message("Warning", "Please upload a stego image first!", QMessageBox.Icon.Warning)
            return

        method = self.method_combo.currentText()
        stego = self.stego_methods[method]

        try:
            # Show progress
            self.progress_bar.setValue(0)
            self.progress_bar.show()
            self.extract_btn.setEnabled(False)
            QApplication.processEvents()

            # Extract message
            if method == 'LSB':
                message = stego.decode(self.stego_viewer.get_image_path())
            else:
                password = self.password_input.text()
                if not password:
                    self.show_dark_message("Warning", "Password is required!", QMessageBox.Icon.Warning)
                    return
                message = stego.decode(self.stego_viewer.get_image_path(), password)

            # Update progress
            self.progress_bar.setValue(100)
            QApplication.processEvents()

            # Show message
            if message:
                self.message_output.setText(message)
                self.show_dark_message(
                    "Success",
                    "Message extracted successfully!",
                    QMessageBox.Icon.Information
                )
            else:
                self.show_dark_message(
                    "Error",
                    "No message found or invalid password!",
                    QMessageBox.Icon.Critical
                )

        except Exception as e:
            self.show_dark_message("Error", f"An error occurred: {str(e)}", QMessageBox.Icon.Critical)
        finally:
            self.extract_btn.setEnabled(True)
            self.progress_bar.hide() 