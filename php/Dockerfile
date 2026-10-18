FROM php:8.2-apache
RUN apt-get update && apt-get install -y --no-install-recommends libcurl4-openssl-dev && docker-php-ext-install curl mysqli pdo pdo_mysql && a2enmod headers && rm -rf /var/lib/apt/lists/*
COPY . /var/www/html/