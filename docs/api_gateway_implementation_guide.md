# API Gateway (Traefik) Implementation Guide

## Overview

The API Gateway serves as the single entry point for all client requests in the D&D Character Creator system. Using Traefik, it provides routing, load balancing, TLS termination, and security features for all backend services.

## Tech Stack

- **Gateway**: Traefik v2.x
- **TLS**: Let's Encrypt for automatic certificate management
- **Authentication**: JWT validation middleware
- **Metrics**: Prometheus/Grafana
- **Service Discovery**: Docker/Podman label-based
- **Load Balancing**: Built-in Traefik algorithms
- **Caching**: Redis for rate limiting state
- **Monitoring**: Traefik dashboard and metrics

## Project Structure

```
api_gateway/
├── config/
│   ├── dynamic/                     # Dynamic configuration
│   │   ├── middlewares.yml         # Middleware configurations
│   │   ├── routers.yml            # Router configurations
│   │   └── services.yml           # Service configurations
│   └── traefik.yml                # Static configuration
├── certs/                         # TLS certificates
│   ├── acme.json                 # Let's Encrypt storage
│   └── custom/                   # Custom certificates
├── middleware/                    # Custom middleware
│   ├── auth/                     # Authentication middleware
│   └── ratelimit/                # Rate limiting middleware
└── scripts/                      # Management scripts
    ├── setup.sh                 # Gateway setup
    └── renew-certs.sh          # Certificate renewal
```

## Core Configuration

### Static Configuration (traefik.yml)
```yaml
# Basic configuration
global:
  checkNewVersion: true
  sendAnonymousUsage: false

# Enable Traefik API and dashboard
api:
  dashboard: true
  insecure: false  # Secure in production

# Entry points configuration
entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
  websecure:
    address: ":443"
    http:
      tls:
        certResolver: letsencrypt

# Certificate resolvers
certificatesResolvers:
  letsencrypt:
    acme:
      email: admin@example.com
      storage: /etc/traefik/certs/acme.json
      httpChallenge:
        entryPoint: web

# Providers configuration
providers:
  docker:
    endpoint: "unix:///var/run/podman.sock"
    exposedByDefault: false
    watch: true
  file:
    directory: /etc/traefik/dynamic
    watch: true

# Metrics configuration
metrics:
  prometheus:
    entryPoint: metrics
    addServicesLabels: true
    addEntryPointsLabels: true
    buckets: [0.1, 0.3, 1.2, 5.0]

# Access logs
accessLog:
  filePath: "/var/log/traefik/access.log"
  bufferingSize: 100
```

### Dynamic Configuration (dynamic/middlewares.yml)
```yaml
http:
  middlewares:
    # CORS middleware
    cors:
      headers:
        accessControlAllowMethods:
          - GET
          - POST
          - PUT
          - DELETE
          - OPTIONS
        accessControlAllowHeaders:
          - Authorization
          - Content-Type
        accessControlAllowOriginList:
          - "https://app.example.com"
        accessControlMaxAge: 100

    # Rate limiting middleware
    rate-limit:
      rateLimit:
        average: 100
        burst: 50
        period: 1m

    # Security headers middleware
    secure-headers:
      headers:
        stsSeconds: 31536000
        browserXssFilter: true
        contentTypeNosniff: true
        forceSTSHeader: true
        stsIncludeSubdomains: true
        stsPreload: true
        customFrameOptionsValue: SAMEORIGIN
        contentSecurityPolicy: "frame-ancestors 'self'"

    # Authentication middleware
    jwt-auth:
      forwardAuth:
        address: "http://auth-service:8300/validate"
        trustForwardHeader: true
        authResponseHeaders:
          - X-User-ID
          - X-User-Role
```

### Service Configuration (dynamic/services.yml)
```yaml
http:
  services:
    character-service:
      loadBalancer:
        servers:
          - url: "http://character-service:8000"
        healthCheck:
          path: /health
          interval: "10s"
          timeout: "3s"

    campaign-service:
      loadBalancer:
        servers:
          - url: "http://campaign-service:8001"
        healthCheck:
          path: /health
          interval: "10s"
          timeout: "3s"

    image-service:
      loadBalancer:
        servers:
          - url: "http://image-service:8002"
        healthCheck:
          path: /health
          interval: "10s"
          timeout: "3s"

    llm-service:
      loadBalancer:
        servers:
          - url: "http://llm-service:8100"
        healthCheck:
          path: /health
          interval: "10s"
          timeout: "3s"

    message-hub:
      loadBalancer:
        servers:
          - url: "http://message-hub:8200"
        healthCheck:
          path: /health
          interval: "10s"
          timeout: "3s"
```

