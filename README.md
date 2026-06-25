AntiAgentAI

AntiAgentAI là một AI Agent hỗ trợ các tác vụ thu thập thông tin và phân tích cơ bản bằng cách kết hợp LLM với công cụ Nmap. Agent có khả năng sử dụng tool để thực hiện quét mạng, đọc tài liệu kiến thức nội bộ và tạo báo cáo dựa trên kết quả thu thập được.

⚠️ Đây là dự án nghiên cứu và demo, chưa phải sản phẩm production-ready.

Tính năng hiện tại
AI Agent sử dụng mô hình ngôn ngữ thông qua OpenRouter API.
Hỗ trợ sử dụng Nmap để thực hiện các tác vụ scan cơ bản.
Hệ thống Knowledge Base phục vụ tra cứu kiến thức về Nmap.
Tạo báo cáo từ kết quả thu thập được.
Kiến trúc Agent đơn giản phục vụ mục đích học tập và nghiên cứu.
Yêu cầu
1. OpenRouter API Key

Dự án sử dụng OpenRouter để truy cập mô hình AI.

Người dùng cần tự tạo API Key tại OpenRouter và thêm vào file .env.

Tạo file .env dựa trên file .env.example:

OPENROUTER_API_KEY=your_api_key_here

2. Nmap

Cần cài đặt Nmap trước khi sử dụng Agent.

Windows

Mặc định tool Nmap hiện đang được cấu hình:

cmd = [r"C:\Program Files (x86)\Nmap\nmap.exe"]

Nếu Nmap được cài đặt ở vị trí khác, vui lòng chỉnh sửa lại đường dẫn trong:

tools/nmap.py
Kali Linux

Nếu sử dụng Kali Linux hoặc các hệ điều hành Linux khác, thay đổi:

cmd = [r"C:\Program Files (x86)\Nmap\nmap.exe"]

thành:

cmd = ["nmap"]

hoặc:

cmd = ["/usr/bin/nmap"]
