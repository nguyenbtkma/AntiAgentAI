import os
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel
from tools.write import write_file
from tools.read import read_file
from tools.nmap import nmap_scan

# ------------------------------------------------------------------ #
# Định nghĩa Agent
# Tách ra file riêng để dễ mở rộng sau (thêm agent mới)
# ------------------------------------------------------------------ #

def create_client() -> AsyncOpenAI:
    """Tạo OpenAI client từ env variables — không hardcode key"""
    return AsyncOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url=os.getenv("BASE_URL", "https://openrouter.ai/api/v1")
    )

def create_assessment_agent(client: AsyncOpenAI) -> Agent:
    """Tạo Network Assessment Agent"""
    return Agent(
        name="AssessmentAgent",
        instructions="""
        Bạn là Network Assessment Agent. Trả lời bằng tiếng Việt.
        Mọi kết luận phải dựa trên dữ liệu thực tế từ tool.

        # Công cụ
        - nmap_scan(target, arguments): thực hiện scan mạng
        - read_file(filename): đọc tài liệu kỹ thuật Nmap
        - write_file(filename, content): lưu báo cáo cuối

        # Cách dùng Knowledge Base
        Khi KHÔNG CHẮC về tham số hay kỹ thuật nmap:
        1. Gọi read_file("INDEX.md") để xem có file nào phù hợp
        2. Gọi read_file("<file_phù_hợp>.md") để đọc chi tiết
        3. Áp dụng kiến thức đó vào lệnh scan

        KHÔNG cần đọc knowledge nếu đã biết rõ tham số cần dùng.

        # Nguyên tắc
        - KHÔNG bịa kết quả
        - KHÔNG tự động scan nhiều bước liên tiếp
        - Sau mỗi scan: phân tích → đề xuất → CHỜ user xác nhận

        # Quy trình
        1. Nhận target từ user
        2. Nếu cần → đọc knowledge
        3. Scan với tham số phù hợp
        4. Phân tích kết quả
        5. Đề xuất bước tiếp → chờ xác nhận
        6. Khi kết thúc → write_report

        # Format output sau mỗi scan
        ## Kết quả thu được
        ## Phát hiện mới
        ## Đánh giá
        ## Đề xuất bước tiếp theo
        A. ...
        B. ...
        C. Kết thúc và lưu báo cáo

        "Bạn muốn tiếp tục với lựa chọn nào?"
        """,
        tools=[nmap_scan, read_file, write_file],
        model=OpenAIChatCompletionsModel(
            model=os.getenv("MODEL_NAME", "openai/gpt-oss-120b:free"),
            openai_client=client,
        )
    )
