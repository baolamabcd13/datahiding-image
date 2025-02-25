import cv2
import numpy as np
import pywt
from cryptography.fernet import Fernet
import base64
from hashlib import sha256

class HybridSteganography:
    def __init__(self):
        self.delimiter = "$$END$$"

    def _get_key_from_password(self, password):
        if not password:
            return None
        key = sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(key[:32])

    def _encrypt_message(self, message, password):
        if not password:
            return message.encode()
        
        key = self._get_key_from_password(password)
        f = Fernet(key)
        return f.encrypt(message.encode())

    def _decrypt_message(self, encrypted_message, password):
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

        # Split message into two parts
        message_length = len(message)
        dwt_message = message[:message_length//2]
        lsb_message = message[message_length//2:]

        # Encrypt both parts
        encrypted_dwt = self._encrypt_message(dwt_message + "$$DWT$$", password)
        encrypted_lsb = self._encrypt_message(lsb_message + "$$LSB$$", password)

        # DWT embedding
        ycbcr = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
        y, cr, cb = cv2.split(ycbcr)
        
        coeffs = pywt.dwt2(y, 'haar')
        cA, (cH, cV, cD) = coeffs

        binary_dwt = ''.join(format(byte, '08b') for byte in encrypted_dwt)
        dwt_length = len(binary_dwt)

        # Check DWT capacity
        max_dwt_capacity = (cA.shape[0] * cA.shape[1]) // 2
        if dwt_length > max_dwt_capacity:
            raise ValueError(f"DWT message too large. Maximum capacity: {max_dwt_capacity} bits")

        # Embed in DWT coefficients
        msg_idx = 0
        modified_cA = cA.copy()
        for i in range(cA.shape[0]):
            for j in range(cA.shape[1]):
                if msg_idx < dwt_length:
                    modified_cA[i, j] = np.floor(cA[i, j])
                    if binary_dwt[msg_idx] == '1':
                        modified_cA[i, j] += 0.5
                    msg_idx += 1

        # Inverse DWT
        modified_coeffs = (modified_cA, (cH, cV, cD))
        modified_y = pywt.idwt2(modified_coeffs, 'haar')
        modified_y = np.clip(modified_y, 0, 255).astype(np.uint8)

        # LSB embedding
        binary_lsb = ''.join(format(byte, '08b') for byte in encrypted_lsb)
        lsb_length = len(binary_lsb)

        # Check LSB capacity
        max_lsb_capacity = (cr.shape[0] * cr.shape[1]) // 2
        if lsb_length > max_lsb_capacity:
            raise ValueError(f"LSB message too large. Maximum capacity: {max_lsb_capacity} bits")

        # Embed in Cr channel using LSB
        msg_idx = 0
        modified_cr = cr.copy()
        for i in range(cr.shape[0]):
            for j in range(cr.shape[1]):
                if msg_idx < lsb_length:
                    modified_cr[i, j] = (modified_cr[i, j] & 254) | int(binary_lsb[msg_idx])
                    msg_idx += 1

        # Reconstruct image
        modified_ycbcr = cv2.merge([modified_y, modified_cr, cb])
        stego_image = cv2.cvtColor(modified_ycbcr, cv2.COLOR_YCR_CB2BGR)

        return stego_image

    def decode(self, stego_image_path, password=None):
        # Read stego image
        stego_image = cv2.imread(stego_image_path)
        if stego_image is None:
            raise ValueError("Could not read stego image")

        # Convert to YCbCr
        ycbcr = cv2.cvtColor(stego_image, cv2.COLOR_BGR2YCR_CB)
        y, cr, cb = cv2.split(ycbcr)

        # Extract DWT message
        coeffs = pywt.dwt2(y, 'haar')
        cA, _ = coeffs

        binary_dwt = ''
        for i in range(cA.shape[0]):
            for j in range(cA.shape[1]):
                decimal_part = cA[i, j] - np.floor(cA[i, j])
                bit = '1' if decimal_part >= 0.4 else '0'
                binary_dwt += bit

        # Extract LSB message
        binary_lsb = ''
        for i in range(cr.shape[0]):
            for j in range(cr.shape[1]):
                binary_lsb += str(cr[i, j] & 1)

        # Convert binary to bytes
        dwt_bytes = bytearray()
        for i in range(0, len(binary_dwt), 8):
            byte = binary_dwt[i:i+8]
            if len(byte) == 8:
                dwt_bytes.append(int(byte, 2))

        lsb_bytes = bytearray()
        for i in range(0, len(binary_lsb), 8):
            byte = binary_lsb[i:i+8]
            if len(byte) == 8:
                lsb_bytes.append(int(byte, 2))

        try:
            # Decrypt both parts
            dwt_decrypted = self._decrypt_message(bytes(dwt_bytes), password)
            lsb_decrypted = self._decrypt_message(bytes(lsb_bytes), password)

            # Extract messages and remove delimiters
            if "$$DWT$$" in dwt_decrypted and "$$LSB$$" in lsb_decrypted:
                dwt_message = dwt_decrypted[:dwt_decrypted.index("$$DWT$$")]
                lsb_message = lsb_decrypted[:lsb_decrypted.index("$$LSB$$")]
                return dwt_message + lsb_message
        except:
            raise ValueError("Invalid password or corrupted message")

        return None

    def calculate_metrics(self, original_image_path, stego_image_path):
        """Calculate PSNR, MSE and capacity"""
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

        # Calculate total capacity (DWT + LSB)
        y = cv2.cvtColor(original, cv2.COLOR_BGR2YCR_CB)[0]
        coeffs = pywt.dwt2(y, 'haar')
        cA, _ = coeffs
        dwt_capacity = (cA.shape[0] * cA.shape[1]) // 16  # Using half for DWT
        lsb_capacity = (original.shape[0] * original.shape[1]) // 16  # Using half for LSB
        total_capacity = dwt_capacity + lsb_capacity

        return {
            'psnr': psnr,
            'mse': mse,
            'capacity': total_capacity
        } 