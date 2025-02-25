import cv2
import numpy as np
import pywt
from cryptography.fernet import Fernet
import base64
from hashlib import sha256

class DWTSteganography:
    def __init__(self):
        self.delimiter = "$$END$$"
        self.wavelet = 'haar'
        self.threshold = 30  # Ngưỡng để nhúng bit

    def _get_key_from_password(self, password):
        if not password:
            raise ValueError("Password is required for DWT method")
        key = sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(key)

    def _encrypt_message(self, message, password):
        key = self._get_key_from_password(password)
        f = Fernet(key)
        return f.encrypt(message.encode())

    def _decrypt_message(self, encrypted_message, password):
        key = self._get_key_from_password(password)
        f = Fernet(key)
        return f.decrypt(encrypted_message).decode()

    def encode(self, image_path, message, password):
        # Đọc ảnh
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")

        # Mã hóa tin nhắn
        encrypted = self._encrypt_message(message + self.delimiter, password)
        binary_message = ''.join(format(byte, '08b') for byte in encrypted)
        message_length = len(binary_message)

        # Tách các kênh màu
        b, g, r = cv2.split(image)

        # Áp dụng DWT cho kênh xanh
        coeffs = pywt.dwt2(b.astype(float), self.wavelet)
        cA, (cH, cV, cD) = coeffs

        # Kiểm tra dung lượng
        max_capacity = (cH.shape[0] * cH.shape[1])
        if message_length > max_capacity:
            raise ValueError(f"Message too large. Maximum capacity: {max_capacity} bits")

        # Nhúng tin nhắn vào hệ số chi tiết ngang (cH)
        msg_idx = 0
        modified_cH = cH.copy()
        
        for i in range(cH.shape[0]):
            for j in range(cH.shape[1]):
                if msg_idx < message_length:
                    current_value = modified_cH[i, j]
                    if binary_message[msg_idx] == '1':
                        # Đảm bảo giá trị dương và đủ lớn cho bit 1
                        modified_cH[i, j] = abs(current_value) + 50
                    else:
                        # Đảm bảo giá trị gần 0 cho bit 0
                        modified_cH[i, j] = current_value * 0.1
                    msg_idx += 1

        # Áp dụng IDWT
        coeffs = (cA, (modified_cH, cV, cD))
        modified_b = pywt.idwt2(coeffs, self.wavelet)

        # Chuẩn hóa kênh xanh
        modified_b = np.clip(modified_b, 0, 255)
        modified_b = modified_b.astype(np.uint8)

        # Blend với tỷ lệ thích hợp để giữ màu sắc
        alpha = 0.85  # Tăng tỷ lệ của kênh đã sửa
        modified_b = cv2.addWeighted(modified_b, alpha, b, 1-alpha, 0)

        # Tạo ảnh stego
        stego = cv2.merge([modified_b, g, r])
        return stego

    def decode(self, stego_image_path, password):
        # Đọc ảnh stego
        stego = cv2.imread(stego_image_path)
        if stego is None:
            raise ValueError("Could not read stego image")

        # Lấy kênh xanh và áp dụng DWT
        blue = stego[:, :, 0].astype(float)
        coeffs = pywt.dwt2(blue, self.wavelet)
        _, (cH, _, _) = coeffs

        # Trích xuất tin nhắn với ngưỡng cố định
        binary_message = ''
        threshold = 25  # Ngưỡng cố định để phân biệt bit 0 và 1
        
        for i in range(cH.shape[0]):
            for j in range(cH.shape[1]):
                if len(binary_message) >= 20000 * 8:  # Giới hạn kích thước
                    break
                # Sử dụng ngưỡng cố định
                bit = '1' if abs(cH[i, j]) > threshold else '0'
                binary_message += bit

                # Thử giải mã sau mỗi 8 bytes
                if len(binary_message) % 64 == 0:
                    try:
                        bytes_data = bytearray()
                        for k in range(0, len(binary_message), 8):
                            if k + 8 <= len(binary_message):
                                bytes_data.append(int(binary_message[k:k+8], 2))
                        
                        decrypted = self._decrypt_message(bytes(bytes_data), password)
                        if self.delimiter in decrypted:
                            return decrypted[:decrypted.index(self.delimiter)]
                    except:
                        continue

        raise ValueError("No valid message found or incorrect password")

    def calculate_metrics(self, original_image_path, stego_image_path):
        original = cv2.imread(original_image_path)
        stego = cv2.imread(stego_image_path)

        if original is None or stego is None:
            raise ValueError("Could not read images")

        if original.shape != stego.shape:
            raise ValueError("Images have different dimensions")

        mse = np.mean((original - stego) ** 2)
        if mse == 0:
            psnr = float('inf')
        else:
            psnr = 20 * np.log10(255.0 / np.sqrt(mse))

        # Tính dung lượng
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        coeffs = pywt.dwt2(gray, self.wavelet)
        _, (cH, _, _) = coeffs
        capacity = (cH.shape[0] * cH.shape[1]) // 8

        return {
            'psnr': psnr,
            'mse': mse,
            'capacity': capacity
        } 