# Security Configuration Guide

This guide provides templates and examples for configuring security features in your payment gateway application.

## Environment Variables

Create a `.env.example` file (never commit actual secrets):

```bash
# Application Settings
APP_ENV=production
APP_DEBUG=false
APP_KEY=generate_with_secure_random_32_bytes

# Database Configuration
DB_CONNECTION=encrypted
DB_HOST=127.0.0.1
DB_PORT=5432
DB_DATABASE=paygate
DB_USERNAME=paygate_user
DB_PASSWORD=use_strong_password_here

# Encryption
ENCRYPTION_KEY=generate_with_secure_random_key
ENCRYPTION_ALGORITHM=aes-256-gcm

# API Keys (use secure vault in production)
PAYMENT_GATEWAY_API_KEY=your_api_key_here
PAYMENT_GATEWAY_SECRET=your_secret_here

# JWT Configuration
JWT_SECRET=generate_with_secure_random_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# Session Configuration
SESSION_LIFETIME=120
SESSION_SECURE_COOKIE=true
SESSION_HTTP_ONLY=true
SESSION_SAME_SITE=strict

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# CORS Settings
CORS_ALLOWED_ORIGINS=https://yourdomain.com
CORS_ALLOWED_METHODS=GET,POST,PUT,DELETE
CORS_ALLOWED_HEADERS=Content-Type,Authorization

# Logging
LOG_LEVEL=info
LOG_CHANNEL=stack

# Monitoring
SENTRY_DSN=your_sentry_dsn_here
NEW_RELIC_LICENSE_KEY=your_new_relic_key_here

# Security Headers
CSP_ENABLED=true
HSTS_ENABLED=true
HSTS_MAX_AGE=31536000
```

## Security Headers Configuration

### Nginx Configuration

```nginx
# /etc/nginx/conf.d/security-headers.conf

# Security Headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

# HSTS (HTTP Strict Transport Security)
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

# Content Security Policy
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self';" always;

# SSL Configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers on;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;

# Rate Limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;

# Apply rate limits to specific locations
location /api/ {
    limit_req zone=api_limit burst=20 nodelay;
}

location /auth/login {
    limit_req zone=login_limit burst=3 nodelay;
}
```

### Apache Configuration

```apache
# .htaccess or httpd.conf

# Security Headers
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-Content-Type-Options "nosniff"
Header always set X-XSS-Protection "1; mode=block"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"

# HSTS
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"

# Content Security Policy
Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"

# SSL Configuration
SSLProtocol -all +TLSv1.2 +TLSv1.3
SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
SSLHonorCipherOrder on
```

## Application Security Configuration

### Python (Flask/Django Example)

```python
# config/security.py

import os
from datetime import timedelta

class SecurityConfig:
    # Session Configuration
    SESSION_COOKIE_SECURE = True  # Only send over HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # Password Hashing
    BCRYPT_LOG_ROUNDS = 12
    
    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = "redis://localhost:6379"
    RATELIMIT_STRATEGY = "fixed-window"
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
    CORS_ALLOW_CREDENTIALS = False
    
    # Content Security Policy
    CSP = {
        'default-src': ["'self'"],
        'script-src': ["'self'"],
        'style-src': ["'self'", "'unsafe-inline'"],
        'img-src': ["'self'", "data:", "https:"],
        'font-src': ["'self'"],
        'connect-src': ["'self'"],
        'frame-ancestors': ["'none'"],
    }
    
    # Security Headers
    SECURITY_HEADERS = {
        'X-Frame-Options': 'SAMEORIGIN',
        'X-Content-Type-Options': 'nosniff',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    }
```

### Node.js (Express Example)

