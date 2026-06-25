# Nmap – Port Scan Techniques

## TCP SYN Scan (mặc định, khuyên dùng)

```bash
# SYN scan cơ bản – cần root/sudo
nmap -sS 192.168.1.1

# SYN + version + OS detection
nmap -sS -sV -O 192.168.1.1

# SYN scan tất cả 65535 ports
nmap -sS -p- 192.168.1.1
```

Cách hoạt động:
```
Attacker → SYN → Target
Attacker ← SYN/ACK ← Target  (port open)
Attacker → RST → Target       (không hoàn thành handshake → ít log)
```

## TCP Connect Scan

```bash
# Connect scan – không cần root
nmap -sT 192.168.1.1

# Dùng khi không có root hoặc qua proxy
nmap -sT -Pn 192.168.1.1
```

> `-sT` hoàn thành 3-way handshake → bị log nhiều hơn `-sS`.

## UDP Scan

```bash
# UDP scan các port quan trọng
nmap -sU -p 53,67,68,69,123,161,162,500,4500 192.168.1.1

# Kết hợp TCP SYN + UDP trong 1 lệnh
nmap -sS -sU -p T:80,443,8080,U:53,161 192.168.1.1

# Tăng tốc UDP scan
nmap -sU --max-retries 1 --host-timeout 5m 192.168.1.1
```

> UDP scan rất chậm. Chỉ scan port cần thiết: `53, 67-68, 69, 123, 161, 500, 4500, 5060`.

## Stealth Variants (Null / FIN / Xmas)

```bash
# TCP Null – không set flag nào
nmap -sN 192.168.1.1

# TCP FIN
nmap -sF 192.168.1.1

# Xmas – FIN + PSH + URG
nmap -sX 192.168.1.1

# Maimon – FIN/ACK
nmap -sM 192.168.1.1

# ACK – phát hiện firewall rules
nmap -sA 192.168.1.1

# Window Scan
nmap -sW 192.168.1.1
```

> Null/FIN/Xmas KHÔNG hoạt động trên Windows (Windows luôn trả RST).
> Port open/filtered → không response. Port closed → RST.

## Port Range & Selection

```bash
# Tất cả 65535 ports
nmap -p- 192.168.1.1

# Port cụ thể
nmap -p 22,80,443,8080,3306,3389 192.168.1.1

# Port range
nmap -p 1-1024 192.168.1.1

# Top 100 port phổ biến
nmap --top-ports 100 192.168.1.1

# Top 1000 (default của nmap)
nmap --top-ports 1000 192.168.1.1

# Fast mode – 100 port
nmap -F 192.168.1.1

# TCP và UDP cùng lúc
nmap -p T:80,443,U:53,161 192.168.1.1
```

## Bảng so sánh Scan Types

| Loại | Flag | Cần root | Noisy | Bypass FW | Ghi chú |
|------|------|----------|-------|-----------|---------|
| TCP SYN | `-sS` | ✓ | Thấp | Trung bình | Mặc định khi có root |
| TCP Connect | `-sT` | ✗ | Cao | Thấp | Mặc định khi không root |
| UDP | `-sU` | ✓ | Thấp | Trung bình | Rất chậm |
| TCP Null | `-sN` | ✓ | Rất thấp | Cao | Không dùng được trên Windows |
| TCP FIN | `-sF` | ✓ | Rất thấp | Cao | Không dùng được trên Windows |
| Xmas | `-sX` | ✓ | Rất thấp | Cao | Không dùng được trên Windows |
| ACK | `-sA` | ✓ | Thấp | N/A | Dùng để map firewall rules |
| Idle/Zombie | `-sI` | ✓ | Không | Cao | Cần zombie host thích hợp |