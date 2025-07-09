#!/bin/bash
set -e

echo "[~] Removing all custom Nmap stealth rules..."
echo ""

# ─────────────────────────────────────────────
# 1. Remove ICMP blocks (DOCKER-USER + INPUT)
# ─────────────────────────────────────────────
echo "[~] Removing ICMP-based host discovery blocks..."
for CHAIN in DOCKER-USER INPUT; do
    sudo iptables -D $CHAIN -p icmp --icmp-type echo-request -j DROP 2>/dev/null || echo "  [!] ICMP echo-request rule not found in $CHAIN"
    sudo iptables -D $CHAIN -p icmp --icmp-type timestamp-request -j DROP 2>/dev/null || echo "  [!] ICMP timestamp-request rule not found in $CHAIN"
    sudo iptables -D $CHAIN -p icmp --icmp-type address-mask-request -j DROP 2>/dev/null || echo "  [!] ICMP address-mask-request rule not found in $CHAIN"
done

# ─────────────────────────────────────────────
# 2. Remove TCP SYN/ACK blocks (DOCKER-USER + INPUT)
# ─────────────────────────────────────────────
echo "[~] Removing TCP-based host discovery blocks (port 443)..."
for CHAIN in DOCKER-USER INPUT; do
    sudo iptables -D $CHAIN -p tcp --dport 443 --syn -j DROP 2>/dev/null || echo "  [!] TCP port 443 SYN rule not found in $CHAIN"
done

# ─────────────────────────────────────────────
# 3. Remove UDP-based discovery blocks (port 53)
# ─────────────────────────────────────────────
echo "[~] Removing UDP-based discovery blocks (port 53)..."
for CHAIN in DOCKER-USER INPUT; do
    sudo iptables -D $CHAIN -p udp --dport 53 -j DROP 2>/dev/null || echo "  [!] UDP port 53 rule not found in $CHAIN"
done

# ─────────────────────────────────────────────
# 4. Keep Docker’s default connection tracking
# ─────────────────────────────────────────────
echo "[~] Keeping Docker's connection tracking defaults (ESTABLISHED,RELATED)"
echo "  [i] This ensures existing services remain unaffected"

# ─────────────────────────────────────────────
# 5. Save rules (if possible)
# ─────────────────────────────────────────────
echo "[~] Saving updated firewall rules..."
if command -v netfilter-persistent >/dev/null; then
    sudo netfilter-persistent save
    echo "  [✓] Rules saved with netfilter-persistent"
elif command -v iptables-save >/dev/null && [ -d /etc/iptables ]; then
    sudo iptables-save > /etc/iptables/rules.v4
    echo "  [✓] Rules saved to /etc/iptables/rules.v4"
else
    echo "  [!] 'netfilter-persistent' or 'iptables-save' not found. Rules will be lost on reboot."
fi

# ─────────────────────────────────────────────
# 6. Final status message
# ─────────────────────────────────────────────
echo ""
echo "[✓] All custom stealth rules removed!"
echo ""
echo "System restored to full visibility:"
echo "  ✅ ICMP ping responses enabled"
echo "  ✅ TCP port 443 connections allowed"
echo "  ✅ UDP port 53 accessible"
echo "  ✅ Web (port 80) remains accessible"
echo ""
echo "Test it now from an attacker machine:"
echo "  ping <ip>         - Should respond"
echo "  nmap <ip>         - Should detect host + open ports"
echo "  nmap -sn <ip>     - Should say 'Host is up'"
