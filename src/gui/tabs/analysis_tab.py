from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QFrame, QGridLayout, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from ..widgets.image_viewer import ImageViewer
from ..steganography.analyst import SteganographyAnalyst

class AnalysisTab(QWidget):
    def __init__(self):
        super().__init__()
        self.analyst = SteganographyAnalyst()
        self.init_ui()

    def init_ui(self):
        # Main layout
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

        title = QLabel("Steganography Analysis")
        title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: 500;
            }
        """)
        title_layout.addWidget(title)
        layout.addWidget(title_container)

        # Content
        content = QWidget()
        content.setStyleSheet("QWidget { background-color: #1e1e1e; }")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(16)

        # Images Grid
        images_grid = QHBoxLayout()
        images_grid.setSpacing(16)

        # Original Image
        original_section = self._create_section("Original Image")
        self.original_viewer = ImageViewer()
        original_section.layout().addWidget(self.original_viewer)
        images_grid.addWidget(original_section)

        # Stego Image
        stego_section = self._create_section("Stego Image")
        self.stego_viewer = ImageViewer()
        stego_section.layout().addWidget(self.stego_viewer)
        images_grid.addWidget(stego_section)

        content_layout.addLayout(images_grid)

        # Metrics Section
        metrics_section = self._create_section("Analysis Results")
        metrics_layout = QGridLayout()
        metrics_layout.setColumnStretch(1, 1)
        
        self.metrics_labels = {
            'psnr': QLabel("PSNR: -"),
            'mse': QLabel("MSE: -"),
            'ssim': QLabel("SSIM: -"),
            'histogram_diff': QLabel("Histogram Difference: -"),
            'chi_square': QLabel("Chi-Square: -")
        }

        row = 0
        for key, label in self.metrics_labels.items():
            label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 13px;
                    padding: 4px 0;
                }
            """)
            metrics_layout.addWidget(label, row, 0)
            row += 1

        metrics_section.layout().addLayout(metrics_layout)
        content_layout.addWidget(metrics_section)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        self.load_original_btn = self._create_button("Load Original")
        self.load_stego_btn = self._create_button("Load Stego")
        self.analyze_btn = self._create_button("Analyze")
        
        button_layout.addWidget(self.load_original_btn)
        button_layout.addWidget(self.load_stego_btn)
        button_layout.addWidget(self.analyze_btn)
        button_layout.addStretch()

        content_layout.addLayout(button_layout)
        layout.addWidget(content)

        # Connect buttons
        self.load_original_btn.clicked.connect(self.load_original)
        self.load_stego_btn.clicked.connect(self.load_stego)
        self.analyze_btn.clicked.connect(self.analyze)

        self.setLayout(layout)

    def _create_section(self, title):
        section = QWidget()
        section.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-radius: 6px;
            }
        """)
        layout = QVBoxLayout(section)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        label = QLabel(title)
        label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 12px;
                font-weight: 500;
            }
        """)
        layout.addWidget(label)
        return section

    def _create_button(self, text):
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #363636;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 3px;
                padding: 5px 15px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #404040;
                border: 1px solid #4d4d4d;
            }
        """)
        return btn

    def analyze(self):
        if not self.original_viewer.get_image_path() or not self.stego_viewer.get_image_path():
            self.show_dark_message("Warning", "Please load both original and stego images!", 
                                 QMessageBox.Icon.Warning)
            return

        try:
            # Get analysis results
            metrics = self.analyst.calculate_metrics(
                self.original_viewer.get_image_path(),
                self.stego_viewer.get_image_path()
            )
            
            # Update metrics labels
            self.metrics_labels['psnr'].setText(f"PSNR: {metrics['psnr']:.2f} dB")
            self.metrics_labels['mse'].setText(f"MSE: {metrics['mse']:.6f}")
            self.metrics_labels['ssim'].setText(f"SSIM: {metrics['ssim']:.4f}")
            self.metrics_labels['histogram_diff'].setText(f"Histogram Difference: {metrics['histogram_difference']:.2f}")
            self.metrics_labels['chi_square'].setText(f"Chi-Square: {metrics['chi_square']:.2f}")

            self.show_dark_message("Success", "Analysis completed successfully!")

        except Exception as e:
            self.show_dark_message("Error", f"An error occurred: {str(e)}", 
                                 QMessageBox.Icon.Critical)

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

    def load_original(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Original Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            self.original_viewer.load_image(file_name)

    def load_stego(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Stego Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            self.stego_viewer.load_image(file_name) 