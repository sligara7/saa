# Interface Control Document: API Gateway Service (ICD-AGW-001)

Version: 0.0
Status: Active
Last Updated: 2025-09-27

## Document Version Control

This document follows semver-date versioning (MAJOR.MINOR+YYYY-MM-DD):

- MAJOR version changes (e.g., 1.2 -> 2.0) indicate breaking changes
  * Interface modifications
  * Removed endpoints/fields
  * Changed request/response formats
  * Protocol changes
  * MUST add a new dated entry to changelog with [BREAKING] prefix

- MINOR version changes (e.g., 1.2 -> 1.3) indicate backward-compatible changes
  * Added endpoints/fields
  * Enhanced documentation
  * Clarifications
  * Non-breaking changes
  * MUST add a new dated entry to changelog

- Date suffix is updated for ALL changes, including formatting
  * Pure formatting changes only update date, not version
  * DO NOT add changelog entry for formatting-only changes

Example: Version 1.2+2025-09-27

## Changelog

_No changes recorded yet - document initialized at version 0.0+2025-09-27_


## Document Version Control

This document follows semver-date versioning (MAJOR.MINOR+YYYY-MM-DD):

- MAJOR version changes indicate breaking changes
  * Interface modifications
  * Removed endpoints/fields
  * Changed request/response formats
  * Protocol changes

- MINOR version changes indicate backward-compatible changes
  * Added endpoints/fields
  * Enhanced documentation
  * Clarifications
  * Non-breaking changes

- Date suffix is updated for ALL changes, including formatting

Example: Version 1.2+2025-09-27


## Document Version Control

This document follows semver-date versioning (MAJOR.MINOR+YYYY-MM-DD):

- MAJOR version changes indicate breaking changes
  * Interface modifications
  * Removed endpoints/fields
  * Changed request/response formats
  * Protocol changes

- MINOR version changes indicate backward-compatible changes
  * Added endpoints/fields
  * Enhanced documentation
  * Clarifications
  * Non-breaking changes

- Date suffix is updated for ALL changes, including formatting

Example: Version 1.2+2025-09-27

## 1. Interface Overview

### 1.1 Purpose
This document defines all interfaces for the API Gateway Service, which provides a unified entry point for external API requests to the XRPL LP Optimization System.

### 1.2 Interface Summary
| Interface | Type | Protocol | Purpose |
|-----------|------|----------|----------|
| REST API | External | HTTPS | Client API access |
| Admin API | Internal | HTTPS | Gateway management |
| Service Discovery | Internal | gRPC | Service routing |
| Metrics | Internal | Prometheus | System monitoring |

## 2. REST API Interface

### 2.1 Common Request Headers
```http
Authorization: Bearer {token}
X-API-Key: {api_key}
X-Request-ID: {uuid}
X-Client-Version: {version}
Content-Type: application/json
Accept: application/json
```

### 2.2 Common Response Headers
```http
X-Request-ID: {uuid}
X-RateLimit-Limit: {limit}
X-RateLimit-Remaining: {remaining}
X-RateLimit-Reset: {timestamp}
Content-Type: application/json
```

### 2.3 Standard Error Format
```json
{
    "error": {
        "code": string,
        "message": string,
        "details": object|null,
        "request_id": string
    },
    "timestamp": string
}
```

### 2.4 Rate Limiting
```typescript
interface RateLimit {
    window_size: number;    // seconds
    max_requests: number;   // per window
    burst_size: number;     // additional burst allowance
    user_type: string;     // determines limits
}
```

## 3. Route Configuration Interface

### 3.1 Route Definition
```yaml
routes:
  - path: /api/v1/pools/*
    service: lp_discovery_service
    methods: [GET, POST]
    auth:
      required: true
      scopes: [pools.read, pools.write]
    rate_limit:
      requests_per_second: 10
      burst: 20
    timeout: 30s
    retry:
      attempts: 3
      backoff: exponential

  - path: /api/v1/portfolio/*
    service: lp_portfolio_service
    methods: [GET, POST, PUT, DELETE]
    auth:
      required: true
      scopes: [portfolio.manage]
    rate_limit:
      requests_per_second: 5
      burst: 10
    timeout: 60s
```

### 3.2 Service Discovery Configuration
```yaml
discovery:
  type: kubernetes
  settings:
    namespace: default
    label_selector: app.kubernetes.io/name
    port_name: http
  health_check:
    path: /health
    interval: 10s
    timeout: 5s
    success_threshold: 1
    failure_threshold: 3
```

## 4. Admin API Interface

### 4.1 Route Management
```http
POST /admin/v1/routes
Content-Type: application/json

Request:
{
    "path": string,
    "service": string,
    "methods": string[],
    "auth": {
        "required": boolean,
        "scopes": string[]
    },
    "rate_limit": {
        "requests_per_second": number,
        "burst": number
    },
    "timeout": string,
    "retry": {
        "attempts": number,
        "backoff": string
    }
}

Response:
{
    "route_id": string,
    "status": "active",
    "created_at": string
}
```

