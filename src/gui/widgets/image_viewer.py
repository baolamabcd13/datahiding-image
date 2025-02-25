from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
import cv2
import numpy as np

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.image_path = None

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Image container
        self.container = QWidget()
        self.container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: 2px dashed #e1e4e8;
                border-radius: 8px;
            }
        """)
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(5, 5, 5, 5)
        
        # Image display
        self.image_label = QLabel("Drop image here\nor click to upload")
        self.image_label.setStyleSheet("""
            QLabel {
                color: #6e7582;
                font-size: 12px;
            }
        """)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(200, 200)
        self.image_label.setMaximumSize(200, 200)
        container_layout.addWidget(self.image_label)
        
        layout.addWidget(self.container)
        self.setLayout(layout)

    def load_image(self, image_path):
        self.image_path = image_path
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(
            200, 200,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)

    def get_image_path(self):
        return self.image_path

    def set_image_from_array(self, image_array):
        height, width = image_array.shape[:2]
        bytes_per_line = 3 * width
        image = QImage(image_array.data, width, height, 
                      bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(300, 300, 
                                    Qt.AspectRatioMode.KeepAspectRatio,
                                    Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap) 