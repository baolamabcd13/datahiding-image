import numpy as np
import cv2
import pywt
from PIL import Image
import matplotlib.pyplot as plt

def test_environment():
    """Test if all required libraries are properly installed"""
    try:
        # Test NumPy
        arr = np.array([1, 2, 3])
        print("NumPy is working")

        # Test OpenCV
        img = cv2.imread("test.jpg") if cv2.imread("test.jpg") is not None else np.zeros((100, 100))
        print("OpenCV is working")

        # Test PyWavelets
        coeffs = pywt.dwt2(np.zeros((100, 100)), 'haar')
        print("PyWavelets is working")

        # Test Pillow
        img = Image.fromarray(np.zeros((100, 100), dtype=np.uint8))
        print("Pillow is working")

        # Test Matplotlib
        plt.figure()
        plt.close()
        print("Matplotlib is working")

        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_environment() 