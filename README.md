# EasyMath

**EasyMath** là một công cụ học toán trực tuyến được xây dựng bằng Python. Dự án này nhằm giúp học sinh hiểu và áp dụng các khái niệm toán học liên quan đến hoán vị, tổ hợp và chỉnh hợp một cách trực quan và hiệu quả. Dự án cũng tích hợp công nghệ AI thông qua Google Gemini để hỗ trợ giải thích và hướng dẫn các bài toán.

## 1. Giới thiệu

EasyMath cung cấp các tính năng học toán tiên tiến, bao gồm:
- Mô tả bài toán toán học bằng ngôn ngữ dễ hiểu.
- Cung cấp kết quả chính xác của các bài toán về hoán vị, tổ hợp, chỉnh hợp.
- Giao diện đơn giản, trực quan, phù hợp với học sinh và giáo viên.
- Hỗ trợ mô hình ngôn ngữ (LLM) để tạo hướng dẫn và lời giải bài toán.

---

## 2. Mô tả từng thành phần:
1. **`.devcontainer/`**: Chứa các cài đặt cần thiết để phát triển dự án trong môi trường container (Docker hoặc DevContainer).
2. **`.idea/`**: Thư mục tự động tạo bởi IDE (ví dụ: PyCharm).
3. **`image/`**: Lưu trữ các hình ảnh cần thiết để minh họa hoặc hiển thị trên giao diện.
4. **`app.py`**: Tệp Python chính để khởi chạy ứng dụng Streamlit, tạo giao diện người dùng.
5. **`prompt.py`**: Tích hợp mô hình ngôn ngữ Google Gemini và xử lý API.
6. **`requirements.txt`**: Danh sách các thư viện Python cần thiết.
7. **`README.md`**: Tài liệu hướng dẫn và giới thiệu dự án.

---

## 3. Tính năng chính

### 3.1. Công cụ tính toán hoán vị, tổ hợp, chỉnh hợp
- **Hoán vị**: Tính toán các kết quả hoán vị của n phần tử.
- **Tổ hợp**: Giải thích và tính số cách chọn k phần tử từ n phần tử.
- **Chỉnh hợp**: Hỗ trợ tính chỉnh hợp không lặp và có lặp.

### 3.2. Tích hợp AI
- **Google Gemini LLM**: Hỗ trợ giải thích bài toán và hướng dẫn giải bằng mô hình ngôn ngữ lớn (LLM).

### 3.3. Giao diện người dùng đơn giản
- **Streamlit**: Giao diện trực quan, dễ sử dụng, phù hợp với học sinh và giáo viên.

---

## 4. Hướng dẫn sử dụng

### 4.1. Cài đặt môi trường
1. Đảm bảo cài đặt Python 3.10 hoặc cao hơn.
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
3. Chạy lệnh sau để mở giao diện:

    ```bash 
   streamlit run app.py
