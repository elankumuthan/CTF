FROM alpine:latest

# Install only what we need for decoys
RUN apk update && \
    apk add --no-cache socat py3-flask bash

# Set up working directory
WORKDIR /opt

# Copy service scripts
COPY services/ /opt/services/
COPY entrypoint.sh /entrypoint.sh

# Make scripts executable
RUN chmod +x /entrypoint.sh
RUN chmod +x /opt/services/*.sh
RUN chmod +x /opt/services/*.py

# Create log directory
RUN mkdir -p /var/log/ctf-decoys

# Expose the ports we actually use
EXPOSE 21 22 80 443 3306 8080

CMD ["/entrypoint.sh"]