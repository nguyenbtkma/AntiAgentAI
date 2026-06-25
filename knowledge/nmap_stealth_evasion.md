# Nmap – Stealth & Evasion

## Timing Templates

| Template | Flag | Delay/Probe | Use Case |
|----------|------|-------------|----------|
| Paranoid | `-T0` | 5 phút | IDS evasion tối đa |
| Sneaky | `-T1` | 15 giây | Tránh hầu hết IDS |
| Polite | `-T2` | 0.4 giây | Giảm tải mạng |
| Normal | `-T3` | Mặc định | Scan thông thường |
| Aggressive | `-T4` | Nhanh hơn 4× | Mạng nhanh, tin cậy |
| Insane | `-T5` | Nhanh nhất | Lab/CTF – có thể miss |

```bash
# Stealth pentest thực chiến
nmap -T2 --scan-delay 500ms 192.168.1.1

# Lab/CTF
nmap -T4 192.168.1.1

# Paranoid – bypass time-based IDS
nmap -T0 --max-retries 1 192.168.1.1
```

> Pentest thực chiến: T2 hoặc T3. CTF/lab: T4. IDS evasion nghiêm túc: T1 + `--scan-delay`.

## Packet Fragmentation

```bash
# Fragment thành 8-byte chunks (bypass stateless FW)
nmap -f 192.168.1.1

# Fragment mạnh hơn – 16-byte chunks
nmap -ff 192.168.1.1

# Custom MTU (phải là bội của 8)
nmap --mtu 24 192.168.1.1

# Kết hợp fragmentation + SYN scan
nmap -f -sS 192.168.1.1
```

## Decoy Scan

```bash
# Decoy ngẫu nhiên (10 IP giả)
nmap -D RND:10 192.168.1.1

# Decoy cụ thể – ME là IP thật của mình
nmap -D 10.0.0.1,10.0.0.2,10.0.0.3,ME 192.168.1.1

# Decoy + SYN scan
nmap -D RND:5 -sS 192.168.1.1
```

> Decoy tạo traffic từ nhiều IP giả → IDS/analyst khó xác định attacker thật.

## Source IP Spoofing

```bash
# Spoof source IP
nmap -S 10.0.0.100 -e eth0 192.168.1.1

# Spoof + chỉ định interface
nmap -S 10.0.0.100 -e eth0 -n 192.168.1.1
```

> `-S` sẽ không nhận được response. Dùng `-D` thực tế hơn cho pentest.

## Idle/Zombie Scan – ẩn danh hoàn toàn

```bash
# Bước 1: Tìm zombie (cần IPID tăng tuần tự)
nmap -O -v 192.168.1.5
nmap --script ipidseq 192.168.1.5

# Bước 2: Thực hiện idle scan qua zombie
nmap -sI 192.168.1.5 192.168.1.1

# Bước 3: Chỉ định zombie port nếu cần
nmap -sI 192.168.1.5:80 192.168.1.1
```

Cách hoạt động:
```
1. Attacker kiểm tra IPID của Zombie
2. Attacker gửi SYN giả IP Zombie → Target
3. Target → SYN/ACK → Zombie (nếu port open)
4. Zombie → RST → Target (IPID tăng +1)
5. Attacker so sánh IPID trước/sau → suy ra port state
```

> Zombie cần IPID predictable (tăng đều). Hay gặp ở: Windows XP, máy in, một số embedded device.