### Router Configuration (dynamic/routers.yml)
```yaml
http:
  routers:
    character-service:
      rule: "PathPrefix(`/api/v1/characters`)"
      service: "character-service"
      middlewares:
        - "cors"
        - "rate-limit"
        - "secure-headers"
        - "jwt-auth"
      tls: {}

    campaign-service:
      rule: "PathPrefix(`/api/v1/campaigns`)"
      service: "campaign-service"
      middlewares:
        - "cors"
        - "rate-limit"
        - "secure-headers"
        - "jwt-auth"
      tls: {}

    image-service:
      rule: "PathPrefix(`/api/v1/images`)"
      service: "image-service"
      middlewares:
        - "cors"
        - "rate-limit"
        - "secure-headers"
        - "jwt-auth"
      tls: {}

    llm-service:
      rule: "PathPrefix(`/api/v1/generate`)"
      service: "llm-service"
      middlewares:
        - "cors"
        - "rate-limit"
        - "secure-headers"
        - "jwt-auth"
      tls: {}

    message-hub:
      rule: "PathPrefix(`/api/v1/messages`)"
      service: "message-hub"
      middlewares:
        - "cors"
        - "rate-limit"
        - "secure-headers"
        - "jwt-auth"
      tls: {}
```

## Service Integration

### Container Labels

Services must include these labels for Traefik integration:

```yaml
# Character Service example
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.character.rule=PathPrefix(`/api/v1/characters`)"
  - "traefik.http.services.character.loadbalancer.server.port=8000"
  - "traefik.http.services.character.loadbalancer.healthcheck.path=/health"
  - "traefik.http.middlewares.character-strip.stripprefix.prefixes=/api/v1/characters"
```

### Health Checking

Services must implement health check endpoints:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }
```

## Setup and Development

### Local Development Setup

1. Create required directories:
```bash
mkdir -p config/dynamic certs/custom
```

2. Create configuration files:
```bash
# Create static config
cat > config/traefik.yml << EOF
# Basic traefik config for development
EOF

# Create dynamic configs
cat > config/dynamic/middlewares.yml << EOF
# Middleware configurations
EOF
```

3. Start Traefik:
```bash
podman run -d \
  --name traefik \
  -p 80:80 \
  -p 443:443 \
  -p 8080:8080 \
  -v $PWD/config:/etc/traefik \
  -v $PWD/certs:/etc/certs \
  -v /var/run/podman.sock:/var/run/docker.sock \
  traefik:v2.9
```

### Environment Variables

Required environment variables:
- `TRAEFIK_LOG_LEVEL` - Log level (default: INFO)
- `TRAEFIK_ACME_EMAIL` - Let's Encrypt email
- `TRAEFIK_AUTH_TOKEN` - Dashboard auth token

Optional environment variables:
- `TRAEFIK_PILOT_TOKEN` - Traefik Pilot token
- `TRAEFIK_METRICS_PORT` - Metrics port (default: 8082)
- `TRAEFIK_DASHBOARD_PORT` - Dashboard port (default: 8080)

## Monitoring

### Prometheus Integration

Metrics endpoint configuration:
```yaml
metrics:
  prometheus:
    entryPoint: metrics
    addServicesLabels: true
    addEntryPointsLabels: true
    buckets:
      - 0.1
      - 0.3
      - 1.2
      - 5.0
```

### Dashboard Access

Secure dashboard configuration:
```yaml
api:
  dashboard: true
  insecure: false
  middlewares:
    - auth-middleware

http:
  middlewares:
    auth-middleware:
      basicAuth:
        users:
          - "admin:$apr1$H6uskkkW$IgXLP6ewTrSuBkTrqE8wj/"
```

### Logging Configuration

Access log configuration:
```yaml
accessLog:
  filePath: "/var/log/traefik/access.log"
  format: json
  fields:
    defaultMode: keep
    headers:
      defaultMode: drop
```

## Security Features

### TLS Configuration

Production TLS settings:
```yaml
tls:
  options:
    default:
      minVersion: "VersionTLS12"
      cipherSuites:
        - "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384"
        - "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"
        - "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305"
        - "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305"
        - "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256"
        - "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
      curvePreferences:
        - "CurveP521"
        - "CurveP384"
      sniStrict: true
```

### Security Headers

Security header middleware:
```yaml
http:
  middlewares:
    secure-headers:
      headers:
        stsSeconds: 31536000
        browserXssFilter: true
        contentTypeNosniff: true
        forceSTSHeader: true
        stsIncludeSubdomains: true
        stsPreload: true
        customFrameOptionsValue: SAMEORIGIN
        contentSecurityPolicy: "frame-ancestors 'self'"
```

## Troubleshooting

### Common Issues

1. Routing Issues
   - Check service labels
   - Verify router rules
   - Review middleware chain
   - Check service health

2. TLS Issues
   - Verify ACME setup
   - Check certificate paths
   - Review TLS options
   - Monitor certificate renewal

3. Performance Issues
   - Monitor request latency
   - Check error rates
   - Review access logs
   - Analyze metrics

### Debugging

1. Enable debug logging:
```yaml
log:
  level: DEBUG
  format: json
```

2. Check logs:
```bash
podman logs traefik
```

3. Review access logs:
```bash
tail -f /var/log/traefik/access.log
```

4. Check Traefik status:
```bash
curl http://localhost:8080/api/overview
```

## Future Improvements

1. Performance Optimizations
   - Enhanced caching
   - Request buffering
   - Response compression
   - Circuit breaking

2. Feature Enhancements
   - Service mesh integration
   - Advanced rate limiting
   - Request transformation
   - Response modification

3. Technical Improvements
   - Enhanced monitoring
   - Automated failover
   - Dynamic configuration
   - Advanced load balancing