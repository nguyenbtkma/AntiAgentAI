# Nmap Knowledge Base – Index

Đọc file này đầu tiên. Sau đó CHỈ đọc file phù hợp với tình huống hiện tại.
KHÔNG đọc tất cả cùng lúc – chỉ đọc khi cần thiết.

## Quyết định nhanh

| Tình huống | File cần đọc |
|-----------|-------------|
| Cần tìm host nào đang sống trong mạng | `nmap_host_discovery.md` |
| Chọn loại scan (SYN, UDP, Null, FIN...) | `nmap_port_scan.md` |
| Detect version service, OS fingerprint | `nmap_service_os.md` |
| Cần script NSE theo dịch vụ (SMB, HTTP, SSL, FTP, SSH, DB...) | `nmap_nse_scripts.md` |
| Cần scan ẩn, tránh IDS, timing, decoy, fragmentation | `nmap_stealth_evasion.md` |
| Bị firewall block, cần bypass | `nmap_firewall_bypass.md` |
| Lưu kết quả ra file, import Metasploit | `nmap_output.md` |
| Scan subnet lớn, cần tăng tốc | `nmap_performance.md` |
| Cần quy trình scan từ đầu đến cuối | `nmap_workflow.md` |

## Nguyên tắc chọn file

- Phát hiện host mới → `nmap_host_discovery.md`
- Biết host rồi, chưa biết port → `nmap_port_scan.md`
- Biết port, cần identify service/version → `nmap_service_os.md`
- Biết service, cần tìm vuln → `nmap_nse_scripts.md`
- Target có firewall/IDS → `nmap_stealth_evasion.md` hoặc `nmap_firewall_bypass.md`