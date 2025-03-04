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

# 1. Clone repository:

```bash
git clone https://github.com/baolamabcd13/datahiding-image
cd datahiding-image
```

# 2. Cài đặt python3.10:

```bash
sudo apt install python3.10
```

# 3. Cài đặt môi trường ảo cho window:

```bash
python3.10 -m venv venv
venv\Scripts\activate
```

# 4. Cài đặt các thư viện cần thiết:

```bash
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
   a. Nguyên lý hoạt động:

   - Mỗi pixel trong ảnh được biểu diễn bởi các giá trị RGB (8 bit/kênh màu)
   - Thay đổi bit cuối cùng (LSB) của mỗi kênh màu để giấu thông tin
   - Mỗi pixel có thể giấu 3 bit thông tin (1 bit/kênh màu)
   - Thông tin cần giấu được chuyển thành dãy bit nhị phân trước khi nhúng
     b. Chức năng:
   - Mã hóa tin nhắn thành dãy bit
   - Quét từng pixel và thay đổi LSB
   - Lưu trữ metadata (độ dài tin nhắn, checksum)
   - Trích xuất tin nhắn bằng cách đọc LSB

2. DWT (Discrete Wavelet Transform)
   a. Nguyên lý hoạt động:

   - Phân tách ảnh thành 4 band tần số (LL, LH, HL, HH)
   - LL: chi tiết thấp tần (approximation)
   - LH, HL: chi tiết theo chiều dọc và ngang
   - HH: chi tiết cao tần
   - Nhúng thông tin vào các hệ số wavelet của band tần số phù hợp
     b. Chức năng:
   - Biến đổi DWT 2D trên ảnh
   - Chọn band tần số và hệ số để nhúng
   - Điều chỉnh cường độ nhúng (alpha)
   - Biến đổi ngược IDWT để tạo ảnh stego

3. Hybrid
   a. Nguyên lý hoạt động:
   - Kết hợp ưu điểm của cả LSB và DWT
   - Phân chia thông tin cần giấu thành 2 phần
   - Phần 1: Giấu bằng LSB trong vùng ít quan trọng
   - Phần 2: Giấu bằng DWT trong các band tần số
   - Sử dụng mã hóa để tăng bảo mật
     b. Chức năng:
   - Phân tích ảnh để xác định vùng thích hợp
   - Điều phối việc giấu tin giữa LSB và DWT
   - Quản lý khóa và mã hóa
   - Tối ưu hóa tỷ lệ phân chia dữ liệu

III. THIẾT KẾ HỆ THỐNG

1. Kiến trúc hệ thống
   a. Steganography Module:

   - LSBEncoder/Decoder: Xử lý giấu/trích xuất LSB
   - DWTEncoder/Decoder: Xử lý biến đổi wavelet
   - HybridEncoder/Decoder: Điều phối hai phương pháp
   - CryptoManager: Quản lý mã hóa và khóa

   b. GUI Module:

   - MainWindow: Cửa sổ chính của ứng dụng
   - HideTab: Giao diện giấu tin
   - ExtractTab: Giao diện trích xuất
   - AnalysisTab: Giao diện phân tích
   - CustomWidgets: Các component tùy chỉnh

   c. Analysis Module:

   - QualityAnalyzer: Tính toán các metrics
   - HistogramAnalyzer: Phân tích histogram
   - SecurityTester: Kiểm tra độ an toàn
   - ReportGenerator: Tạo báo cáo kết quả

2. Luồng xử lý
   a. Quá trình giấu tin:

   - Tiền xử lý ảnh và thông điệp
   - Kiểm tra dung lượng có thể giấu
   - Mã hóa thông điệp (nếu có)
   - Thực hiện giấu tin theo phương pháp đã chọn
   - Lưu metadata và checksum
   - Tạo ảnh stego

   b. Quá trình trích xuất:

   - Đọc metadata từ ảnh stego
   - Xác thực checksum
   - Trích xuất dữ liệu theo phương pháp tương ứng
   - Giải mã thông điệp (nếu có)
   - Kiểm tra tính toàn vẹn

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
```
