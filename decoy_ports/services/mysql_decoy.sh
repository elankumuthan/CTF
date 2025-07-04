#!/bin/bash
# services/mysql_decoy.sh - MySQL with fake flag bait
printf "\x5a\x00\x00\x00\x0a"
printf "8.0.32-ctf-edition\x00"
printf "\x01\x00\x00\x00"
printf "CTF{fake_mysql_flag_bait}\x00"
printf "\xff\xf7\xff\x02\x00\xff\xc1\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
printf "mysql_native_password\x00"