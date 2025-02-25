from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QTextEdit, QFileDialog, QFrame, QComboBox,
                           QLineEdit, QApplication, QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt
from ..widgets.image_viewer import ImageViewer
from ..steganography.lsb import LSBSteganography
from ..steganography.dwt import DWTSteganography
from ..steganography.hybrid import HybridSteganography
import cv2
import os
import tempfile

class HideTab(QWidget):
    def __init__(self):
        super().__init__()
        # Khởi tạo các biến
        self.temp_path = None
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

        title = QLabel("Hide Secret Message")
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
        content.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
            }
        """)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(12)

        # Method and password container
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
        method_label.setStyleSheet("color: #ffffff; font-size: 14px;")
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
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        method_layout.addWidget(method_label)
        method_layout.addWidget(self.method_combo)
        controls_layout.addLayout(method_layout)

        # Password input
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_label.setStyleSheet("color: #ffffff; font-size: 14px;")
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
        self.password_input.setPlaceholderText("Optional")
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        controls_layout.addLayout(password_layout)
        controls_layout.addStretch()
        content_layout.addWidget(controls)

        # Image and message area
        work_area = QWidget()
        work_area.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-radius: 8px;
            }
        """)
        work_layout = QHBoxLayout(work_area)
        work_layout.setContentsMargins(12, 12, 12, 12)
        work_layout.setSpacing(12)

        # Left side - Original image
        left_layout = QVBoxLayout()
        original_label = QLabel("Original Image")
        original_label.setStyleSheet("color: #ffffff; font-size: 13px;")
        left_layout.addWidget(original_label)
        
        self.original_viewer = ImageViewer()
        self.original_viewer.setStyleSheet("""
            QWidget {
                background-color: #363636;
                border-radius: 3px;
                min-height: 200px;
            }
        """)
        left_layout.addWidget(self.original_viewer)
        
        self.load_btn = QPushButton("Upload Image")
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
        left_layout.addWidget(self.load_btn)
        work_layout.addLayout(left_layout)

        # Right side - Message input
        right_layout = QVBoxLayout()
        message_label = QLabel("Secret Message")
        message_label.setStyleSheet("color: #ffffff; font-size: 13px;")
        right_layout.addWidget(message_label)
        
        self.msg_input = QTextEdit()
        self.msg_input.setStyleSheet("""
            QTextEdit {
                background-color: #363636;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 3px;
                padding: 6px;
                font-size: 12px;
                min-height: 200px;
            }
            QTextEdit:focus {
                border: 1px solid #0066ff;
            }
        """)
        self.msg_input.setPlaceholderText("Enter your secret message here...")
        right_layout.addWidget(self.msg_input)
        
        self.hide_btn = QPushButton("Hide Message")
        self.hide_btn.setStyleSheet("""
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
        right_layout.addWidget(self.hide_btn)
        work_layout.addLayout(right_layout)
        content_layout.addWidget(work_area)

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

        # Result area
        result_area = QWidget()
        result_area.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-radius: 8px;
            }
        """)
        result_layout = QVBoxLayout(result_area)
        result_layout.setContentsMargins(12, 12, 12, 12)
        
        result_label = QLabel("Result")
        result_label.setStyleSheet("color: #ffffff; font-size: 12px;")
        result_layout.addWidget(result_label)
        
        self.stego_viewer = ImageViewer()
        self.stego_viewer.setStyleSheet("""
            QWidget {
                background-color: #363636;
                border-radius: 3px;
                min-height: 200px;
            }
        """)
        result_layout.addWidget(self.stego_viewer)
        
        self.save_btn = QPushButton("Save Image")
        self.save_btn.setStyleSheet("""
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
        result_layout.addWidget(self.save_btn)
        content_layout.addWidget(result_area)

        layout.addWidget(content)
        self.setLayout(layout)

        # Connect signals
        self.load_btn.clicked.connect(self.load_image)
        self.hide_btn.clicked.connect(self.hide_message)
        self.save_btn.clicked.connect(self.save_image)
        self.method_combo.currentTextChanged.connect(self.on_method_change)

    def on_method_change(self, method):
        # Enable/disable password based on method
        self.password_input.setEnabled(method in ['DWT', 'Hybrid'])
        if method == 'LSB':
            self.password_input.setPlaceholderText("Password not supported in LSB mode")
        else:
            self.password_input.setPlaceholderText("Enter password to encrypt message")

    def hide_message(self):
        if not self.original_viewer.get_image_path():
            self.show_dark_message("Warning", "Please upload an image first!", QMessageBox.Icon.Warning)
            return

        message = self.msg_input.toPlainText()
        if not message:
            self.show_dark_message("Warning", "Please enter a message!", QMessageBox.Icon.Warning)
            return

        # Lấy phương thức được chọn
        method = self.method_combo.currentText()
        stego = self.stego_methods[method]
        
        try:
            # Show progress bar
            self.progress_bar.setValue(0)
            self.progress_bar.show()
            self.hide_btn.setEnabled(False)
            QApplication.processEvents()

            # Hide message - chỉ dùng password cho DWT và Hybrid
            if method == 'LSB':
                stego_image = stego.encode(
                    self.original_viewer.get_image_path(),
                    message
                )
            else:
                password = self.password_input.text()
                stego_image = stego.encode(
                    self.original_viewer.get_image_path(),
                    message,
                    password
                )

            # Update progress
            self.progress_bar.setValue(50)
            QApplication.processEvents()

            # Save and display result
            if self.temp_path and os.path.exists(self.temp_path):
                os.remove(self.temp_path)
            
            self.temp_path = os.path.join(tempfile.gettempdir(), f"temp_stego_{method}.png")
            cv2.imwrite(self.temp_path, stego_image)
            self.stego_viewer.load_image(self.temp_path)

            # Calculate metrics
            metrics = stego.calculate_metrics(
                self.original_viewer.get_image_path(),
                self.temp_path
            )

            # Update progress
            self.progress_bar.setValue(100)
            QApplication.processEvents()

            # Show results
            info_text = (
                f"Message hidden successfully using {method}!\n\n"
                f"Image Quality (PSNR): {metrics['psnr']:.2f} dB\n"
                f"Maximum capacity: {metrics['capacity']} bytes\n"
                f"Message size: {len(message)} bytes\n"
                f"Password protected: {'Yes' if method != 'LSB' else 'No'}\n\n"
                f"Use Save Image to keep the result."
            )
            
            self.show_dark_message(
                "Success", 
                info_text,
                QMessageBox.Icon.Information
            )

        except Exception as e:
            self.show_dark_message("Error", f"An error occurred: {str(e)}", QMessageBox.Icon.Critical)
        finally:
            self.hide_btn.setEnabled(True)
            self.progress_bar.hide()

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.original_viewer.load_image(file_name)

    def show_dark_message(self, title, text, icon):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        
        # Style cho dark theme message box
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
            }
            QMessageBox QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #404040;
            }
            QMessageBox QPushButton:pressed {
                background-color: #505050;
            }
        """)
        
        msg.exec()

    def save_image(self):
        if not self.stego_viewer.get_image_path():
            self.show_dark_message("Warning", "No stego image to save!", QMessageBox.Icon.Warning)
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Stego Image",
            "",
            "PNG Files (*.png)"
        )
        if file_name:
            try:
                stego_image = cv2.imread(self.stego_viewer.get_image_path())
                cv2.imwrite(file_name, stego_image)
                self.show_dark_message(
                    "Success", 
                    "Stego image saved successfully!",
                    QMessageBox.Icon.Information
                )
            except Exception as e:
                self.show_dark_message(
                    "Error", 
                    f"Failed to save image: {str(e)}",
                    QMessageBox.Icon.Critical
                )

    def closeEvent(self, event):
        # Cleanup temp file when closing
        if self.temp_path and os.path.exists(self.temp_path):
            try:
                os.remove(self.temp_path)
            except:
                pass
        super().closeEvent(event) 