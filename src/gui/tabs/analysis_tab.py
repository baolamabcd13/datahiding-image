from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QFrame, QGridLayout, QFileDialog)
from PyQt6.QtCore import Qt
from ..widgets.image_viewer import ImageViewer

class AnalysisTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("Image Analysis")
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
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # Images grid
        images_grid = QGridLayout()
        
        # Original Image
        original_section = QVBoxLayout()
        original_label = QLabel("Original Image")
        original_label.setStyleSheet("font-weight: bold; color: #2d3436;")
        original_section.addWidget(original_label)
        self.original_viewer = ImageViewer()
        original_section.addWidget(self.original_viewer)
        images_grid.addLayout(original_section, 0, 0)

        # Stego Image
        stego_section = QVBoxLayout()
        stego_label = QLabel("Stego Image")
        stego_label.setStyleSheet("font-weight: bold; color: #2d3436;")
        stego_section.addWidget(stego_label)
        self.stego_viewer = ImageViewer()
        stego_section.addWidget(self.stego_viewer)
        images_grid.addLayout(stego_section, 0, 1)

        # Histogram
        histogram_section = QVBoxLayout()
        histogram_label = QLabel("Histogram")
        histogram_label.setStyleSheet("font-weight: bold; color: #2d3436;")
        histogram_section.addWidget(histogram_label)
        self.histogram_viewer = ImageViewer()
        histogram_section.addWidget(self.histogram_viewer)
        images_grid.addLayout(histogram_section, 1, 0)

        # Difference
        difference_section = QVBoxLayout()
        difference_label = QLabel("Difference")
        difference_label.setStyleSheet("font-weight: bold; color: #2d3436;")
        difference_section.addWidget(difference_label)
        self.difference_viewer = ImageViewer()
        difference_section.addWidget(self.difference_viewer)
        images_grid.addLayout(difference_section, 1, 1)

        content_layout.addLayout(images_grid)

        # Analysis Results
        results_frame = QFrame()
        results_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        results_layout = QHBoxLayout(results_frame)

        self.psnr_label = QLabel("PSNR: -")
        self.mse_label = QLabel("MSE: -")
        self.capacity_label = QLabel("Capacity: -")
        
        for label in [self.psnr_label, self.mse_label, self.capacity_label]:
            label.setStyleSheet("""
                QLabel {
                    color: #2d3436;
                    font-size: 13px;
                    padding: 5px 10px;
                }
            """)
            results_layout.addWidget(label)

        content_layout.addWidget(results_frame)

        # Buttons
        btn_layout = QHBoxLayout()
        self.load_original_btn = QPushButton("Load Original")
        self.load_stego_btn = QPushButton("Load Stego")
        self.analyze_btn = QPushButton("Analyze")

        for btn in [self.load_original_btn, self.load_stego_btn, self.analyze_btn]:
            btn.setStyleSheet("""
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
            btn_layout.addWidget(btn)

        content_layout.addLayout(btn_layout)
        layout.addWidget(content)

        # Connect buttons
        self.load_original_btn.clicked.connect(self.load_original)
        self.load_stego_btn.clicked.connect(self.load_stego)
        self.analyze_btn.clicked.connect(self.analyze)

        self.setLayout(layout)

    def load_original(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Original Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.original_viewer.load_image(file_name)

    def load_stego(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Stego Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.stego_viewer.load_image(file_name)

    def analyze(self):
        if self.original_viewer.get_image_path() and self.stego_viewer.get_image_path():
            # TODO: Implement analysis logic
            self.psnr_label.setText("PSNR: 45.3 dB")
            self.mse_label.setText("MSE: 0.0019")
            self.capacity_label.setText("Capacity: 1024 bytes") 