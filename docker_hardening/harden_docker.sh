#!/bin/bash
set -e

echo "[+] Fixing Nmap visibility: stealth mode with port 80 left open..."

# ─────────────────────────────────────────────
# 1. BACKUP EXISTING RULES IN DOCKER-USER
# ─────────────────────────────────────────────
echo "[+] Backing up existing ACCEPT/RETURN rules from DOCKER-USER..."
ACCEPT_RULES=$(sudo iptables -S DOCKER-USER | grep -E "ACCEPT|RETURN")

echo "[+] Current DOCKER-USER chain:"
sudo iptables -L DOCKER-USER -v --line-numbers

# ─────────────────────────────────────────────
# 2. REMOVE OLD DROP RULES TO AVOID DUPLICATES
# ─────────────────────────────────────────────
echo "[+] Removing any existing DROP rules..."
sudo iptables -D DOCKER-USER -p icmp --icmp-type echo-request -j DROP 2>/dev/null || true
sudo iptables -D DOCKER-USER -p icmp --icmp-type timestamp-request -j DROP 2>/dev/null || true
sudo iptables -D DOCKER-USER -p icmp --icmp-type address-mask-request -j DROP 2>/dev/null || true
sudo iptables -D DOCKER-USER -p tcp --dport 443 --syn -j DROP 2>/dev/null || true
sudo iptables -D DOCKER-USER -p udp --dport 53 -j DROP 2>/dev/null || true

# ─────────────────────────────────────────────
# 3. INSERT NEW DROP RULES INTO DOCKER-USER
# ─────────────────────────────────────────────
echo "[+] Inserting stealth DROP rules into DOCKER-USER..."
sudo iptables -I DOCKER-USER 1 -p icmp --icmp-type echo-request -j DROP
sudo iptables -I DOCKER-USER 1 -p icmp --icmp-type timestamp-request -j DROP
sudo iptables -I DOCKER-USER 1 -p icmp --icmp-type address-mask-request -j DROP
sudo iptables -I DOCKER-USER 1 -p tcp --dport 443 --syn -j DROP
sudo iptables -I DOCKER-USER 1 -p udp --dport 53 -j DROP

# ─────────────────────────────────────────────
# 4. INSERT MATCHING RULES INTO HOST INPUT CHAIN
# ─────────────────────────────────────────────
echo "[+] Inserting stealth DROP rules into INPUT chain (for host)..."
sudo iptables -I INPUT -p icmp --icmp-type echo-request -j DROP
sudo iptables -I INPUT -p icmp --icmp-type timestamp-request -j DROP
sudo iptables -I INPUT -p icmp --icmp-type address-mask-request -j DROP
sudo iptables -I INPUT -p tcp --dport 443 --syn -j DROP
sudo iptables -I INPUT -p udp --dport 53 -j DROP

# ─────────────────────────────────────────────
# 5. SHOW FINAL RULES
# ─────────────────────────────────────────────
echo ""
echo "[✓] Final DOCKER-USER chain:"
sudo iptables -L DOCKER-USER -v --line-numbers

echo ""
echo "[✓] Final INPUT chain (filtered):"
sudo iptables -L INPUT -v --line-numbers | grep -E "DROP|icmp|443|53"

# ─────────────────────────────────────────────
# 6. SAVE RULES IF PERSISTENT SUPPORT EXISTS
# ─────────────────────────────────────────────
echo ""
echo "[+] Saving firewall rules..."
if command -v netfilter-persistent >/dev/null; then
    sudo netfilter-persistent save
elif command -v iptables-save >/dev/null && [ -d /etc/iptables ]; then
    sudo iptables-save > /etc/iptables/rules.v4
else
    echo "[!] Warning: Firewall rules will be lost on reboot. Install 'netfilter-persistent' or save manually."
fi

# ─────────────────────────────────────────────
# 7. DONE
# ─────────────────────────────────────────────
echo ""
echo "[✓] Stealth configuration complete."
echo ""
echo "🔍 Test this from your attacker VM:"
echo "    ping <ip>                → should fail"
echo "    nmap <ip>                → should say 'Host seems down'"
echo "    nmap -Pn <ip>            → should show open ports like 80"
