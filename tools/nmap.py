import subprocess, os
from agents import function_tool

# ------------------------------------------------------------------ #
# Định nghĩa tools cho agent
# Mỗi tool là 1 hành động cụ thể agent có thể yêu cầu thực thi
# ------------------------------------------------------------------ #

@function_tool
def nmap_scan(target: str, arguments: str = "") -> str:
    """
    Chạy nmap scan trên target.
    
    Args:
        target: IP hoặc domain cần scan
        arguments: Các tham số nmap (VD: "-sV -p 80,443")
    
    Returns:
        Raw output từ nmap
    """
    cmd = [r"C:\Program Files (x86)\Nmap\nmap.exe"]

    if arguments:
        cmd.extend(arguments.split())

    cmd.append(target)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3000
        )
        return result.stdout if result.stdout else result.stderr
    except subprocess.TimeoutExpired:
        return "Lỗi: Scan timeout sau 3000 giây"
    except FileNotFoundError:
        return "Lỗi: Không tìm thấy nmap. Kiểm tra đường dẫn cài đặt."
    except Exception as e:
        return f"Lỗi không xác định: {str(e)}"
    
