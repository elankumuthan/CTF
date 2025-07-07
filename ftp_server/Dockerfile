FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y vsftpd zip unzip

# Fix for vsftpd secure chroot dir error
RUN mkdir -p /var/run/vsftpd/empty && chmod 755 /var/run/vsftpd/empty

# Add ftp user
RUN useradd -m ftpuser && echo "ftpuser:ftp123" | chpasswd && \
    mkdir -p /srv/ftp && chmod 755 /srv/ftp && \
    mkdir -p /home/ftpuser/ftp && chmod 755 /home/ftpuser/ftp

COPY vsftpd.conf /etc/vsftpd.conf
COPY startup.sh /usr/local/bin/startup.sh
COPY ftp_files/ /srv/ftp/

RUN chmod +x /usr/local/bin/startup.sh

EXPOSE 20 21 10000-10100

CMD ["/usr/local/bin/startup.sh"]
