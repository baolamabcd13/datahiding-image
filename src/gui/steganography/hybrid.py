import cv2
import numpy as np
import pywt
from cryptography.fernet import Fernet
import base64
from hashlib import sha256

class HybridSteganography:
    def __init__(self):
        self.delimiter = "$$END$$"
        self.wavelet = 'haar'

    def _get_key_from_password(self, password):
        """Generate Fernet key from password"""
        if not password:
            raise ValueError("Password is required for Hybrid method")
        key = sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(key)

    def _encrypt_message(self, message, password):
        """Encrypt message using Fernet encryption"""
        key = self._get_key_from_password(password)
        f = Fernet(key)
        return f.encrypt(message.encode())

    def _decrypt_message(self, encrypted_message, password):
        """Decrypt message using Fernet encryption"""
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

        # Tách kênh màu
        b, g, r = cv2.split(image)

        # Áp dụng DWT cho kênh xanh
        coeffs = pywt.dwt2(b.astype(float), self.wavelet)
        cA, (cH, cV, cD) = coeffs

        # Nhúng tin nhắn vào cả hệ số DWT và LSB
        msg_idx = 0
        modified_cH = cH.copy()
        modified_b = b.copy()

        for i in range(cH.shape[0]):
            for j in range(cH.shape[1]):
                if msg_idx < len(binary_message):
                    # Nhúng vào DWT
                    if binary_message[msg_idx] == '1':
                        modified_cH[i, j] = 50
                    else:
                        modified_cH[i, j] = -50

                    # Nhúng vào LSB của pixel tương ứng
                    if binary_message[msg_idx] == '1':
                        modified_b[i*2, j*2] = modified_b[i*2, j*2] | 1
                    else:
                        modified_b[i*2, j*2] = modified_b[i*2, j*2] & ~1
                    
                    msg_idx += 1

        # Áp dụng IDWT
        coeffs = (cA, (modified_cH, cV, cD))
        dwt_b = pywt.idwt2(coeffs, self.wavelet)
        dwt_b = np.clip(dwt_b, 0, 255).astype(np.uint8)

        # Kết hợp DWT và LSB
        final_b = cv2.addWeighted(dwt_b, 0.7, modified_b, 0.3, 0)
        
        # Tạo ảnh stego
        stego = cv2.merge([final_b, g, r])
        return stego

    def decode(self, stego_image_path, password):
        # Đọc ảnh stego
        stego = cv2.imread(stego_image_path)
        if stego is None:
            raise ValueError("Could not read stego image")

        # Lấy kênh xanh
        blue = stego[:, :, 0]

        # Trích xuất từ DWT
        coeffs = pywt.dwt2(blue.astype(float), self.wavelet)
        _, (cH, _, _) = coeffs

        # Trích xuất bit từ cả DWT và LSB
        binary_message = ''
        for i in range(cH.shape[0]):
            for j in range(cH.shape[1]):
                if len(binary_message) >= 20000:
                    break
                
                # Lấy bit từ DWT
                dwt_bit = '1' if cH[i, j] > 0 else '0'
                # Lấy bit từ LSB
                lsb_bit = '1' if (blue[i*2, j*2] & 1) else '0'
                
                # Chọn bit phổ biến hơn
                binary_message += dwt_bit if dwt_bit == lsb_bit else dwt_bit

                # Thử giải mã sau mỗi 64 bit
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
        height, width = original.shape[:2]
        capacity = (height * width) // 16  # Dung lượng cho hybrid

        return {
            'psnr': psnr,
            'mse': mse,
            'capacity': capacity
        } 