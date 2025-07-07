#!/bin/bash
set -e

echo "[~] Removing all Nmap blocking rules..."
echo ""

echo "[~] Removing ICMP-based host discovery blocks..."
sudo iptables -D DOCKER-USER -p icmp --icmp-type echo-request -j DROP 2>/dev/null || echo "  [!] ICMP echo-request rule not found"
sudo iptables -D DOCKER-USER -p icmp --icmp-type timestamp-request -j DROP 2>/dev/null || echo "  [!] ICMP timestamp-request rule not found"
sudo iptables -D DOCKER-USER -p icmp --icmp-type address-mask-request -j DROP 2>/dev/null || echo "  [!] ICMP address-mask-request rule not found"

echo "[~] Removing TCP-based host discovery blocks (only port 443)..."
# Leave port 80 open permanently for honeypots
sudo iptables -D DOCKER-USER -p tcp --dport 443 --syn -j DROP 2>/dev/null || echo "  [!] TCP port 443 SYN rule not found"

echo "[~] Removing UDP-based host discovery blocks..."
sudo iptables -D DOCKER-USER -p udp --dport 53 -j DROP 2>/dev/null || echo "  [!] UDP port 53 rule not found"

echo "[~] Keeping connection tracking rules (Docker's defaults)..."
echo "  [i] ESTABLISHED,RELATED and NEW connection rules are Docker defaults - keeping them"

echo "[~] Saving updated firewall rules..."
if command -v netfilter-persistent >/dev/null; then
    sudo netfilter-persistent save
    echo "  [✓] Rules saved with netfilter-persistent"
else
    echo "  [!] 'iptables-persistent' not installed. Rules removed but not persisted."
    echo "      Rules will be restored on reboot unless you save them manually."
fi

echo ""
echo "[✓] All custom Nmap blocking rules removed!"
echo ""
echo "System restored to normal state:"
echo "  ✅ ICMP ping responses enabled"
echo "  ✅ TCP connections to port 443 allowed"
echo "  ✅ UDP port 53 accessible"
echo "  ✅ TCP port 80 remains open (honeypots unaffected)"
echo "  ✅ Normal Nmap scanning will now detect host"
echo ""
echo "Test commands:"
echo "  ping <ip>       - Should work"
echo "  nmap <ip>       - Should show open ports"
echo "  nmap -sn <ip>   - Should detect host as up"
