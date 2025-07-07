#!/bin/bash
mkdir -p "Program Files" AppData/Local AppData/Roaming images RecycleBin

# ------------------------
# 🧾 Top-Level Files
# ------------------------

# Hidden config
cat <<EOF > .vimrc
set number
syntax on
set tabstop=4
EOF

# Fake creds
cat <<EOF > creds.txt
# leaked FTP credentials
username: user5
password: tryme123
EOF

# Fake .env
cat <<EOF > secrets.env
API_KEY=asdf1234lkjhg
DB_PASS=changeme
JWT_SECRET=supersecrettoken
EOF

# Broken config
cat <<EOF > broken_config.cfg
[network]
timeout=∞
retry=999
mode=experimental

[auth]
token=::INVALID::
EOF

# Log file
for i in {1..20}; do
  echo "[ERROR] Service failed at $(date -d "-$i min")" >> system.log
done

# Notes
cat <<EOF > notes.old
1. Fix backup corruption.
2. Ask Mark about the old VPN key.
3. Don’t forget: user5 only has frontend access.
EOF

# Web backup
cat <<EOF > web_backup.bak
-- SQLITE BACKUP FILE START --
TABLE users (id, username, password_hash)
TABLE flags (id, flag_value)
EOF

# PDF decoy
echo "Fake PDF content. FLAG not here :)" > flag.pdf

# "Database"
cat <<EOF > xxx.db
SQLite format 3
CREATE TABLE users(id INT, name TEXT, password TEXT);
INSERT INTO users VALUES(1, 'admin', 'notarealhash');
EOF

# "DLL"
echo "This is not a real DLL file, just bait." > xxx.dll

# Corrupted ISO
echo "ISO9660 FAKE IMAGE - BOOT FAILURE" > corrupted.iso

# ------------------------
# 🧰 Program Files
# ------------------------

cat <<EOF > "Program Files/updater.exe"
This binary updates the internal configs.
Version: 3.3.7
EOF

cat <<EOF > "Program Files/winlogon.scr"
Fake Windows screensaver.
Do not trust.
EOF

# ------------------------
# 🖼️ Images
# ------------------------

echo "PNG FAKE HEADER" > images/img1.png
echo "IMG2 - corrupted pixels!" > images/img2_corrupted.png

# ------------------------
# 🗂️ AppData
# ------------------------

echo "TEMP FILE, DO NOT DELETE" > AppData/Local/temp.tmp
cat <<EOF > AppData/Roaming/secrets.sqlite
SQLite format 3
-- This is a decoy file for player frustration --
EOF

# ------------------------
# 🗑️ Recycle Bin
# ------------------------

cat <<EOF > RecycleBin/deleted.docx
Dear manager,

I’ve accidentally deleted the secret.zip password. Sorry.

Regards,
Intern
EOF

# ------------------------
# 🔐 ZIP FILE
# ------------------------

zip --password 123456 secret.zip xxx.db xxx.dll system.log creds.txt > /dev/null
