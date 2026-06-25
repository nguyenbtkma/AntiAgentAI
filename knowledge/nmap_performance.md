# Nmap – Performance Tuning

## Parallelism & Rate

```bash
# Tối thiểu 100 probes song song
nmap --min-parallelism 100 192.168.1.0/24

# Tối đa 200 probes song song
nmap --max-parallelism 200 192.168.1.0/24

# Rate tối thiểu 1000 packets/giây
nmap --min-rate 1000 192.168.1.0/24

# Rate tối đa 5000 packets/giây
nmap --max-rate 5000 192.168.1.0/24
```

## Timeout & Retries

```bash
# Custom RTT timeout
nmap --max-rtt-timeout 100ms --min-rtt-timeout 50ms 192.168.1.0/24

# Host timeout 3 phút
nmap --host-timeout 3m 192.168.1.0/24

# Delay giữa các probe
nmap --scan-delay 200ms 192.168.1.0/24
nmap --max-scan-delay 500ms 192.168.1.0/24

# Giảm retries để nhanh hơn (hy sinh accuracy)
nmap --max-retries 1 192.168.1.0/24

# Không retry
nmap --max-retries 0 192.168.1.0/24
```

## Preset cho từng tình huống

```bash
# Scan subnet lớn – cân bằng tốc độ/accuracy
nmap -sS -T4 --min-rate 5000 --max-retries 1 -p- 192.168.1.0/24

# Scan cực nhanh top 1000 ports
nmap -sS -T5 --min-rate 10000 --top-ports 1000 192.168.1.0/24

# Scan chậm để tránh IDS
nmap -sS -T1 --scan-delay 1s --max-retries 2 192.168.1.0/24

# Scan UDP nhanh hơn
nmap -sU --max-retries 1 --host-timeout 5m -p 53,161,500 192.168.1.0/24
```

## Flags tóm tắt

| Flag | Mô tả |
|------|-------|
| `--min-parallelism N` | Tối thiểu N probes song song |
| `--max-parallelism N` | Tối đa N probes song song |
| `--min-rate N` | Gửi tối thiểu N packets/giây |
| `--max-rate N` | Gửi tối đa N packets/giây |
| `--host-timeout` | Bỏ host sau thời gian nhất định |
| `--scan-delay` | Delay giữa các probe |
| `--max-retries N` | Số lần retry tối đa |
| `--max-rtt-timeout` | RTT timeout tối đa |

> Scan subnet lớn: `-T4 --min-rate 5000 --max-retries 1 -p-` là preset tốt nhất để cân bằng tốc độ và độ chính xác.