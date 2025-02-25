Phần 1: Giới thiệu và Tổng quan

# Image Steganography Application

Ứng dụng giấu tin trong ảnh sử dụng các phương pháp LSB, DWT và Hybrid, được xây dựng với Python và PyQt6.

## Tổng quan

Ứng dụng cung cấp 3 phương pháp steganography:

- **LSB (Least Significant Bit)**: Thay đổi bit cuối cùng của mỗi pixel
- **DWT (Discrete Wavelet Transform)**: Sử dụng biến đổi sóng con để nhúng thông tin
- **Hybrid**: Kết hợp cả LSB và DWT để tăng độ an toàn và dung lượng

## Cài đặt và sử dụng

### Cài đặt

1. Clone repository:  
   git clone https://github.com/baolamabcd13/datahiding-image

2. Cài đặt các thư viện cần thiết:
   pip install -r requirements.txt

3. Chạy ứng dụng:
   python main.py

4. Sử dụng:

- Chọn phương pháp giấu tin
- Chọn ảnh gốc và ảnh đích
- Nhập thông tin cần giấu
- Chọn đường dẫn lưu ảnh kết quả

### Chức năng chính của từng module:

#### Steganography Module:

- **LSB**:

  - Xử lý bit-level của ảnh
  - Thay đổi bit ít quan trọng nhất
  - Tối ưu hóa capacity

- **DWT**:

  - Biến đổi wavelet
  - Xử lý frequency domain
  - Bảo toàn chất lượng ảnh

- **Hybrid**:
  - Kết hợp hai phương pháp
  - Tăng cường bảo mật
  - Cân bằng capacity và quality

#### GUI Module:

- **Tabs**:

  - Quản lý luồng người dùng
  - Xử lý input/output
  - Hiển thị kết quả

- **Widgets**:
  - Components tái sử dụng
  - Xử lý tương tác người dùng
  - Hiển thị dữ liệu

#### Analysis Module:

- **Metrics**:
  - Đánh giá chất lượng
  - So sánh hiệu suất
  - Phân tích bảo mật
