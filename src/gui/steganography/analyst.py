import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr

class SteganographyAnalyst:
    def __init__(self):
        pass

    def calculate_metrics(self, original_image_path, stego_image_path):
        """Tính toán các chỉ số đánh giá chất lượng"""
        # Đọc ảnh
        original = cv2.imread(original_image_path)
        stego = cv2.imread(stego_image_path)

        if original is None or stego is None:
            raise ValueError("Could not read images")

        if original.shape != stego.shape:
            raise ValueError("Images have different dimensions")

        # Chuyển sang ảnh xám để tính SSIM
        original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        stego_gray = cv2.cvtColor(stego, cv2.COLOR_BGR2GRAY)

        # Tính MSE
        mse = np.mean((original - stego) ** 2)

        # Tính PSNR
        if mse == 0:
            psnr_value = float('inf')
        else:
            psnr_value = 20 * np.log10(255.0 / np.sqrt(mse))

        # Tính SSIM
        ssim_value = ssim(original_gray, stego_gray)

        # Tính histogram difference
        hist_diff = self._calculate_histogram_difference(original, stego)

        # Tính chi-square test
        chi_square = self._calculate_chi_square(original, stego)

        return {
            'psnr': psnr_value,
            'mse': mse,
            'ssim': ssim_value,
            'histogram_difference': hist_diff,
            'chi_square': chi_square
        }

    def _calculate_histogram_difference(self, original, stego):
        """Tính sự khác biệt histogram giữa hai ảnh"""
        hist_diff = 0
        for channel in range(3):  # BGR channels
            hist_orig = cv2.calcHist([original], [channel], None, [256], [0, 256])
            hist_stego = cv2.calcHist([stego], [channel], None, [256], [0, 256])
            hist_diff += np.sum(np.abs(hist_orig - hist_stego))
        return hist_diff / 3  # Trung bình trên 3 kênh màu

    def _calculate_chi_square(self, original, stego):
        """Tính chi-square test giữa hai ảnh"""
        chi_square = 0
        for channel in range(3):
            hist_orig = cv2.calcHist([original], [channel], None, [256], [0, 256])
            hist_stego = cv2.calcHist([stego], [channel], None, [256], [0, 256])
            # Tránh chia cho 0
            hist_orig = hist_orig + 1e-10
            chi_square += np.sum((hist_orig - hist_stego) ** 2 / hist_orig)
        return chi_square / 3

    def analyze_noise_pattern(self, original_image_path, stego_image_path):
        """Phân tích pattern nhiễu"""
        original = cv2.imread(original_image_path)
        stego = cv2.imread(stego_image_path)

        if original is None or stego is None:
            raise ValueError("Could not read images")

        # Tính difference image
        diff = cv2.absdiff(original, stego)
        
        # Tăng contrast để thấy rõ sự khác biệt
        diff = cv2.convertScaleAbs(diff, alpha=5, beta=0)

        # Tính histogram của ảnh difference
        hist_diff = []
        for channel in range(3):
            hist = cv2.calcHist([diff], [channel], None, [256], [0, 256])
            hist_diff.append(hist.flatten())

        return {
            'difference_image': diff,
            'difference_histogram': hist_diff
        }

    def analyze_bit_planes(self, image_path):
        """Phân tích các bit plane của ảnh"""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")

        bit_planes = []
        for bit in range(8):
            # Tạo mask cho từng bit
            plane = np.bitwise_and(image, 2**bit)
            plane = plane * 255 // (2**bit)  # Normalize để hiển thị
            bit_planes.append(plane.astype(np.uint8))

        return bit_planes

    def generate_report(self, original_image_path, stego_image_path):
        """Tạo báo cáo tổng hợp"""
        metrics = self.calculate_metrics(original_image_path, stego_image_path)
        noise_analysis = self.analyze_noise_pattern(original_image_path, stego_image_path)
        bit_planes = self.analyze_bit_planes(stego_image_path)

        report = {
            'metrics': metrics,
            'noise_analysis': noise_analysis,
            'bit_planes': bit_planes,
            'recommendations': self._generate_recommendations(metrics)
        }

        return report

    def _generate_recommendations(self, metrics):
        """Tạo các khuyến nghị dựa trên kết quả phân tích"""
        recommendations = []

        # Đánh giá PSNR
        if metrics['psnr'] < 30:
            recommendations.append("PSNR thấp, cần cải thiện chất lượng ảnh")
        elif metrics['psnr'] > 40:
            recommendations.append("PSNR tốt, chất lượng ảnh được duy trì")

        # Đánh giá SSIM
        if metrics['ssim'] < 0.95:
            recommendations.append("SSIM thấp, cấu trúc ảnh bị thay đổi đáng kể")
        elif metrics['ssim'] > 0.98:
            recommendations.append("SSIM tốt, cấu trúc ảnh được bảo toàn")

        # Đánh giá histogram
        if metrics['histogram_difference'] > 1000:
            recommendations.append("Histogram thay đổi nhiều, có thể dễ bị phát hiện")
        elif metrics['histogram_difference'] < 500:
            recommendations.append("Histogram ổn định, khó phát hiện")

        return recommendations 