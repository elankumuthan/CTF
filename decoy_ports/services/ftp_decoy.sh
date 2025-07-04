#!/bin/bash
# services/ftp_decoy.sh - Interactive FTP honeypot
echo "220 CTF-FTP-Server 2.1.0 ready"
while read line; do
    case "$line" in
        USER*) echo "331 Password required for user" ;;
        PASS*) echo "530 Login incorrect" ;;
        QUIT*) echo "221 Goodbye"; exit ;;
        LIST*) echo "150 Here comes the directory listing"
               echo "drwxr-xr-x 2 root root 4096 Jan 01 12:00 .secret"
               echo "-rw-r--r-- 1 root root 1337 Jan 01 12:00 flag.txt"
               echo "226 Directory send OK" ;;
        RETR*) echo "550 Permission denied" ;;
        *) echo "500 Unknown command" ;;
    esac
done