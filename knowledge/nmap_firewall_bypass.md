# Nmap – Firewall Bypass

## Source Port Tricks

Nhiều firewall cho phép traffic từ các port "tin cậy" (53, 80, 443).

```bash
# Dùng port 53 (DNS) làm source
nmap --source-port 53 192.168.1.1

# Dùng port 80 làm source
nmap --source-port 80 192.168.1.1

# Dùng port 443 làm source
nmap --source-port 443 192.168.1.1

# Kết hợp với SYN scan
nmap -sS --source-port 53 192.168.1.1
```

## Packet Manipulation

```bash
# Thêm random data padding – bypass signature-based IDS
nmap --data-length 200 192.168.1.1

# Custom MTU để bypass deep packet inspection
nmap --mtu 24 192.168.1.1

# Gửi packet checksum sai – test phản ứng IDS
nmap --badsum 192.168.1.1

# Thêm IP options
nmap --ip-options "L 192.168.1.1 192.168.1.2" 192.168.1.1
```

## Scan qua Proxy & Tor

```bash
# Qua proxychains
proxychains nmap -sT -Pn 192.168.1.1

# Qua SOCKS5 trực tiếp (Tor: port 9050)
nmap -sT -Pn --proxy socks5://127.0.0.1:9050 192.168.1.1

# Qua HTTP proxy
nmap -sT -Pn --proxy http://127.0.0.1:8080 192.168.1.1
```

> Khi dùng proxy **bắt buộc** dùng `-sT`. Raw packet scan (`-sS`, `-sU`) không hoạt động qua proxy.

## ACK Scan – Map Firewall Rules

```bash
# ACK scan để xác định port nào FW cho qua
nmap -sA 192.168.1.1

# Kết hợp với Window scan
nmap -sW 192.168.1.1
```

| Response | Ý nghĩa |
|----------|---------|
| RST | Port **unfiltered** – firewall cho qua |
| Không response / ICMP unreachable | Port **filtered** – firewall block |

## Bypass Host-based Firewall (Windows)

```bash
# Scan qua port 80 (thường được FW rule cho phép)
nmap -sS --source-port 80 -p 445 192.168.1.1

# Fragment nhỏ để bypass stateful inspection
nmap -f --mtu 8 192.168.1.1

# Kết hợp nhiều kỹ thuật
nmap -sS -f --source-port 53 --data-length 100 -T2 192.168.1.1
```

## Checklist khi bị block

1. Thử `-Pn` nếu host không ping được
2. Thử `--source-port 53` hoặc `--source-port 80`
3. Thử `-f` hoặc `--mtu 24` để fragment
4. Thử `-sA` để xem port nào unfiltered
5. Thử scan qua proxy nếu cần ẩn danh
6. Thử `-T1` hoặc `-T2` nếu nghi bị rate-limit