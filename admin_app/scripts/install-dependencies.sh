#!/bin/bash
# -------------------------------------------------------------------------------------------------
#   Admin App (PHP) Installation Script
# -------------------------------------------------------------------------------------------------
# PHP
php -v || log "fatal" "PHP installation failed"
log "success" "PHP installation successful"

# Composer
export COMPOSER_ALLOW_SUPERUSER=1
curl -sS https://getcomposer.org/installer | php
mv composer.phar /usr/local/bin/composer
composer --version || log "fatal" "Composer installation failed"
log "success" "Composer installation successful"

# Create Laravel project (already done)
# composer create-project laravel/laravel admin-app
cd admin-app

# Install dependencies
composer install || log "fatal" "Composer installation failed"
log "success" "Composer installation successful"

# Configure .env
# + change SESSION_DRIVER to file, CACHE_DRIVER to file, and comment out 
cp .env.example .env
php artisan key:generate


php artisan config:clear
php artisan cache:clear
php artisan route:clear
php artisan view:clear
php artisan optimize:clear


php artisan serve --host=0.0.0.0 --port=8000