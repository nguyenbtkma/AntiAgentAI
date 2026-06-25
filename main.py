import asyncio
import os
from dotenv import load_dotenv
from agents import Runner, SQLiteSession

# Load env variables từ .env — không hardcode key trong code
load_dotenv()

# Tắt tracing
os.environ["OPENAI_AGENTS_DISABLE_TRACING"] = "1"
os.environ["OPENAI_TRACING_DISABLED"] = "1"

from agents1.agent_def import create_client, create_assessment_agent

# ------------------------------------------------------------------ #
# Entry point
# ------------------------------------------------------------------ #

async def main():
    # Khởi tạo client và agent
    client = create_client()
    agent = create_assessment_agent(client)

    # Session để lưu lịch sử hội thoại (Memory)
    session = SQLiteSession("assessment")

    # Câu hỏi đầu tiên
    user_input = input("Nhập target cần scan (VD: scanme.nmap.org): ").strip()
    if not user_input:
        user_input = "Scan domain scanme.nmap.org"

    print(f"\n[*] Bắt đầu scan: {user_input}\n")

    while True:
        # Chạy agent
        result = await Runner.run(
            agent,
            user_input,
            session=session
        )

        # Hiển thị output
        print("\n" + "="*60)
        print(result.final_output)
        print("="*60)

        # Nhận input tiếp theo từ user
        user_input = input("\nLựa chọn của bạn (hoặc 'exit' để thoát): ").strip()

        if user_input.lower() in ["exit", "quit", "thoát"]:
            print("\n[*] Kết thúc phiên đánh giá.")
            break

if __name__ == "__main__":
    asyncio.run(main())