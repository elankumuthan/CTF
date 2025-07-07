#!/bin/bash

echo "Starting CTF decoy services..."

# SSH (22) - Slow connection that hangs then disconnects
socat TCP-LISTEN:22,fork,reuseaddr EXEC:"/opt/services/ssh_decoy.sh" &
echo "SSH decoy started on port 22"

# HTTP (80) - Login panel with fake SQL injection hints
socat TCP-LISTEN:80,fork,reuseaddr EXEC:"echo -e 'HTTP/1.1 200 OK\\r\\nContent-Type: text/html\\r\\n\\r\\n<html><head><title>CTF Login</title></head><body><h2>Employee Login</h2><form method=POST action=/login><input name=username placeholder=\"Username\"><br><input type=password name=password placeholder=\"Password\"><br><input type=submit value=\"Login\"></form><!-- SQL: SELECT * FROM users WHERE username=\"\$username\" AND password=\"\$password\" --><p style=\"color:red\">Debug: Check /var/log/sql.log for query logs</p></body></html>'" &
echo "HTTP login decoy started on port 80"

# HTTPS (443) - SSL error that hints at certificate issues
socat TCP-LISTEN:443,fork,reuseaddr EXEC:"echo 'SSL certificate error: CN=ctf-internal.local expired'" &
echo "HTTPS decoy started on port 443"

# MySQL (3306) - Database with fake flag as bait
socat TCP-LISTEN:3306,fork,reuseaddr EXEC:"/opt/services/mysql_decoy.sh" &
echo "MySQL decoy started on port 3306"

# Web application (8080) - Advanced Flask app with fake vulnerabilities
python3 /opt/services/web_decoy.py &
echo "Web application decoy started on port 8080"

echo "All decoy services started successfully!"

# Keep container running - wait for all background processes
wait