#!/bin/bash
# services/ssh_decoy.sh - SSH time waster
echo "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1"
# Hang for a few seconds then disconnect
sleep 5
echo "Connection closed by remote host"
