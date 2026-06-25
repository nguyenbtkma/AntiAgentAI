# Nmap – Output & Reporting

## Output Formats

```bash
# Normal – dễ đọc cho người
nmap -oN scan_normal.txt 192.168.1.1

# XML – import vào Metasploit, Faraday, các tools khác
nmap -oX scan_results.xml 192.168.1.1

# Grepable – dễ dùng với grep/awk/sed
nmap -oG scan_grep.gnmap 192.168.1.1

# Tất cả 3 format cùng lúc (KHUYÊN DÙNG)
nmap -oA scan_all 192.168.1.1
```

> Luôn dùng `-oA <basename>` để có đủ 3 format. XML cần thiết để import vào Metasploit.

## Verbosity & Debugging

```bash
# Verbose level 1
nmap -v 192.168.1.1

# Verbose level 2
nmap -vv 192.168.1.1

# Hiện lý do port state (SYN-ACK, RST, ...)
nmap --reason 192.168.1.1

# Chỉ hiện open ports
nmap --open 192.168.1.0/24

# Hiện từng packet gửi/nhận
nmap --packet-trace 192.168.1.1

# Debug level
nmap -d 192.168.1.1
nmap -dd 192.168.1.1
```

## Lọc kết quả với grep/awk

```bash
# Host có port 80 open
grep "80/open" scan_all.gnmap | awk '{print $2}'

# Tất cả IP đang up
grep "Status: Up" scan_all.gnmap | awk '{print $2}'

# Host có SSH open
grep "22/open" scan_all.gnmap

# Open ports của 1 host cụ thể
grep "192.168.1.1" scan_all.gnmap
```

## Import vào Metasploit

```bash
# Trong msfconsole
msf> db_import /path/to/scan_all.xml
msf> hosts        # danh sách hosts
msf> services     # danh sách services
msf> vulns        # vulnerabilities
```

## Flags tóm tắt

| Flag | Mô tả |
|------|-------|
| `-oN` | Normal output |
| `-oX` | XML output |
| `-oG` | Grepable output |
| `-oA <basename>` | Tất cả 3 format |
| `-v / -vv` | Verbose level 1/2 |
| `-d / -dd` | Debug level 1/2 |
| `--reason` | Lý do port state |
| `--open` | Chỉ hiện open ports |
| `--packet-trace` | Hiện từng packet |