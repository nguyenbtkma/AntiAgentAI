# Nmap – Host Discovery

## Cú pháp target

| Cú pháp | Ví dụ | Mô tả |
|---------|-------|-------|
| IP đơn | `nmap 192.168.1.1` | Scan 1 host |
| CIDR | `nmap 192.168.1.0/24` | Scan toàn subnet |
| Range | `nmap 192.168.1.1-50` | Scan range IP |
| Hostname | `nmap target.com` | Scan theo domain |
| Từ file | `nmap -iL targets.txt` | Đọc target từ file |
| Exclude IP | `nmap 192.168.1.0/24 --exclude 192.168.1.1` | Loại trừ IP |
| Exclude file | `nmap 192.168.1.0/24 --excludefile excl.txt` | Loại trừ từ file |

## Ping Scan – tìm host sống

```bash
# Ping sweep toàn subnet – không scan port
nmap -sn 192.168.1.0/24

# Tắt DNS resolution để nhanh hơn
nmap -sn -n 10.0.0.0/24

# ARP ping trên LAN (chính xác nhất, cần root)
nmap -PR -sn 192.168.1.0/24

# ICMP echo request
nmap -PE -sn 192.168.1.0/24

# ICMP timestamp
nmap -PP -sn 192.168.1.0/24

# ICMP netmask request
nmap -PM -sn 192.168.1.0/24
```

## TCP/UDP Ping

```bash
# TCP SYN ping port 80
nmap -PS80 -sn 192.168.1.0/24

# TCP SYN ping nhiều port (khi ICMP bị block)
nmap -PS22,80,443,3389 -sn 192.168.1.0/24

# TCP ACK ping
nmap -PA80 -sn 192.168.1.0/24

# UDP ping port 53
nmap -PU53 -sn 192.168.1.0/24
```

## Bỏ qua host discovery

```bash
# Xem host như online dù không ping được (bypass FW block ICMP)
nmap -Pn 192.168.1.1

# Không DNS lookup
nmap -n 192.168.1.0/24

# Chỉ list host, không scan
nmap -sL 192.168.1.0/24
```

## Flags tóm tắt

| Flag | Mô tả |
|------|-------|
| `-sn` | No port scan – chỉ host discovery |
| `-Pn` | Bỏ qua host discovery, scan thẳng port |
| `-n` | Tắt DNS reverse lookup |
| `-PR` | ARP ping (LAN – chính xác nhất) |
| `-PE` | ICMP echo request |
| `-PS[ports]` | TCP SYN ping |
| `-PA[ports]` | TCP ACK ping |
| `-PU[ports]` | UDP ping |

> Trên LAN dùng `-PR`. Ngoài internet dùng `-PE` hoặc `-PS80,443`.
> Nếu ICMP bị block hoàn toàn, dùng `-Pn` để bỏ qua discovery.