```javascript
// config/security.js

const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const mongoSanitize = require('express-mongo-sanitize');

module.exports = {
  // Helmet configuration for security headers
  helmetConfig: helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", "data:", "https:"],
        connectSrc: ["'self'"],
        fontSrc: ["'self'"],
        objectSrc: ["'none'"],
        mediaSrc: ["'self'"],
        frameSrc: ["'none'"],
      },
    },
    hsts: {
      maxAge: 31536000,
      includeSubDomains: true,
      preload: true,
    },
  }),

  // Rate limiting configuration
  rateLimitConfig: rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
    message: 'Too many requests from this IP, please try again later.',
  }),

  // Strict rate limit for authentication
  authRateLimitConfig: rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 5,
    skipSuccessfulRequests: true,
    message: 'Too many login attempts, please try again later.',
  }),

  // CORS configuration
  corsConfig: {
    origin: process.env.CORS_ALLOWED_ORIGINS?.split(',') || [],
    credentials: false,
    optionsSuccessStatus: 200,
  },

  // Session configuration
  sessionConfig: {
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: true, // requires HTTPS
      httpOnly: true,
      maxAge: 2 * 60 * 60 * 1000, // 2 hours
      sameSite: 'strict',
    },
  },

  // MongoDB sanitization to prevent injection
  mongoSanitizeConfig: {
    replaceWith: '_',
  },
};
```

## Database Security Configuration

### PostgreSQL

```sql
-- Create dedicated user with limited privileges
CREATE USER paygate_app WITH PASSWORD 'strong_password_here';

-- Create database
CREATE DATABASE paygate_db OWNER paygate_app;

-- Connect to database
\c paygate_db

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Grant minimal required privileges
GRANT CONNECT ON DATABASE paygate_db TO paygate_app;
GRANT USAGE ON SCHEMA public TO paygate_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO paygate_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO paygate_app;

-- Enable SSL connections (postgresql.conf)
-- ssl = on
-- ssl_cert_file = '/path/to/server.crt'
-- ssl_key_file = '/path/to/server.key'

-- Enable encrypted connections only (pg_hba.conf)
-- hostssl all all 0.0.0.0/0 md5

-- Enable audit logging (postgresql.conf)
-- log_connections = on
-- log_disconnections = on
-- log_duration = on
-- log_statement = 'ddl'
```

### MongoDB

```javascript
// MongoDB security configuration

// Create admin user
use admin
db.createUser({
  user: "admin",
  pwd: "strong_admin_password",
  roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
})

// Create application user with limited privileges
use paygate_db
db.createUser({
  user: "paygate_app",
  pwd: "strong_app_password",
  roles: [
    { role: "readWrite", db: "paygate_db" }
  ]
})

// Enable authentication (mongod.conf)
// security:
//   authorization: enabled

// Enable TLS/SSL (mongod.conf)
// net:
//   ssl:
//     mode: requireSSL
//     PEMKeyFile: /path/to/mongodb.pem
//     CAFile: /path/to/ca.pem

// Enable audit logging (mongod.conf)
// auditLog:
//   destination: file
//   format: JSON
//   path: /var/log/mongodb/audit.json
```

## Firewall Configuration

### UFW (Ubuntu)

```bash
#!/bin/bash
# firewall-setup.sh

# Reset firewall
sudo ufw --force reset

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (limit to prevent brute force)
sudo ufw limit 22/tcp

# Allow HTTPS
sudo ufw allow 443/tcp

# Allow HTTP (redirect to HTTPS in nginx/apache)
sudo ufw allow 80/tcp

# Allow database access only from application server
# Replace 10.0.0.5 with your app server IP
sudo ufw allow from 10.0.0.5 to any port 5432 proto tcp

# Enable firewall
sudo ufw --force enable

# Show status
sudo ufw status verbose
```

## Docker Security Configuration

