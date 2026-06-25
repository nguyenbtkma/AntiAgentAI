from agents import function_tool
@function_tool
def read_file(path: str) -> str:
    """Đọc nội dung file"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Lỗi: {str(e)}"