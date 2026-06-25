# Nmap – Workflow Thực Chiến

## Phase 1: Network Discovery

```bash
# Bước 1: Tìm host alive trong subnet
nmap -sn -T4 192.168.1.0/24 -oG alive_hosts.gnmap

# Lọc IP đang up
grep "Status: Up" alive_hosts.gnmap | awk '{print $2}' > live_hosts.txt

# Bước 2: Scan nhanh top 1000 ports trên tất cả live hosts
nmap -sS -T4 --top-ports 1000 -iL live_hosts.txt -oA phase1_quick
```

## Phase 2: Detailed Enumeration

```bash
# Bước 3: Full port scan trên target thú vị
nmap -sS -p- -T4 --min-rate 5000 192.168.1.10 -oA phase2_fullport

# Bước 4: Service + OS detection trên open ports
nmap -sV -O -sC -p 22,80,443,445 192.168.1.10 -oA phase2_detail
```

## Phase 3: Vulnerability Scanning

```bash
# SMB vuln
nmap --script smb-vuln* -p 445 192.168.1.10

# HTTP vuln
nmap --script http-enum,http-vuln* -p 80,443,8080 192.168.1.10

# SSL vuln
nmap --script ssl-enum-ciphers,ssl-heartbleed,ssl-poodle -p 443 192.168.1.10

# Toàn bộ vuln scan (chậm nhưng đầy đủ)
nmap --script vuln -sV 192.168.1.10 -oA phase3_vuln
```

## Phase 4: External Recon (Black-box)

```bash
# DNS enumeration
nmap --script dns-brute,dns-zone-transfer -p 53 target.com

# Web service info
nmap -sS -sV -T4 --script http-headers,http-title -p 80,443 target.com

# Scan ẩn danh qua Tor
proxychains nmap -sT -Pn -T2 --top-ports 100 target.com
```

## Quick Commands hay dùng nhất

```bash
# Quick recon 1 host
nmap -sV -sC -T4 192.168.1.1

# Full aggressive
nmap -A -T4 -p- 192.168.1.1

# Stealth + lưu kết quả
nmap -sS -T2 -oA result 192.168.1.0/24

# Vuln check nhanh
nmap --script vuln -sV 192.168.1.1

# UDP important ports
nmap -sU -p 53,161,500 192.168.1.1

# SMB check
nmap --script smb-vuln-ms17-010 -p 445 192.168.1.1

# SSL check
nmap --script ssl-enum-ciphers,ssl-heartbleed -p 443 192.168.1.1
```

## Quyết định scan theo phát hiện

| Phát hiện | Bước tiếp theo |
|-----------|---------------|
| Host mới | `nmap_host_discovery.md` → xác nhận alive |
| Port mở mới | `nmap_service_os.md` → detect service/version |
| Service xác định | `nmap_nse_scripts.md` → chạy script phù hợp |
| FW block | `nmap_firewall_bypass.md` → thử bypass |
| Cần ẩn | `nmap_stealth_evasion.md` → giảm noise |
| Subnet lớn | `nmap_performance.md` → tăng tốc |