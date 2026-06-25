# Nmap RAG – Pentest Reference

> **Tổng hợp đầy đủ các kỹ thuật Nmap cho Penetration Testing**  
> Tác giả: Tổng hợp từ thực chiến & tài liệu chính thức  
> Version: 1.0

---

## Mục Lục

1. [Cú Pháp Cơ Bản](#1-cú-pháp-cơ-bản)
2. [Host Discovery](#2-host-discovery)
3. [Port Scan Techniques](#3-port-scan-techniques)
4. [Service & OS Detection](#4-service--os-detection)
5. [NSE Scripts](#5-nse-scripts)
6. [Stealth & Evasion](#6-stealth--evasion)
7. [Firewall Bypass](#7-firewall-bypass)
8. [Output & Reporting](#8-output--reporting)
9. [Performance Tuning](#9-performance-tuning)
10. [Workflow Thực Chiến](#10-workflow-thực-chiến)
11. [Cheatsheet Quick Reference](#11-cheatsheet-quick-reference)

---

## 1. Cú Pháp Cơ Bản

```
nmap [Scan Type] [Options] {target}
```

### Target Specification

| Cú pháp | Ví dụ | Mô tả |
|---------|-------|-------|
| IP đơn | `nmap 192.168.1.1` | Scan 1 host |
| CIDR | `nmap 192.168.1.0/24` | Scan toàn subnet |
| Range | `nmap 192.168.1.1-50` | Scan range IP |
| Hostname | `nmap target.com` | Scan theo domain |
| Từ file | `nmap -iL targets.txt` | Đọc target từ file |
| Exclude IP | `nmap 192.168.1.0/24 --exclude 192.168.1.1` | Loại trừ IP |
| Exclude file | `nmap 192.168.1.0/24 --excludefile excl.txt` | Loại trừ từ file |

---

## 2. Host Discovery

### 2.1 Ping Scan – Khám phá host còn sống

```bash
# Ping sweep toàn subnet (không scan port)
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

### 2.2 TCP/UDP Ping

```bash
# TCP SYN ping (port 80)
nmap -PS80 -sn 192.168.1.0/24

# TCP SYN ping (multi port)
nmap -PS22,80,443,3389 -sn 192.168.1.0/24

# TCP ACK ping
nmap -PA80 -sn 192.168.1.0/24

# UDP ping (port 53)
nmap -PU53 -sn 192.168.1.0/24
```

### 2.3 Bỏ qua host discovery

```bash
# Xem host như online dù không ping được (bypass FW block ICMP)
nmap -Pn 192.168.1.1

# Không DNS lookup
nmap -n 192.168.1.0/24

# Chỉ DNS lookup, không scan
nmap -sL 192.168.1.0/24
```

### Flags Host Discovery

| Flag | Mô tả |
|------|-------|
| `-sn` | No port scan – chỉ host discovery |
| `-Pn` | Bỏ qua host discovery, scan thẳng port |
| `-n` | Tắt DNS reverse lookup |
| `-R` | DNS lookup cho tất cả host (kể cả offline) |
| `-PR` | ARP ping (LAN – nhanh và chính xác nhất) |
| `-PE` | ICMP echo request |
| `-PP` | ICMP timestamp |
| `-PM` | ICMP netmask |
| `-PS[ports]` | TCP SYN ping |
| `-PA[ports]` | TCP ACK ping |
| `-PU[ports]` | UDP ping |

> **Tip:** Trên LAN dùng `-PR` nhanh và chính xác nhất. Ngoài internet dùng `-PE` hoặc `-PS80,443`.

---

## 3. Port Scan Techniques

### 3.1 TCP SYN Scan (Stealth Scan)

```bash
# SYN scan cơ bản – cần root/sudo
nmap -sS 192.168.1.1

# SYN + version + OS detection
nmap -sS -sV -O 192.168.1.1

# SYN scan tất cả 65535 ports
nmap -sS -p- 192.168.1.1
```

**Cách hoạt động:**
```
Attacker → SYN → Target
Attacker ← SYN/ACK ← Target  (port open)
Attacker → RST → Target       (không hoàn thành handshake → ít log)
```

### 3.2 TCP Connect Scan

```bash
# Connect scan – không cần root
nmap -sT 192.168.1.1

# Dùng khi không có quyền root hoặc qua proxy
nmap -sT -Pn 192.168.1.1
```

> **Lưu ý:** `-sT` hoàn thành 3-way handshake → bị log nhiều hơn `-sS`.

### 3.3 UDP Scan

```bash
# UDP scan các port phổ biến
nmap -sU -p 53,67,68,69,123,161,162,500,4500 192.168.1.1

# Kết hợp TCP SYN + UDP trong 1 lệnh
nmap -sS -sU -p T:80,443,8080,U:53,161 192.168.1.1

# UDP scan nhanh hơn với max-retries
nmap -sU --max-retries 1 --host-timeout 5m 192.168.1.1
```

> **Cảnh báo:** UDP scan rất chậm. Chỉ scan port quan trọng: `53, 67-68, 69, 123, 161, 500, 4500, 5060`.

### 3.4 Scan kiểu đặc biệt (Stealth Variants)

```bash
# TCP Null Scan – không set flag nào
nmap -sN 192.168.1.1

# TCP FIN Scan
nmap -sF 192.168.1.1

# Xmas Scan – FIN + PSH + URG
nmap -sX 192.168.1.1

# Maimon Scan – FIN/ACK
nmap -sM 192.168.1.1

# ACK Scan – phát hiện firewall rules
nmap -sA 192.168.1.1

# Window Scan
nmap -sW 192.168.1.1
```

> **Khi dùng Null/FIN/Xmas:**  
> - Port **open hoặc filtered** → không response  
> - Port **closed** → RST  
> - **Không hoạt động trên Windows** (Windows luôn trả RST)

### 3.5 Port Range & Selection

```bash
# Scan tất cả 65535 ports
nmap -p- 192.168.1.1

# Port cụ thể
nmap -p 22,80,443,8080,3306,3389 192.168.1.1

# Port range
nmap -p 1-1024 192.168.1.1

# Top 100 port phổ biến nhất
nmap --top-ports 100 192.168.1.1

# Top 1000 (default)
nmap --top-ports 1000 192.168.1.1

# Fast mode – 100 port
nmap -F 192.168.1.1

# TCP và UDP cùng lúc
nmap -p T:80,443,U:53,161 192.168.1.1
```

### Bảng so sánh Scan Types

| Loại | Flag | Cần root | Noisy | Bypass FW | Ghi chú |
|------|------|----------|-------|-----------|---------|
| TCP SYN | `-sS` | ✓ | Thấp | Trung bình | Mặc định khi có root |
| TCP Connect | `-sT` | ✗ | Cao | Thấp | Mặc định khi không có root |
| UDP | `-sU` | ✓ | Thấp | Trung bình | Rất chậm |
| TCP Null | `-sN` | ✓ | Rất thấp | Cao | Không hoạt động trên Windows |
| TCP FIN | `-sF` | ✓ | Rất thấp | Cao | Không hoạt động trên Windows |
| Xmas | `-sX` | ✓ | Rất thấp | Cao | Không hoạt động trên Windows |
| ACK | `-sA` | ✓ | Thấp | N/A | Dùng để map firewall rules |
| Idle/Zombie | `-sI` | ✓ | Không | Cao | Cần zombie host thích hợp |

---

## 4. Service & OS Detection

### 4.1 Version Detection (`-sV`)

```bash
# Version scan cơ bản
nmap -sV 192.168.1.1

# Version intensity tối đa (chậm hơn nhưng chi tiết hơn)
nmap -sV --version-intensity 9 192.168.1.1

# Light mode – nhanh hơn
nmap -sV --version-light 192.168.1.1

# Thử tất cả probes
nmap -sV --version-all 192.168.1.1
```

| Flag | Tương đương | Mô tả |
|------|-------------|-------|
| `--version-intensity 0-9` | — | 0=nhẹ, 9=nặng nhất (default 7) |
| `--version-light` | intensity 2 | Nhanh, ít chính xác |
| `--version-all` | intensity 9 | Thử tất cả probes |

### 4.2 OS Detection (`-O`)

```bash
# OS detection cơ bản
nmap -O 192.168.1.1

# OS + version detection (combo chuẩn)
nmap -sV -O 192.168.1.1

# Aggressive guess kể cả khi uncertain
nmap -O --osscan-guess 192.168.1.1

# Chỉ OS scan khi có ít nhất 1 open + 1 closed port
nmap -O --osscan-limit 192.168.1.1
```

> **Cảnh báo:** OS detection cần ít nhất **1 open** và **1 closed** port. Nếu firewall block hết thì kết quả không chính xác.

### 4.3 Aggressive Mode (`-A`)

```bash
# All-in-one: OS + version + default scripts + traceroute
nmap -A 192.168.1.1

# Aggressive + tất cả ports
nmap -A -p- 192.168.1.1

# Aggressive + timing T4
nmap -A -T4 192.168.1.1
```

`-A` = `-sV -O --script=default --traceroute`

> **Cảnh báo:** `-A` rất noisy! Chỉ dùng khi đã có phép và không cần stealth.

### 4.4 Traceroute

```bash
# Trace đường đi tới target
nmap --traceroute 192.168.1.1

# Traceroute + verbose
nmap --traceroute -v 192.168.1.1
```

---

## 5. NSE Scripts

### 5.1 NSE Categories

| Category | Mô tả | Khi dùng |
|----------|-------|----------|
| `default` | Scripts an toàn, hữu ích chung | Recon thông thường |
| `discovery` | Thu thập thông tin thêm | Enumeration |
| `safe` | Không gây hại cho target | Scan thụ động |
| `intrusive` | Có thể gây ảnh hưởng target | Cẩn thận khi dùng |
| `vuln` | Kiểm tra vulnerabilities | Vuln scanning |
| `exploit` | Khai thác lỗ hổng | Exploitation phase |
| `auth` | Kiểm tra authentication | Brute force, bypass |
| `brute` | Brute force credentials | Password attack |
| `malware` | Phát hiện malware/backdoor | Incident response |
| `external` | Dùng external services | WHOIS, DNS, v.v. |

### 5.2 Cách dùng Scripts

```bash
# Chạy default scripts (= -sC)
nmap -sC 192.168.1.1

# Script cụ thể
nmap --script=http-title 192.168.1.1

# Nhiều scripts
nmap --script=smb-vuln*,http-enum 192.168.1.1

# Toàn bộ category vuln
nmap --script vuln 192.168.1.1

# Script với arguments
nmap --script=http-brute --script-args http-brute.path=/login 192.168.1.1

# Cập nhật script database
nmap --script-updatedb

# Xem help của script
nmap --script-help http-enum
```

### 5.3 Scripts quan trọng theo dịch vụ

#### HTTP/HTTPS (port 80, 443, 8080)

```bash
# Enumeration đường dẫn ẩn
nmap --script http-enum -p 80,443,8080 192.168.1.1

# HTTP headers info
nmap --script http-headers -p 80 192.168.1.1

# HTTP methods cho phép
nmap --script http-methods -p 80 192.168.1.1

# Server info
nmap --script http-server-header -p 80 192.168.1.1

# Robots.txt
nmap --script http-robots.txt -p 80 192.168.1.1

# Shellshock vulnerability
nmap --script http-shellshock -p 80 192.168.1.1

# HTTP auth brute force
nmap --script http-brute -p 80 192.168.1.1

# WordPress vuln scan
nmap --script http-wordpress-enum -p 80 192.168.1.1

# Default credentials
nmap --script http-default-accounts -p 80 192.168.1.1
```

#### SMB (port 445, 139)

```bash
# Tất cả SMB vuln check
nmap --script smb-vuln* -p 445 192.168.1.1

# MS17-010 – EternalBlue (WannaCry)
nmap --script smb-vuln-ms17-010 -p 445 192.168.1.1

# MS08-067 – Conficker
nmap --script smb-vuln-ms08-067 -p 445 192.168.1.1

# MS06-025
nmap --script smb-vuln-ms06-025 -p 445 192.168.1.1

# SMB security mode
nmap --script smb-security-mode -p 445 192.168.1.1

# Liệt kê shares
nmap --script smb-enum-shares -p 445 192.168.1.1

# Liệt kê users
nmap --script smb-enum-users -p 445 192.168.1.1

# SMB OS discovery
nmap --script smb-os-discovery -p 445 192.168.1.1

# Null session check
nmap --script smb-enum-sessions -p 445 192.168.1.1
```

#### FTP (port 21)

```bash
# Anonymous FTP login
nmap --script ftp-anon -p 21 192.168.1.1

# FTP bounce scan
nmap --script ftp-bounce -p 21 192.168.1.1

# FTP brute force
nmap --script ftp-brute -p 21 192.168.1.1

# vsFTPd 2.3.4 backdoor
nmap --script ftp-vsftpd-backdoor -p 21 192.168.1.1
```

#### SSH (port 22)

```bash
# SSH auth methods
nmap --script ssh-auth-methods -p 22 192.168.1.1

# SSH hostkey info
nmap --script ssh-hostkey -p 22 192.168.1.1

# SSH brute force
nmap --script ssh-brute -p 22 192.168.1.1

# SSH2 algorithms
nmap --script ssh2-enum-algos -p 22 192.168.1.1
```

#### SSL/TLS (port 443)

```bash
# Enumerate cipher suites
nmap --script ssl-enum-ciphers -p 443 192.168.1.1

# Heartbleed vulnerability
nmap --script ssl-heartbleed -p 443 192.168.1.1

# POODLE vulnerability
nmap --script ssl-poodle -p 443 192.168.1.1

# DROWN vulnerability
nmap --script ssl-drown -p 443 192.168.1.1

# CCS injection
nmap --script ssl-ccs-injection -p 443 192.168.1.1

# Certificate info
nmap --script ssl-cert -p 443 192.168.1.1

# Date validity
nmap --script ssl-date -p 443 192.168.1.1
```

#### Database (MySQL, MSSQL, PostgreSQL)

```bash
# MySQL empty password
nmap --script mysql-empty-password -p 3306 192.168.1.1

# MySQL info
nmap --script mysql-info -p 3306 192.168.1.1

# MySQL databases
nmap --script mysql-databases --script-args mysqluser=root -p 3306 192.168.1.1

# MSSQL info
nmap --script ms-sql-info -p 1433 192.168.1.1

# MSSQL empty password
nmap --script ms-sql-empty-password -p 1433 192.168.1.1

# MSSQL xp_cmdshell
nmap --script ms-sql-xp-cmdshell --script-args "mssql.username=sa,mssql.password=,ms-sql-xp-cmdshell.cmd=ipconfig" -p 1433 192.168.1.1

# PostgreSQL brute
nmap --script pgsql-brute -p 5432 192.168.1.1
```

#### RDP (port 3389)

```bash
# RDP encryption level
nmap --script rdp-enum-encryption -p 3389 192.168.1.1

# MS12-020 – Remote code execution
nmap --script rdp-vuln-ms12-020 -p 3389 192.168.1.1
```

#### SNMP (port 161 UDP)

```bash
# SNMP brute community string
nmap --script snmp-brute -sU -p 161 192.168.1.1

# SNMP system info
nmap --script snmp-sysdescr -sU -p 161 192.168.1.1

# SNMP network interfaces
nmap --script snmp-interfaces -sU -p 161 192.168.1.1

# SNMP full enumeration
nmap --script snmp-info,snmp-interfaces,snmp-netstat,snmp-processes,snmp-sysdescr -sU -p 161 192.168.1.1
```

#### DNS (port 53)

```bash
# DNS brute subdomain
nmap --script dns-brute 192.168.1.1

# DNS zone transfer
nmap --script dns-zone-transfer --script-args dns-zone-transfer.domain=target.com -p 53 192.168.1.1

# DNS recursion
nmap --script dns-recursion -sU -p 53 192.168.1.1
```

#### VPN/IKE (port 500 UDP)

```bash
# IKE transforms enumeration
nmap --script ike-version -sU -p 500 192.168.1.1
```

### 5.4 Script Path & Custom Scripts

```bash
# Vị trí scripts
ls /usr/share/nmap/scripts/

# Tìm script theo tên
ls /usr/share/nmap/scripts/ | grep smb

# Xem source code script
cat /usr/share/nmap/scripts/http-enum.nse
```

---

## 6. Stealth & Evasion

### 6.1 Timing Templates

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

# Paranoid (bypass Time-based IDS)
nmap -T0 --max-retries 1 192.168.1.1
```

### 6.2 Packet Fragmentation

```bash
# Fragment thành 8-byte chunks (bypass stateless FW)
nmap -f 192.168.1.1

# Fragment mạnh hơn – 16 byte chunks
nmap -ff 192.168.1.1

# Custom MTU (phải là bội của 8)
nmap --mtu 24 192.168.1.1

# Kết hợp fragmentation + SYN scan
nmap -f -sS 192.168.1.1
```

### 6.3 Decoy Scan

```bash
# Decoy ngẫu nhiên (10 decoys)
nmap -D RND:10 192.168.1.1

# Decoy cụ thể – ME là IP thật của mình
nmap -D 10.0.0.1,10.0.0.2,10.0.0.3,ME 192.168.1.1

# Decoy + SYN scan
nmap -D RND:5 -sS 192.168.1.1
```

> **Nguyên lý:** Decoy tạo traffic từ nhiều IP giả → IDS/analyst khó xác định attacker thật.

### 6.4 Source IP Spoofing

```bash
# Spoof source IP (sẽ không nhận response)
nmap -S 10.0.0.100 -e eth0 192.168.1.1

# Spoof + specify interface
nmap -S 10.0.0.100 -e eth0 -n 192.168.1.1
```

> **Cảnh báo:** `-S` (IP spoof) sẽ không nhận được response trả về. Dùng `-D` thực tế hơn cho pentest.

### 6.5 Idle/Zombie Scan – Hoàn toàn ẩn danh

```bash
# Bước 1: Tìm zombie phù hợp (IPID incremental)
nmap -O -v 192.168.1.5
nmap --script ipidseq 192.168.1.5

# Bước 2: Thực hiện idle scan qua zombie
nmap -sI 192.168.1.5 192.168.1.1

# Bước 3: Chỉ định zombie port (nếu cần)
nmap -sI 192.168.1.5:80 192.168.1.1
```

**Cách hoạt động:**
```
1. Attacker → kiểm tra IPID của Zombie
2. Attacker gửi SYN giả IP Zombie → Target
3. Target → SYN/ACK → Zombie (nếu port open)
4. Zombie → RST → Target (IPID tăng +1)
5. Attacker so sánh IPID trước/sau để suy ra trạng thái port
```

> **Yêu cầu zombie:** IPID phải tăng tuần tự (predictable). Nhiều máy Windows XP, máy in, một số embedded device đáp ứng.

---

## 7. Firewall Bypass

### 7.1 Source Port Tricks

```bash
# Dùng port 53 (DNS) làm source – nhiều FW cho qua
nmap --source-port 53 192.168.1.1

# Dùng port 80 làm source
nmap --source-port 80 192.168.1.1

# Dùng port 443 làm source
nmap --source-port 443 192.168.1.1

# Kết hợp với SYN scan
nmap -sS --source-port 53 192.168.1.1
```

### 7.2 Packet Manipulation

```bash
# Thêm random data padding vào packet
nmap --data-length 200 192.168.1.1

# Custom MTU để bypass deep packet inspection
nmap --mtu 24 192.168.1.1

# Gửi packet có checksum sai – test IDS response
nmap --badsum 192.168.1.1

# Thêm IP options
nmap --ip-options "L 192.168.1.1 192.168.1.2" 192.168.1.1
```

### 7.3 Scan qua Proxy & Tor

```bash
# Qua proxychains (cần cấu hình /etc/proxychains.conf)
proxychains nmap -sT -Pn 192.168.1.1

# Qua SOCKS5 proxy trực tiếp
nmap -sT -Pn --proxy socks5://127.0.0.1:9050 192.168.1.1

# Qua HTTP proxy
nmap -sT -Pn --proxy http://127.0.0.1:8080 192.168.1.1
```

> **Bắt buộc:** Khi dùng proxy chỉ dùng `-sT` (TCP Connect). Các raw packet scan (`-sS`, `-sU`) sẽ không hoạt động qua proxy.

### 7.4 ACK Scan – Map Firewall Rules

```bash
# ACK scan để xác định port nào firewall cho qua
nmap -sA 192.168.1.1

# ACK scan kết hợp window scan
nmap -sW 192.168.1.1
```

| Response | Ý nghĩa |
|----------|---------|
| RST | Port **unfiltered** (FW cho qua) |
| Không response / ICMP unreachable | Port **filtered** (FW block) |

### 7.5 Bypass Host-based Firewall (Windows)

```bash
# Scan qua port 80 (thường được phép)
nmap -sS --source-port 80 -p 445 192.168.1.1

# Fragment nhỏ để bypass stateful inspection
nmap -f --mtu 8 192.168.1.1
```

---

## 8. Output & Reporting

### 8.1 Output Formats

```bash
# Normal output – dễ đọc cho người
nmap -oN scan_normal.txt 192.168.1.1

# XML – import vào Metasploit, Faraday, các tools khác
nmap -oX scan_results.xml 192.168.1.1

# Grepable format – dễ dùng với grep/awk/sed
nmap -oG scan_grep.gnmap 192.168.1.1

# Tất cả 3 format cùng lúc (KHUYÊN DÙNG)
nmap -oA scan_all 192.168.1.1

# Script kiddie output (lol)
nmap -oS scan_l33t.txt 192.168.1.1
```

> **Best practice:** Luôn dùng `-oA <basename>` để lưu tất cả format. XML dùng để import vào Metasploit:  
> `db_import scan_all.xml`

### 8.2 Verbosity & Debugging

```bash
# Verbose level 1
nmap -v 192.168.1.1

# Verbose level 2 (hiện thêm chi tiết)
nmap -vv 192.168.1.1

# Debug level 1
nmap -d 192.168.1.1

# Debug level 2 (rất nhiều thông tin)
nmap -dd 192.168.1.1

# Hiện lý do port state (SYN-ACK, RST, ...)
nmap --reason 192.168.1.1

# Chỉ hiện open ports
nmap --open 192.168.1.0/24

# Hiện từng packet gửi/nhận
nmap --packet-trace 192.168.1.1
```

### 8.3 Xử lý kết quả với grep/awk

```bash
# Lọc host có port 80 open từ grepable output
grep "80/open" scan_all.gnmap | awk '{print $2}'

# Liệt kê tất cả IP đang up
grep "Status: Up" scan_all.gnmap | awk '{print $2}'

# Tìm hosts có port SSH open
grep "22/open" scan_all.gnmap

# Lọc open ports của 1 host
grep "192.168.1.1" scan_all.gnmap
```

### 8.4 Import vào Metasploit

```bash
# Trong msfconsole:
msf> db_import /path/to/scan_all.xml
msf> hosts          # xem danh sách hosts
msf> services       # xem danh sách services
msf> vulns          # xem vulnerabilities
```

---

## 9. Performance Tuning

### 9.1 Parallelism & Timing

```bash
# Tối thiểu 100 probes song song
nmap --min-parallelism 100 192.168.1.0/24

# Tối đa 200 probes song song
nmap --max-parallelism 200 192.168.1.0/24

# Rate tối thiểu 1000 packets/giây
nmap --min-rate 1000 192.168.1.0/24

# Rate tối đa 5000 packets/giây
nmap --max-rate 5000 192.168.1.0/24

# Custom RTT timeout
nmap --max-rtt-timeout 100ms --min-rtt-timeout 50ms 192.168.1.0/24

# Host timeout 3 phút
nmap --host-timeout 3m 192.168.1.0/24

# Delay giữa các probe
nmap --scan-delay 200ms 192.168.1.0/24
nmap --max-scan-delay 500ms 192.168.1.0/24
```

### 9.2 Retries

```bash
# Giảm retries để nhanh hơn (hy sinh accuracy)
nmap --max-retries 1 192.168.1.0/24

# Không retry
nmap --max-retries 0 192.168.1.0/24
```

### 9.3 Preset nhanh cho scan lớn

```bash
# Scan nhanh subnet lớn – cân bằng tốc độ/accuracy
nmap -sS -T4 --min-rate 5000 --max-retries 1 -p- 192.168.1.0/24

# Scan cực nhanh chỉ top 1000 ports
nmap -sS -T5 --min-rate 10000 --top-ports 1000 192.168.1.0/24

# Scan subnet chậm để tránh IDS
nmap -sS -T1 --scan-delay 1s --max-retries 2 192.168.1.0/24
```

---

## 10. Workflow Thực Chiến

### Phase 1: Network Discovery

```bash
# Bước 1: Xác định host alive trong subnet
nmap -sn -T4 192.168.1.0/24 -oG alive_hosts.gnmap

# Lọc IP đang up
grep "Status: Up" alive_hosts.gnmap | awk '{print $2}' > live_hosts.txt

# Bước 2: Scan nhanh top ports trên tất cả live hosts
nmap -sS -T4 --top-ports 1000 -iL live_hosts.txt -oA phase1_quick
```

### Phase 2: Detailed Enumeration

```bash
# Bước 3: Full port scan trên các target thú vị
nmap -sS -p- -T4 --min-rate 5000 192.168.1.10 -oA phase2_fullport

# Bước 4: Service + OS detection
nmap -sV -O -sC -p $(grep "open" phase2_fullport.gnmap | grep -oP '\d+(?=/open)' | tr '\n' ',') 192.168.1.10 -oA phase2_detail
```

### Phase 3: Vulnerability Scanning

```bash
# Bước 5: Vuln scan theo service phát hiện được
# Nếu có SMB:
nmap --script smb-vuln* -p 445 192.168.1.10

# Nếu có HTTP:
nmap --script http-enum,http-vuln* -p 80,443,8080 192.168.1.10

# Nếu có SSL:
nmap --script ssl-enum-ciphers,ssl-heartbleed,ssl-poodle -p 443 192.168.1.10

# Toàn bộ vuln scan
nmap --script vuln -sV 192.168.1.10 -oA phase3_vuln
```

### Phase 4: External Recon (Black-box)

```bash
# DNS enumeration
nmap --script dns-brute,dns-zone-transfer -p 53 target.com

# Subdomain + service
nmap -sS -sV -T4 --script http-headers,http-title -p 80,443 target.com

# Scan qua Tor cho ẩn danh
proxychains nmap -sT -Pn -T2 --top-ports 100 target.com
```

---

## 11. Cheatsheet Quick Reference

### Lệnh hay dùng nhất

```bash
# Quick scan (top 1000, version, scripts)
nmap -sV -sC -T4 192.168.1.1

# Full aggressive
nmap -A -T4 -p- 192.168.1.1

# Stealth + save all
nmap -sS -T2 -oA result 192.168.1.0/24

# Vuln check
nmap --script vuln -sV 192.168.1.1

# UDP important ports
nmap -sU -p 53,161,500 192.168.1.1

# SMB check
nmap --script smb-vuln-ms17-010 -p 445 192.168.1.1

# SSL check
nmap --script ssl-enum-ciphers,ssl-heartbleed -p 443 192.168.1.1
```

### Flag Index

| Flag | Mô tả |
|------|-------|
| `-sS` | TCP SYN Scan |
| `-sT` | TCP Connect Scan |
| `-sU` | UDP Scan |
| `-sN` | TCP Null Scan |
| `-sF` | TCP FIN Scan |
| `-sX` | Xmas Scan |
| `-sA` | ACK Scan (map firewall) |
| `-sI <zombie>` | Idle/Zombie Scan |
| `-sn` | Ping Scan (no port scan) |
| `-Pn` | No ping (skip host discovery) |
| `-n` | No DNS resolution |
| `-sV` | Service version detection |
| `-O` | OS detection |
| `-A` | Aggressive (OS+version+script+traceroute) |
| `-sC` | Default scripts |
| `--script <name>` | Run specific script |
| `-p-` | All 65535 ports |
| `-p <port>` | Specific ports |
| `-F` | Fast – top 100 ports |
| `--top-ports N` | Top N ports |
| `-T0` đến `-T5` | Timing templates |
| `-f` | Fragment packets (8 byte) |
| `-ff` | Fragment packets (16 byte) |
| `--mtu N` | Custom MTU |
| `-D <decoys>` | Decoy scan |
| `-S <IP>` | Spoof source IP |
| `--source-port N` | Source port |
| `--data-length N` | Pad packets |
| `-oN` | Normal output |
| `-oX` | XML output |
| `-oG` | Grepable output |
| `-oA` | All formats |
| `-v / -vv` | Verbose |
| `--reason` | Show port state reason |
| `--open` | Only show open ports |
| `--min-rate N` | Min packets/sec |
| `--max-rate N` | Max packets/sec |
| `--max-retries N` | Max probe retries |
| `--host-timeout` | Per-host timeout |

### Port List quan trọng

| Port | Service | Scan gợi ý |
|------|---------|-----------|
| 21 | FTP | `--script ftp-anon,ftp-vsftpd-backdoor` |
| 22 | SSH | `--script ssh-auth-methods,ssh-brute` |
| 23 | Telnet | `--script telnet-brute` |
| 25 | SMTP | `--script smtp-enum-users` |
| 53 | DNS | `--script dns-brute,dns-zone-transfer` |
| 80/443 | HTTP/S | `--script http-enum,http-vuln*` |
| 110 | POP3 | `--script pop3-brute` |
| 135 | MSRPC | `-sV` |
| 139/445 | SMB | `--script smb-vuln*,smb-enum-*` |
| 161 | SNMP (UDP) | `-sU --script snmp-*` |
| 389 | LDAP | `--script ldap-*` |
| 443 | HTTPS | `--script ssl-*` |
| 1433 | MSSQL | `--script ms-sql-*` |
| 1521 | Oracle | `--script oracle-*` |
| 3306 | MySQL | `--script mysql-*` |
| 3389 | RDP | `--script rdp-*` |
| 5432 | PostgreSQL | `--script pgsql-brute` |
| 5900 | VNC | `--script vnc-brute,vnc-info` |
| 6379 | Redis | `--script redis-info` |
| 8080 | HTTP-Alt | `--script http-enum` |
| 27017 | MongoDB | `--script mongodb-info` |

---

> **Disclaimer:** Tài liệu này chỉ dùng cho mục đích giáo dục và authorized penetration testing. Không sử dụng trên hệ thống không được phép.