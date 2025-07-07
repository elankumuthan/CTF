#!/bin/bash
set -e

echo "[+] Fixing rule order in DOCKER-USER chain..."

# Backup info
echo "[+] Backing up existing ACCEPT/RETURN rules..."
ACCEPT_RULES=$(sudo iptables -S DOCKER-USER | grep -E "ACCEPT|RETURN")

echo "[+] Current DOCKER-USER chain:"
sudo iptables -L DOCKER-USER -v --line-numbers

echo ""
echo "[+] Clearing old DROP rules to reorder properly..."
sudo iptables -D DOCKER-USER -p icmp --icmp-type echo-request -j DROP 2>/dev/null || echo "  [!] ICMP echo-request rule not found"
sudo iptables -D DOCKER-USER -p icmp --icmp-type timestamp-request -j DROP 2>/dev/null || echo "  [!] ICMP timestamp rule not found"
sudo iptables -D DOCKER-USER -p icmp --icmp-type address-mask-request -j DROP 2>/dev/null || echo "  [!] ICMP address-mask rule not found"
sudo iptables -D DOCKER-USER -p tcp --dport 443 --syn -j DROP 2>/dev/null || echo "  [!] TCP port 443 rule not found"
sudo iptables -D DOCKER-USER -p udp --dport 53 -j DROP 2>/dev/null || echo "  [!] UDP port 53 rule not found"
# NOTE: Port 80 is intentionally not dropped

echo ""
echo "[+] Inserting updated DROP rules at the TOP of the DOCKER-USER chain..."
sudo iptables -I DOCKER-USER 1 -p icmp --icmp-type echo-request -j DROP
sudo iptables -I DOCKER-USER 1 -p icmp --icmp-type timestamp-request -j DROP
sudo iptables -I DOCKER-USER 1 -p icmp --icmp-type address-mask-request -j DROP
sudo iptables -I DOCKER-USER 1 -p tcp --dport 443 --syn -j DROP
sudo iptables -I DOCKER-USER 1 -p udp --dport 53 -j DROP

echo ""
echo "[+] Final DOCKER-USER chain:"
sudo iptables -L DOCKER-USER -v --line-numbers

echo ""
echo "[+] Saving firewall rules..."
if command -v netfilter-persistent >/dev/null; then
    sudo netfilter-persistent save
else
    echo "[!] netfilter-persistent not found. Rules will be lost on reboot."
fi

echo ""
echo "[✓] Rule order fixed. Port 80 is left open for honeypots."
echo ""
echo "🔍 Test from attacker machine:"
echo "  ping <ip>                  → should timeout"
echo "  nmap <ip>                  → should say 'Host seems down'"
echo "  nmap -Pn <ip>              → should reveal open ports, including 80"