```yaml
# docker-compose.yml (security-focused)

version: '3.8'

services:
  app:
    image: paygate-app:latest
    build:
      context: .
      dockerfile: Dockerfile
    read_only: true
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    tmpfs:
      - /tmp
    environment:
      - NODE_ENV=production
    env_file:
      - .env.production
    volumes:
      - ./logs:/app/logs:rw
    networks:
      - app-network
    restart: unless-stopped
    
  db:
    image: postgres:15-alpine
    read_only: true
    security_opt:
      - no-new-privileges:true
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - /dev/shm:/dev/shm
    tmpfs:
      - /tmp
      - /run/postgresql
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
    driver: bridge
    internal: true

volumes:
  postgres_data:
    driver: local

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## Secrets Management

### Using HashiCorp Vault

```python
# utils/vault.py

import hvac
import os

class VaultClient:
    def __init__(self):
        self.client = hvac.Client(
            url=os.getenv('VAULT_ADDR'),
            token=os.getenv('VAULT_TOKEN')
        )
    
    def get_secret(self, path):
        """Retrieve secret from Vault"""
        try:
            secret = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point='secret'
            )
            return secret['data']['data']
        except Exception as e:
            print(f"Error retrieving secret: {e}")
            return None
    
    def store_secret(self, path, secret_data):
        """Store secret in Vault"""
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=secret_data,
                mount_point='secret'
            )
            return True
        except Exception as e:
            print(f"Error storing secret: {e}")
            return False

# Usage
vault = VaultClient()
db_creds = vault.get_secret('database/credentials')
api_key = vault.get_secret('payment-gateway/api-key')
```

## Monitoring Configuration

### Prometheus Metrics

```python
# monitoring/metrics.py

from prometheus_client import Counter, Histogram, Gauge

# Security metrics
failed_login_attempts = Counter(
    'failed_login_attempts_total',
    'Total number of failed login attempts',
    ['username']
)

suspicious_transactions = Counter(
    'suspicious_transactions_total',
    'Total number of suspicious transactions detected',
    ['reason']
)

payment_processing_duration = Histogram(
    'payment_processing_duration_seconds',
    'Time spent processing payments'
)

active_sessions = Gauge(
    'active_sessions',
    'Number of active user sessions'
)

# Usage in application
def process_login(username, password):
    if not authenticate(username, password):
        failed_login_attempts.labels(username=username).inc()
        return False
    return True
```

## Backup Configuration

```bash
#!/bin/bash
# backup.sh - Secure backup script

# Configuration
BACKUP_DIR="/secure/backups"
DB_NAME="paygate_db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gpg"
RETENTION_DAYS=30

# Create encrypted backup
pg_dump -U paygate_app ${DB_NAME} | \
  gzip | \
  gpg --encrypt --recipient backup@example.com \
  > ${BACKUP_FILE}

# Verify backup was created
if [ -f "${BACKUP_FILE}" ]; then
    echo "Backup created successfully: ${BACKUP_FILE}"
    
    # Remove old backups
    find ${BACKUP_DIR} -name "*.sql.gpg" -mtime +${RETENTION_DAYS} -delete
else
    echo "Backup failed!"
    exit 1
fi

# Upload to secure storage (e.g., S3 with encryption)
aws s3 cp ${BACKUP_FILE} s3://secure-backup-bucket/ \
  --sse AES256 \
  --storage-class STANDARD_IA
```

## Regular Security Tasks

Add to crontab:

```cron
# Daily security scans at 2 AM
0 2 * * * /usr/local/bin/security-scan.sh

# Weekly dependency updates on Sundays at 3 AM
0 3 * * 0 /usr/local/bin/update-dependencies.sh

# Daily backup at 1 AM
0 1 * * * /usr/local/bin/backup.sh

# Hourly log rotation
0 * * * * /usr/sbin/logrotate /etc/logrotate.conf

# Weekly SSL certificate check
0 8 * * 1 /usr/local/bin/check-ssl-certs.sh
```

## Conclusion

This configuration guide provides templates for securing your payment gateway application. Remember to:

1. Never commit actual secrets to version control
2. Use environment-specific configurations
3. Regularly update and patch all components
4. Monitor and audit security configurations
5. Test configurations in non-production environments first
