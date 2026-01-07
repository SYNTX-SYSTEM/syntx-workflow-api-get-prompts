# ═══════════════════════════════════════════════════════════════════════════════
#  💎 SYNTX SYSTEM - NGINX RESONANZ-ROUTER
#  Domain: dev.syntx-system.com
#  Purpose: Field-based API routing - All streams flow here
# ═══════════════════════════════════════════════════════════════════════════════

server {
    listen 443 ssl;
    server_name dev.syntx-system.com;

    ssl_certificate /etc/letsencrypt/live/dev.syntx-system.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dev.syntx-system.com/privkey.pem;

    # ───────────────────────────────────────────────────────────────────────────
    #  🔥 SYNTX INJECTOR API (Port 8001) - Core Field Resonance
    # ───────────────────────────────────────────────────────────────────────────

    # Chat Interface - Direct LLM Communication
    location /api/chat {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 1600s;
        proxy_send_timeout 1600s;
        proxy_read_timeout 1600s;
    }

    # Resonanz API - Wrappers, Formats, Styles, Stats
    location /resonanz/ {
        proxy_pass http://127.0.0.1:8001/resonanz/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 1600s;
        proxy_send_timeout 1600s;
        proxy_read_timeout 1600s;
    }

    # Profiles API - Pattern Analytics, Usage Stats, System Consciousness
    location /profiles/ {
        proxy_pass http://127.0.0.1:8001/profiles/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # ───────────────────────────────────────────────────────────────────────────
    #  🌊 STROM-ORCHESTRATOR API (Port 8020) - Generation & Calibration
    # ───────────────────────────────────────────────────────────────────────────

    location /api/strom/ {
        rewrite ^/api/strom/(.*) /$1 break;
        proxy_pass http://127.0.0.1:8020;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # ───────────────────────────────────────────────────────────────────────────
    #  ⚡ GENERATOR API (Port 8040) - Prompt Generation
    # ───────────────────────────────────────────────────────────────────────────

    location /api/generator/v1/ {
        proxy_pass http://127.0.0.1:8040/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # ───────────────────────────────────────────────────────────────────────────
    #  🌊 LEGACY BACKEND (External Server) - Old API
    # ───────────────────────────────────────────────────────────────────────────

    location /api/ {
        proxy_pass http://49.13.3.21:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 800s;
        proxy_send_timeout 800s;
        proxy_read_timeout 800s;
    }

    # ───────────────────────────────────────────────────────────────────────────
    #  📊 STATIC CONTENT - Documentation & Logs
    # ───────────────────────────────────────────────────────────────────────────

    # API Documentation
    location /docs/ {
        alias /var/www/syntx-api-docs/;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # Root Redirect
    location = / {
        return 302 /docs/;
    }

    # Training Data Logs (Protected)
    location /logs/ {
        alias /opt/syntx-config/logs/;
        autoindex on;
        auth_basic "SYNTX Training Data - Protected";
        auth_basic_user_file /etc/nginx/.htpasswd;
        limit_except GET { deny all; }
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
#  🔒 HTTP → HTTPS REDIRECT
# ═══════════════════════════════════════════════════════════════════════════════

server {
    listen 80;
    server_name dev.syntx-system.com;
    return 301 https://$server_name$request_uri;
}
