# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory inside the Flask app
WORKDIR /app

# Add non-root user BEFORE copying files
RUN adduser --disabled-password --gecos "" ey_user123

# Install system dependencies and tools
RUN apt update && \
    apt install -y net-tools iproute2 lsof curl passwd openssl nodejs npm && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Set root password (for CTF realism)
RUN echo 'root:toor' | chpasswd

# Install vulnerable JWT lib
RUN npm install -g jwt-simple@0.3.0

# Copy the entire project into the container
COPY . /app

# Set root ownership first
RUN chown -R root:root /app

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Create logs folder with full access
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Ensure DB files exist and have proper perms
RUN mkdir -p /app/utils && \
    touch /app/utils/users.db /app/utils/comments.db && \
    chmod -R 777 /app/utils


# Initialize database
RUN python3 /app/utils/clear_db.py && \
    python3 /app/utils/init_db.py

# Add fake bash history
COPY utils/bash_history_custom /home/ey_user123/.bash_history
RUN chown ey_user123:ey_user123 /home/ey_user123/.bash_history

# Copy public key and leaked DB
COPY utils/public.pem /home/ey_user123/
COPY utils/database_to_leak.db /home/ey_user123/database.db
RUN chown ey_user123:ey_user123 /home/ey_user123/public.pem /home/ey_user123/database.db

# Final fix for uploads ownership
RUN chown -R ey_user123:ey_user123 /app/uploads

# Switch to non-root user
USER ey_user123

# Expose Flask port
EXPOSE 80

# Run Flask app
CMD ["python3", "-u", "app.py"]
