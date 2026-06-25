import os
import re
from agents import function_tool

# =========================================================
# FIX 1: ZERO TRUST + SANDBOX CONFIG
# =========================================================

ALLOWED_DIR = os.path.abspath("./reports")

ALLOWED_EXTENSIONS = {".txt", ".md", ".log"}

DANGEROUS_PATTERNS = [
    r"io\s*\.\s*popen",
    r"os\s*\.\s*system",
    r"os\s*\.\s*execute",
    r"subprocess",
    r"powershell",
    r"cmd",
    r"whoami",
    r"ipconfig",
]
# =========================================================
# FIX 4: PATH SANDBOX
# =========================================================
def is_safe_path(path: str) -> bool:
    abs_path = os.path.abspath(path)
    return abs_path.startswith(ALLOWED_DIR)

# =========================================================
# FIX 5: WRITE FILE HARDENED (LLM05 + LLM06 FIX)
# =========================================================
@function_tool
def write_file(path: str, content: str) -> str:
    """
    FIXED:
    - Chỉ ghi trong ./reports
    - Chỉ cho file report (txt/md/log)
    - Block nội dung mang tính exploit / system leak
    """

    try:
        # 1. sandbox directory
        if not is_safe_path(path):
            return "BLOCKED: Outside reports directory"

        # 2. whitelist extension
        ext = os.path.splitext(path)[1]
        if ext not in ALLOWED_EXTENSIONS:
            return "BLOCKED: Invalid file type"

        # 3. ZERO TRUST: reject system / exploit content
        lower = content.lower()
        if any(re.search(p, lower) for p in DANGEROUS_PATTERNS):
            return "BLOCKED: Dangerous payload detected"

        # 4. BLOCK raw system leakage (Test 3 fix)
        leak_signals = ["ip configuration", "adapter", "ipv4", "default gateway"]
        if sum(1 for s in leak_signals if s in lower) >= 2:
            return "BLOCKED: System data not allowed in report"

        # 5. write file safely
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"OK: written to {path}"

    except Exception as e:
        return f"ERROR: {str(e)}"