from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
import cv2
import numpy as np
from PIL import Image
import io

class ImageViewer(QLabel):
    def __init__(self):
        super().__init__()
        self.image_path = None
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(200, 150)
        self.setMaximumHeight(300)
        self.setStyleSheet("""
            QLabel {
                background-color: #363636;
                border: 1px solid #404040;
                border-radius: 3px;
            }
        """)

    def load_image(self, image_path):
        """Load image from file path"""
        self.image_path = image_path
        image = cv2.imread(image_path)
        if image is not None:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self._display_image(image)

    def load_image_from_array(self, image_array):
        """Load image from numpy array (BGR format)"""
        if image_array is not None:
            if len(image_array.shape) == 2:  # Grayscale
                image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)
            elif image_array.shape[2] == 3:  # BGR
                image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            self._display_image(image_array)

    def load_image_from_pil(self, pil_image):
        """Load image from PIL Image object"""
        if pil_image is not None:
            # Convert PIL image to numpy array
            image_array = np.array(pil_image)
            if len(image_array.shape) == 2:  # Grayscale
                image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)
            elif image_array.shape[2] == 4:  # RGBA
                image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
            self._display_image(image_array)

    def _display_image(self, image_array):
        """Display image array in the label"""
        h, w = image_array.shape[:2]
        bytes_per_line = 3 * w

        # Create QImage from numpy array
        q_image = QImage(
            image_array.data,
            w, h,
            bytes_per_line,
            QImage.Format.Format_RGB888
        )

        # Scale image to fit the label while maintaining aspect ratio
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)

    def get_image_path(self):
        """Return the current image path"""
        return self.image_path

    def resizeEvent(self, event):
        """Handle resize events to maintain aspect ratio"""
        super().resizeEvent(event)
        if self.pixmap():
            scaled_pixmap = self.pixmap().scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.setPixmap(scaled_pixmap) 