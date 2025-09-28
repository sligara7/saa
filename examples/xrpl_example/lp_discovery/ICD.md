# Interface Control Document: LP Discovery Service (ICD-LPD-001)

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


## 1. Introduction

### 1.1 Purpose
This document defines all interfaces exposed by and consumed by the LP Discovery Service.

### 1.2 Scope
Covers:
- REST API endpoints
- Message bus interfaces
- Service dependencies
- Data formats

## 2. Interface Overview

### 2.1 External Interfaces

#### 2.1.1 REST API
Base URL: `/api/v1`
Authentication: API Key (X-API-Key header)

Endpoints:

1. Pool Discovery
   ```
   GET /pools
   GET /pools/{pool_id}
   GET /pools/search
   ```

2. Pool Metrics
   ```
   GET /pools/{pool_id}/metrics
   GET /pools/{pool_id}/metrics/history
   GET /pools/{pool_id}/depth
   ```

3. Pool Scoring
   ```
   GET /pools/{pool_id}/score
   GET /pools/scores
   GET /pools/{pool_id}/score/history
   ```

4. Health
   ```
   GET /health
   GET /health/live
   GET /health/ready
   ```

### 2.2 Message Bus Interfaces

#### 2.2.1 Published Events
- `pool.discovered`: New pool found
- `pool.updated`: Pool status change
- `metrics.collected`: New metrics available
- `score.updated`: Score calculation complete
- `score.failed`: Score calculation error

#### 2.2.2 Consumed Events
- `xrpl.ledger.closed`: New ledger closed
- `xrpl.amm.updated`: AMM state change
- `database.pool.updated`: Pool data updated

## 3. Data Formats

### 3.1 Pool Object
```json
{
  "pool_id": "string",
  "asset_a": {
    "currency": "string",
    "issuer": "string",
    "type": "XRP|TOKEN|NFT"
  },
  "asset_b": {
    "currency": "string",
    "issuer": "string",
    "type": "XRP|TOKEN|NFT"
  },
  "status": "ACTIVE|INACTIVE|FROZEN",
  "pool_type": "STABLE|VOLATILE|EXOTIC",
  "trading_fee": "decimal",
  "total_lp_tokens": "decimal",
  "lp_count": "integer",
  "created_at": "ISO8601"
}
```

### 3.2 Pool Score
```json
{
  "pool_id": "string",
  "total_score": "decimal",
  "components": {
    "volume": "decimal",
    "fee": "decimal",
    "stability": "decimal",
    "depth": "decimal",
    "risk": "decimal"
  },
  "confidence": "HIGH|MEDIUM|LOW",
  "timestamp": "ISO8601"
}
```

### 3.3 Pool Metrics
```json
{
  "pool_id": "string",
  "tvl_xrp": "decimal",
  "volume_24h_xrp": "decimal",
  "trades_24h": "integer",
  "price": "decimal",
  "price_24h_high": "decimal",
  "price_24h_low": "decimal",
  "volatility_24h": "decimal",
  "fee_rate": "decimal",
  "fee_revenue_24h": "decimal"
}
```

## 4. Service Dependencies

### 4.1 Required Services
1. XRPL Service
   - Endpoint: `/api/v1`
   - Authentication: Service-to-service JWT

2. Database Service
   - Message bus: `database.*`
   - Authentication: Service identity

3. Message Bus Service
   - AMQP connection
   - Authentication: Service credentials

4. Metrics Service
   - Prometheus endpoint: `/metrics`
   - No authentication required

### 4.2 Optional Services
1. API Gateway Service
   - For external request routing
   - Rate limiting and authentication

## 5. Error Handling

### 5.1 HTTP Error Codes
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Error
- 503: Service Unavailable

### 5.2 Error Response Format
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

## 6. Rate Limits

### 6.1 API Rate Limits
- Default: 1000 requests/minute
- Bulk operations: 100 requests/minute
- Historical data: 50 requests/minute

### 6.2 Message Bus Limits
- Publishing: 1000 messages/second
- Consuming: 2000 messages/second
- Max message size: 1MB

## 7. Security

### 7.1 Authentication
- API Key for external requests
- JWT for service-to-service
- TLS 1.3 required

### 7.2 Authorization
- Role-based access control
- Scope-based permissions
- Rate limit tiers

---

## Document History
- 2025-08-29: Initial version
- 2025-09-20: Added Pool Scoring interfaces
