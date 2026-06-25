# Nmap – NSE Scripts

## Cách dùng scripts

```bash
# Chạy default scripts (= -sC)
nmap -sC 192.168.1.1

# Script cụ thể
nmap --script=http-title 192.168.1.1

# Nhiều scripts + wildcard
nmap --script=smb-vuln*,http-enum 192.168.1.1

# Toàn bộ category vuln
nmap --script vuln 192.168.1.1

# Script với arguments
nmap --script=http-brute --script-args http-brute.path=/login 192.168.1.1

# Xem help script
nmap --script-help http-enum

# Cập nhật script DB
nmap --script-updatedb
```

## NSE Categories

| Category | Mô tả | Khi dùng |
|----------|-------|----------|
| `default` | Scripts an toàn, hữu ích chung | Recon thông thường |
| `discovery` | Thu thập thêm thông tin | Enumeration |
| `safe` | Không gây hại | Scan thụ động |
| `intrusive` | Có thể ảnh hưởng target | Cẩn thận |
| `vuln` | Kiểm tra vulnerabilities | Vuln scanning |
| `exploit` | Khai thác lỗ hổng | Exploitation |
| `auth` | Kiểm tra authentication | Brute force, bypass |
| `brute` | Brute force credentials | Password attack |
| `malware` | Phát hiện malware/backdoor | Incident response |

---

## Scripts theo dịch vụ

### HTTP/HTTPS (port 80, 443, 8080)

```bash
nmap --script http-enum -p 80,443,8080 192.168.1.1          # Tìm hidden dirs
nmap --script http-headers -p 80 192.168.1.1                 # HTTP headers
nmap --script http-methods -p 80 192.168.1.1                 # Các method cho phép
nmap --script http-robots.txt -p 80 192.168.1.1              # Robots.txt
nmap --script http-shellshock -p 80 192.168.1.1              # Shellshock
nmap --script http-brute -p 80 192.168.1.1                   # Auth brute force
nmap --script http-wordpress-enum -p 80 192.168.1.1          # WordPress enum
nmap --script http-default-accounts -p 80 192.168.1.1        # Default credentials
```

### SMB (port 445, 139)

```bash
nmap --script smb-vuln* -p 445 192.168.1.1                   # Tất cả SMB vuln
nmap --script smb-vuln-ms17-010 -p 445 192.168.1.1           # EternalBlue (WannaCry)
nmap --script smb-vuln-ms08-067 -p 445 192.168.1.1           # Conficker
nmap --script smb-security-mode -p 445 192.168.1.1           # SMB security mode
nmap --script smb-enum-shares -p 445 192.168.1.1             # Liệt kê shares
nmap --script smb-enum-users -p 445 192.168.1.1              # Liệt kê users
nmap --script smb-os-discovery -p 445 192.168.1.1            # OS qua SMB
nmap --script smb-enum-sessions -p 445 192.168.1.1           # Null session check
```

### FTP (port 21)

```bash
nmap --script ftp-anon -p 21 192.168.1.1                     # Anonymous login
nmap --script ftp-bounce -p 21 192.168.1.1                   # FTP bounce
nmap --script ftp-brute -p 21 192.168.1.1                    # Brute force
nmap --script ftp-vsftpd-backdoor -p 21 192.168.1.1          # vsFTPd 2.3.4 backdoor
```

### SSH (port 22)

```bash
nmap --script ssh-auth-methods -p 22 192.168.1.1             # Auth methods
nmap --script ssh-hostkey -p 22 192.168.1.1                  # Host key info
nmap --script ssh-brute -p 22 192.168.1.1                    # Brute force
nmap --script ssh2-enum-algos -p 22 192.168.1.1              # Algorithms
```

### SSL/TLS (port 443)

```bash
nmap --script ssl-enum-ciphers -p 443 192.168.1.1            # Cipher suites
nmap --script ssl-heartbleed -p 443 192.168.1.1              # Heartbleed
nmap --script ssl-poodle -p 443 192.168.1.1                  # POODLE
nmap --script ssl-drown -p 443 192.168.1.1                   # DROWN
nmap --script ssl-ccs-injection -p 443 192.168.1.1           # CCS injection
nmap --script ssl-cert -p 443 192.168.1.1                    # Certificate info
```

### Database

```bash
# MySQL (3306)
nmap --script mysql-empty-password -p 3306 192.168.1.1
nmap --script mysql-info -p 3306 192.168.1.1
nmap --script mysql-databases --script-args mysqluser=root -p 3306 192.168.1.1

# MSSQL (1433)
nmap --script ms-sql-info -p 1433 192.168.1.1
nmap --script ms-sql-empty-password -p 1433 192.168.1.1
nmap --script ms-sql-xp-cmdshell --script-args "mssql.username=sa,mssql.password=,ms-sql-xp-cmdshell.cmd=whoami" -p 1433 192.168.1.1

# PostgreSQL (5432)
nmap --script pgsql-brute -p 5432 192.168.1.1
```

### RDP (port 3389)

```bash
nmap --script rdp-enum-encryption -p 3389 192.168.1.1        # Encryption level
nmap --script rdp-vuln-ms12-020 -p 3389 192.168.1.1          # MS12-020 RCE
```

### SNMP (port 161 UDP)

```bash
nmap --script snmp-brute -sU -p 161 192.168.1.1              # Brute community string
nmap --script snmp-sysdescr -sU -p 161 192.168.1.1           # System info
nmap --script snmp-interfaces -sU -p 161 192.168.1.1         # Network interfaces
nmap --script snmp-info,snmp-interfaces,snmp-netstat,snmp-processes,snmp-sysdescr -sU -p 161 192.168.1.1
```

### DNS (port 53)

```bash
nmap --script dns-brute 192.168.1.1                          # Subdomain brute
nmap --script dns-zone-transfer --script-args dns-zone-transfer.domain=target.com -p 53 192.168.1.1
nmap --script dns-recursion -sU -p 53 192.168.1.1            # DNS recursion
```

### VPN/IKE (port 500 UDP)

```bash
nmap --script ike-version -sU -p 500 192.168.1.1
```

---

## Port → Script nhanh

| Port | Service | Script gợi ý |
|------|---------|-------------|
| 21 | FTP | `ftp-anon,ftp-vsftpd-backdoor` |
| 22 | SSH | `ssh-auth-methods,ssh-brute` |
| 23 | Telnet | `telnet-brute` |
| 25 | SMTP | `smtp-enum-users` |
| 53 | DNS | `dns-brute,dns-zone-transfer` |
| 80/443 | HTTP/S | `http-enum,http-vuln*` |
| 139/445 | SMB | `smb-vuln*,smb-enum-*` |
| 161 UDP | SNMP | `snmp-brute,snmp-info` |
| 443 | HTTPS | `ssl-enum-ciphers,ssl-heartbleed` |
| 1433 | MSSQL | `ms-sql-info,ms-sql-empty-password` |
| 3306 | MySQL | `mysql-empty-password,mysql-info` |
| 3389 | RDP | `rdp-enum-encryption,rdp-vuln-ms12-020` |
| 5432 | PostgreSQL | `pgsql-brute` |
| 5900 | VNC | `vnc-brute,vnc-info` |
| 6379 | Redis | `redis-info` |
| 27017 | MongoDB | `mongodb-info` |

> Scripts nằm tại: `C:\Program Files (x86)\Nmap\scripts\` (Windows)
> hoặc `/usr/share/nmap/scripts/` (Linux)