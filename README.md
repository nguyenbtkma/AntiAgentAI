# AntiAgentAI

AntiAgentAI là một AI Agent hỗ trợ thu thập thông tin và phân tích cơ bản bằng cách kết hợp LLM với công cụ Nmap. Agent có khả năng sử dụng tool để thực hiện quét mạng, truy xuất tài liệu kiến thức nội bộ và tạo báo cáo dựa trên kết quả thu thập được.

> ⚠️ Đây là dự án nghiên cứu và demo, chưa phải sản phẩm production-ready.

---

## Tính năng hiện tại

- Sử dụng mô hình ngôn ngữ thông qua OpenRouter API.
- Tích hợp Nmap để thực hiện các tác vụ scan cơ bản.
- Hệ thống Knowledge Base phục vụ tra cứu kiến thức về Nmap.
- Hỗ trợ tạo báo cáo từ kết quả thu thập được.
- Kiến trúc Agent đơn giản phục vụ mục đích học tập và nghiên cứu.

---

## Kiến trúc dự án

```
AntiAgentAI/
│
├── agents1/        # Agent definitions
├── knowledge/      # Knowledge Base
├── tools/          # Tool implementations
├── reports/        # Generated reports
├── main.py         # Entry point
├── .env.example    # Environment template
├── requirements.txt
└── README.md
```

---

## Yêu cầu

### 1. OpenRouter API Key

Dự án sử dụng OpenRouter để truy cập các mô hình AI.

Người dùng cần tự tạo API Key và thêm vào file `.env`.

Tạo file `.env` từ `.env.example`:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Ví dụ trên Linux:

```bash
cp .env.example .env
nano .env
```

---

### 2. Nmap

Cần cài đặt Nmap trước khi sử dụng Agent.

#### Windows

Hiện tại tool Nmap được cấu hình mặc định:

```python
cmd = [r"C:\Program Files (x86)\Nmap\nmap.exe"]
```

Nếu Nmap được cài đặt ở vị trí khác, vui lòng chỉnh sửa lại đường dẫn trong:

```text
tools/nmap.py
```

#### Kali Linux / Linux

Nếu sử dụng Kali Linux hoặc các bản phân phối Linux khác, thay đổi:

```python
cmd = [r"C:\Program Files (x86)\Nmap\nmap.exe"]
```

thành:

```python
cmd = ["nmap"]
```

hoặc:

```python
cmd = ["/usr/bin/nmap"]
```

---

## Cài đặt

Clone repository:

```bash
git clone https://github.com/nguyenbtkma/AntiAgentAI.git
cd AntiAgentAI
```

Cài đặt thư viện:

```bash
pip install -r requirements.txt
```

Tạo file môi trường:

```bash
cp .env.example .env
```

Thêm OpenRouter API Key vào `.env`.

---

## Chạy chương trình

```bash
python main.py
```

---
