import cv2
import numpy as np
import pywt
from cryptography.fernet import Fernet
import base64
from hashlib import sha256

class DWTSteganography:
    def __init__(self):
        self.delimiter = "$$END$$"
        
    def _get_key_from_password(self, password):
        """Generate Fernet key from password"""
        if not password:
            return None
        key = sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(key[:32])

    def _encrypt_message(self, message, password):
        """Encrypt message using Fernet encryption"""
        if not password:
            return message.encode()
        
        key = self._get_key_from_password(password)
        f = Fernet(key)
        return f.encrypt(message.encode())

    def _decrypt_message(self, encrypted_message, password):
        """Decrypt message using Fernet encryption"""
        if not password:
            return encrypted_message.decode()
        
        key = self._get_key_from_password(password)
        f = Fernet(key)
        return f.decrypt(encrypted_message).decode()

    def encode(self, image_path, message, password=None):
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")

        # Convert to YCbCr color space
        ycbcr = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
        y, cr, cb = cv2.split(ycbcr)

        # Apply DWT to Y channel
        coeffs = pywt.dwt2(y, 'haar')
        cA, (cH, cV, cD) = coeffs

        # Encrypt message
        encrypted = self._encrypt_message(message + self.delimiter, password)
        binary_message = ''.join(format(byte, '08b') for byte in encrypted)
        message_length = len(binary_message)

        # Check capacity
        max_capacity = (cA.shape[0] * cA.shape[1]) // 2
        if message_length > max_capacity:
            raise ValueError(f"Message too large. Maximum capacity: {max_capacity} bits")

        # Embed message in cA coefficients
        msg_idx = 0
        modified_cA = cA.copy()
        for i in range(cA.shape[0]):
            for j in range(cA.shape[1]):
                if msg_idx < message_length:
                    # Modify least significant bit
                    modified_cA[i, j] = np.floor(cA[i, j])
                    if binary_message[msg_idx] == '1':
                        modified_cA[i, j] += 0.5
                    msg_idx += 1

        # Inverse DWT
        modified_coeffs = (modified_cA, (cH, cV, cD))
        modified_y = pywt.idwt2(modified_coeffs, 'haar')

        # Ensure proper size and type
        modified_y = np.clip(modified_y, 0, 255)
        modified_y = modified_y.astype(np.uint8)

        # Reconstruct image
        modified_ycbcr = cv2.merge([modified_y, cr, cb])
        stego_image = cv2.cvtColor(modified_ycbcr, cv2.COLOR_YCR_CB2BGR)

        return stego_image

    def decode(self, stego_image_path, password=None):
        # Read stego image
        stego_image = cv2.imread(stego_image_path)
        if stego_image is None:
            raise ValueError("Could not read stego image")

        # Convert to YCbCr
        ycbcr = cv2.cvtColor(stego_image, cv2.COLOR_BGR2YCR_CB)
        y, _, _ = cv2.split(ycbcr)

        # Apply DWT
        coeffs = pywt.dwt2(y, 'haar')
        cA, _ = coeffs

        # Extract binary message
        binary_message = ''
        for i in range(cA.shape[0]):
            for j in range(cA.shape[1]):
                # Extract bit from decimal part
                decimal_part = cA[i, j] - np.floor(cA[i, j])
                bit = '1' if decimal_part >= 0.4 else '0'
                binary_message += bit

        # Convert binary to bytes
        bytes_data = bytearray()
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if len(byte) == 8:
                bytes_data.append(int(byte, 2))

        try:
            # Decrypt message
            decrypted = self._decrypt_message(bytes(bytes_data), password)
            
            # Remove delimiter
            if self.delimiter in decrypted:
                return decrypted[:decrypted.index(self.delimiter)]
        except:
            raise ValueError("Invalid password or corrupted message")

        return None

    def calculate_metrics(self, original_image_path, stego_image_path):
        """Calculate PSNR and MSE between original and stego images"""
        original = cv2.imread(original_image_path)
        stego = cv2.imread(stego_image_path)

        if original is None or stego is None:
            raise ValueError("Could not read images")

        if original.shape != stego.shape:
            raise ValueError("Images have different dimensions")

        # Calculate MSE
        mse = np.mean((original - stego) ** 2)
        
        # Calculate PSNR
        if mse == 0:
            psnr = float('inf')
        else:
            psnr = 20 * np.log10(255.0 / np.sqrt(mse))

        # Calculate embedding capacity (in bytes)
        y = cv2.cvtColor(original, cv2.COLOR_BGR2YCR_CB)[0]
        coeffs = pywt.dwt2(y, 'haar')
        cA, _ = coeffs
        capacity = (cA.shape[0] * cA.shape[1]) // 8

        return {
            'psnr': psnr,
            'mse': mse,
            'capacity': capacity
        } 