### 4.2 Key Management
```http
POST /admin/v1/api-keys
Content-Type: application/json

Request:
{
    "name": string,
    "scopes": string[],
    "rate_limit": {
        "requests_per_second": number,
        "burst": number
    },
    "expires_at": string
}

Response:
{
    "key_id": string,
    "api_key": string,
    "created_at": string,
    "expires_at": string
}
```

## 5. Service Discovery Interface

### 5.1 Service Registration
```protobuf
service ServiceRegistry {
    rpc Register(ServiceInfo) returns (RegistrationResponse);
    rpc Deregister(ServiceId) returns (DeregistrationResponse);
    rpc GetService(ServiceQuery) returns (ServiceInfo);
    rpc WatchServices(ServiceQuery) returns (stream ServiceUpdate);
}

message ServiceInfo {
    string service_id = 1;
    string name = 2;
    string version = 3;
    repeated Endpoint endpoints = 4;
    map<string, string> metadata = 5;
    HealthStatus health = 6;
}
```

### 5.2 Health Check
```protobuf
message HealthCheck {
    string service_id = 1;
    Status status = 2;
    string message = 3;
    map<string, Status> components = 4;
}

enum Status {
    UNKNOWN = 0;
    HEALTHY = 1;
    DEGRADED = 2;
    UNHEALTHY = 3;
}
```

## 6. Metrics Interface

### 6.1 Prometheus Metrics
```
# Request Metrics
api_requests_total{method="*",path="*",status="*"} counter
api_request_duration_seconds{method="*",path="*"} histogram
api_request_size_bytes{method="*",path="*"} histogram
api_response_size_bytes{method="*",path="*"} histogram

# Rate Limiting Metrics
api_rate_limit_exceeded_total{client_id="*"} counter
api_rate_limit_remaining{client_id="*"} gauge

# Auth Metrics
api_auth_failures_total{type="*"} counter
api_auth_latency_seconds histogram

# Routing Metrics
api_route_lookup_duration_seconds histogram
api_route_errors_total{service="*"} counter
```

### 6.2 Service Metrics
```
# Service Health
service_health_status{service="*"} gauge
service_response_time_seconds{service="*"} histogram
service_errors_total{service="*"} counter

# Circuit Breaker
circuit_breaker_state{service="*"} gauge
circuit_breaker_failures_total{service="*"} counter
```

## 7. Security

### 7.1 Authentication Methods
```yaml
auth_methods:
  - type: api_key
    header: X-API-Key
    validation: hmac
    
  - type: jwt
    header: Authorization
    schema: Bearer
    issuer: auth0
    
  - type: mtls
    client_ca: /etc/certs/client-ca.crt
    verify: true
```

### 7.2 Authorization Scopes
```yaml
scopes:
  - name: pools.read
    description: Read pool information
    methods: [GET]
    paths: [/api/v1/pools/*]
    
  - name: pools.write
    description: Modify pool settings
    methods: [POST, PUT, DELETE]
    paths: [/api/v1/pools/*]
    
  - name: portfolio.manage
    description: Manage portfolios
    methods: [GET, POST, PUT, DELETE]
    paths: [/api/v1/portfolio/*]
```

## 8. Circuit Breaker

### 8.1 Circuit Configuration
```typescript
interface CircuitBreaker {
    failure_threshold: number;    // 5 failures
    success_threshold: number;    // 3 successes
    timeout: number;             // 30 seconds
    half_open_timeout: number;   // 5 seconds
}
```

### 8.2 Fallback Behavior
```typescript
interface Fallback {
    type: "static" | "cache" | "degraded";
    ttl: number;
    response: {
        status: number;
        body: object;
    };
}
```

## 9. Cache Control

### 9.1 Cache Configuration
```yaml
cache:
  backend: redis
  default_ttl: 300
  max_size: 1000000
  strategies:
    - pattern: /api/v1/pools/list
      ttl: 60
      vary: [Accept-Encoding, Authorization]
    - pattern: /api/v1/metrics/*
      ttl: 300
      vary: [Accept-Encoding]
```

### 9.2 Cache Headers
```http
Cache-Control: public, max-age=300
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
Vary: Accept-Encoding, Authorization
```

## 10. Integration Patterns

### 10.1 Request Pattern
```typescript
interface RequestPattern {
    timeout: number;
    retry: {
        max_attempts: number;
        backoff: "fixed" | "exponential";
        initial_delay: number;
    };
    circuit_breaker: CircuitBreaker;
    fallback: Fallback;
}
```

### 10.2 Response Pattern
```typescript
interface ResponsePattern {
    transform: boolean;
    compress: boolean;
    cache: boolean;
    cors: CORSConfig;
    headers: Record<string, string>;
}
```

## 11. Versioning

### 11.1 API Versioning
- Version in URL path: /v1/
- Version header: X-API-Version
- Accept header: application/vnd.api.v1+json

### 11.2 Service Versioning
- Service version header: X-Service-Version
- Minimum version header: X-Min-Version
- Version negotiation in service discovery
