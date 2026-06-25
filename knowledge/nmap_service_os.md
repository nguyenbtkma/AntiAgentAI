# Nmap – Service & OS Detection

## Version Detection (-sV)

```bash
# Version scan cơ bản
nmap -sV 192.168.1.1

# Version intensity tối đa (chi tiết nhất, chậm hơn)
nmap -sV --version-intensity 9 192.168.1.1

# Light mode – nhanh hơn, ít chính xác hơn
nmap -sV --version-light 192.168.1.1

# Thử tất cả probes
nmap -sV --version-all 192.168.1.1
```

| Flag | Tương đương | Mô tả |
|------|-------------|-------|
| `--version-intensity 0-9` | — | 0=nhẹ nhất, 9=nặng nhất (default 7) |
| `--version-light` | intensity 2 | Nhanh, ít chính xác |
| `--version-all` | intensity 9 | Thử tất cả probes |

## OS Detection (-O)

```bash
# OS detection cơ bản
nmap -O 192.168.1.1

# OS + version detection (combo chuẩn nhất)
nmap -sV -O 192.168.1.1

# Aggressive guess kể cả khi uncertain
nmap -O --osscan-guess 192.168.1.1

# Chỉ OS scan khi có ít nhất 1 open + 1 closed port
nmap -O --osscan-limit 192.168.1.1
```

> OS detection cần ít nhất **1 open** và **1 closed** port.
> Nếu firewall block hết thì kết quả không chính xác – thêm `--osscan-guess`.

## Aggressive Mode (-A)

```bash
# All-in-one: OS + version + default scripts + traceroute
nmap -A 192.168.1.1

# Aggressive + tất cả ports
nmap -A -p- 192.168.1.1

# Aggressive + timing T4
nmap -A -T4 192.168.1.1
```

`-A` = `-sV -O --script=default --traceroute`

> `-A` rất noisy! Chỉ dùng khi đã có phép và không cần stealth.

## Traceroute

```bash
# Trace đường đi tới target
nmap --traceroute 192.168.1.1

# Traceroute + verbose
nmap --traceroute -v 192.168.1.1
```

## Combo thực chiến

```bash
# Recon nhanh 1 host – cân bằng tốc độ/thông tin
nmap -sV -sC -T4 192.168.1.1

# Recon đầy đủ sau khi biết port open
nmap -sV -O --osscan-guess -p 22,80,443,445 192.168.1.1
```