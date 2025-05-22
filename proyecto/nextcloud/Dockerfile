FROM nextcloud:latest

RUN a2enmod ssl 

RUN a2enmod rewrite

CMD ["apache2ctl", "-D", "FOREGROUND"]
