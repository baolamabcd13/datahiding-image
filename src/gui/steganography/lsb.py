import cv2
import numpy as np

class LSBSteganography:
    def __init__(self):
        self.delimiter = "$$END$$"

    def text_to_binary(self, text):
        """Convert text to binary string"""
        binary = ''.join(format(ord(char), '08b') for char in text)
        return binary + ''.join(format(ord(char), '08b') for char in self.delimiter)

    def binary_to_text(self, binary):
        """Convert binary string back to text"""
        text = ''
        # Split binary string into 8-bit chunks
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            text += chr(int(byte, 2))
            # Check for delimiter
            if text.endswith(self.delimiter):
                return text[:-len(self.delimiter)]
        return text

    def can_encode(self, image, message):
        """Check if the message can fit in the image"""
        max_bytes = (image.shape[0] * image.shape[1] * 3) // 8
        message_size = len(message) + len(self.delimiter)
        return message_size < max_bytes

    def encode(self, image_path, message):
        """Hide message in image using LSB steganography"""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")

        # Check if message can fit in image
        if not self.can_encode(image, message):
            raise ValueError("Message too large for image")

        # Convert message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in message + self.delimiter)
        message_length = len(binary_message)

        # Flatten the image array
        stego_image = image.copy()
        stego_flat = stego_image.flatten()

        # Hide message in LSB
        for i in range(message_length):
            stego_flat[i] = (stego_flat[i] & 254) | int(binary_message[i])

        # Reshape back to image dimensions
        stego_image = stego_flat.reshape(image.shape)
        return stego_image

    def decode(self, stego_image_path):
        """Extract hidden message from stego image"""
        # Read stego image
        stego_image = cv2.imread(stego_image_path)
        if stego_image is None:
            raise ValueError("Could not read stego image")

        # Convert image to binary string
        binary_data = ''
        stego_flat = stego_image.flatten()

        # Extract LSB from each pixel
        for pixel in stego_flat:
            binary_data += str(pixel & 1)
            # Try to find delimiter in extracted text
            if len(binary_data) % 8 == 0:
                text = self.binary_to_text(binary_data)
                if self.delimiter in text:
                    return text

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
        capacity = (original.shape[0] * original.shape[1] * 3) // 8

        return {
            'psnr': psnr,
            'mse': mse,
            'capacity': capacity
        } 