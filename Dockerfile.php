FROM php:7.4-apache

# Copy uploads (shell.php ends up here)
COPY uploads/ /var/www/html/

# Set permissions
RUN chown -R www-data:www-data /var/www/html && \
    chmod -R 755 /var/www/html
