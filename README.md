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

#### Báo cáo:

I. GIỚI THIỆU

1. Tổng quan
   Tên đồ án: Image Steganography Application
   Công nghệ: Python, PyQt6
   Chức năng: Giấu và trích xuất thông tin trong ảnh số
   Phương pháp: LSB, DWT và Hybrid
2. Mục tiêu
   Xây dựng ứng dụng giấu tin trong ảnh
   So sánh hiệu quả các phương pháp steganography
   Tạo giao diện người dùng thân thiện
   Đánh giá chất lượng ảnh sau khi giấu tin

II. CƠ SỞ LÝ THUYẾT

1. LSB (Least Significant Bit)
   Nguyên lý: Thay đổi bit cuối của pixel
   Ưu điểm:
   Đơn giản, dễ triển khai
   Dung lượng giấu tin lớn
   Nhược điểm: Dễ bị phát hiện
2. DWT (Discrete Wavelet Transform)
   Nguyên lý: Biến đổi sóng con rời rạc
   Ưu điểm:
   Khó phát hiện
   Chất lượng ảnh tốt
   Nhược điểm: Dung lượng giấu tin thấp
3. Hybrid
   Nguyên lý: Kết hợp LSB và DWT
   Ưu điểm:
   Tăng độ an toàn
   Cân bằng dung lượng và chất lượng
   Nhược điểm: Phức tạp trong triển khai

III. THIẾT KẾ HỆ THỐNG
steganography-app/
├── main.py # Entry point
├── src/
│ └── gui/
│ ├── steganography/ # Các thuật toán
│ ├── tabs/ # Giao diện
│ └── widgets/ # Components 2. Các module chính
Steganography Module: Xử lý thuật toán
GUI Module: Giao diện người dùng
Analysis Module: Phân tích và đánh giá 3. Công nghệ sử dụng
PyQt6: GUI Framework
OpenCV: Xử lý ảnh
NumPy: Tính toán ma trận
PyWavelets: Biến đổi DWT
Cryptography: Mã hóa dữ liệu

IV. TRIỂN KHAI

1. Giao diện người dùng
   Hide Message Tab: Giấu tin
   Extract Message Tab: Trích xuất tin
   Analysis Tab: Phân tích kết quả
2. Các chức năng chính
   Giấu tin với 3 phương pháp
   Trích xuất tin nhắn đã giấu
   Phân tích chất lượng ảnh
   Bảo vệ tin nhắn bằng mật khẩu
3. Metrics đánh giá
   PSNR (Peak Signal-to-Noise Ratio)
   MSE (Mean Square Error)
   SSIM (Structural Similarity Index)
   Histogram Difference
   Chi-Square Analysis

V. KẾT QUẢ VÀ ĐÁNH GIÁ

1. Kết quả đạt được
   Triển khai thành công 3 phương pháp
   Giao diện thân thiện, dễ sử dụng
   Hệ thống phân tích chi tiết
   Bảo mật tin nhắn với mã hóa
2. Hạn chế
   Cần tối ưu thêm về performance
   Chưa có unit tests
   Cần bổ sung thêm documentation
3. Hướng phát triển
   Thêm các phương pháp steganography mới
   Tối ưu hóa thuật toán
   Thêm tính năng batch processing
   Phát triển phiên bản web

VI. KẾT LUẬN
Đã xây dựng thành công ứng dụng steganography
So sánh được ưu nhược điểm các phương pháp
Tạo được công cụ hữu ích cho việc giấu tin
Đáp ứng các yêu cầu đề ra
