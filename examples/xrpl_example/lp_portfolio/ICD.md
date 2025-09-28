# Interface Control Document: LP Portfolio Service (ICD-LPP-001)

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


## 1. Interface Overview

### 1.1 Purpose
This document defines all internal interfaces for the LP Portfolio Service, ensuring compatibility and interoperability with other system components. This service is not directly exposed externally - all public access is routed through the API Gateway.

### 1.2 Interface Summary
| Interface | Type | Protocol | Purpose |
|-----------|------|----------|----------|
| gRPC API | Internal | HTTP/2 | Portfolio management |
| Message Bus | Internal | AMQP | Event communication |
| Metrics | Internal | Prometheus | System monitoring |
| Health | Internal | HTTPS | Service health checks |

## 2. REST API Interface

### 2.1 Endpoint
```
grpc://{service}/v1/portfolio
```

### 2.2 Authentication
- Mutual TLS authentication between services
- Internal service tokens for authorization
- Trust organization ID from API Gateway headers

### 2.3 Endpoints

#### 2.3.1 Portfolio Management
```http
POST /portfolios/create
Content-Type: application/json

Request:
{
    "name": string,
    "strategy_id": string,
    "risk_profile": {
        "max_il_tolerance": decimal,
        "concentration_limit": decimal,
        "min_liquidity": decimal
    },
    "allocation_limits": {
        "min_position": decimal,
        "max_position": decimal,
        "target_positions": integer
    }
}

Response:
{
    "portfolio_id": string,
    "status": string,
    "creation_time": string
}
```

#### 2.3.2 Position Management
```http
POST /positions/open
Content-Type: application/json

Request:
{
    "portfolio_id": string,
    "pool_id": string,
    "size": decimal,
    "entry_config": {
        "max_slippage": decimal,
        "timeout": integer,
        "fee_limit": decimal
    }
}

Response:
{
    "position_id": string,
    "status": string,
    "execution_details": {
        "entry_price": decimal,
        "executed_size": decimal,
        "fees_paid": decimal,
        "timestamp": string
    }
}
```

#### 2.3.3 Performance Analytics
```http
GET /portfolios/{portfolio_id}/performance?timeframe=string

Response:
{
    "portfolio_id": string,
    "metrics": {
        "total_value": decimal,
        "total_pnl": decimal,
        "il_exposure": decimal,
        "fee_revenue": decimal,
        "roi": decimal
    },
    "positions": [
        {
            "position_id": string,
            "pool_id": string,
            "metrics": {
                "value": decimal,
                "pnl": decimal,
                "il": decimal,
                "fees": decimal
            }
        }
    ],
    "timestamp": string
}
```

## 3. Message Bus Interface

### 3.1 Events Published

#### 3.1.1 Portfolio Events
```protobuf
message PortfolioUpdate {
    string portfolio_id = 1;
    double total_value = 2;
    double total_pnl = 3;
    double il_exposure = 4;
    string timestamp = 5;
}

message PositionUpdate {
    string position_id = 1;
    string portfolio_id = 2;
    string pool_id = 3;
    double size = 4;
    double value = 5;
    string status = 6;
    string timestamp = 7;
}
```

#### 3.1.2 Risk Events
```protobuf
message RiskAlert {
    string portfolio_id = 1;
    string alert_type = 2;
    string severity = 3;
    map<string, double> metrics = 4;
    string timestamp = 5;
}

message RebalanceRequired {
    string portfolio_id = 1;
    repeated PositionAdjustment adjustments = 2;
    string reason = 3;
    string timestamp = 4;
}

message PositionAdjustment {
    string position_id = 1;
    double current_size = 2;
    double target_size = 3;
    string reason = 4;
}
```

### 3.2 Events Consumed

#### 3.2.1 Market Events
```protobuf
message PoolUpdate {
    string pool_id = 1;
    double volume_24h = 2;
    double tvl = 3;
    double score = 4;
    string timestamp = 5;
}

message PoolRiskUpdate {
    string pool_id = 1;
    double il_risk = 2;
    double volatility = 3;
    double correlation = 4;
    string timestamp = 5;
}
```

## 4. Metrics Interface

### 4.1 Prometheus Metrics
```
# Portfolio Metrics
portfolio_total_value{portfolio_id="*"} gauge
portfolio_position_count{portfolio_id="*"} gauge
portfolio_il_exposure{portfolio_id="*"} gauge
portfolio_fee_revenue{portfolio_id="*"} counter

# Position Metrics
position_value{position_id="*",pool_id="*"} gauge
position_pnl{position_id="*",pool_id="*"} gauge
position_il{position_id="*",pool_id="*"} gauge
position_fees{position_id="*",pool_id="*"} counter

# Performance Metrics
strategy_execution_duration_seconds histogram
position_update_duration_seconds histogram
risk_calculation_duration_seconds histogram
```

### 4.2 Health Check
```http
GET /health

Response:
{
    "status": "up|down|degraded",
    "components": {
        "strategy_engine": "up|down",
        "risk_calculator": "up|down",
        "position_manager": "up|down"
    },
    "version": string,
    "timestamp": string
}
```

## 5. Data Formats

### 5.1 Pool Configuration
```yaml
name: "TOKEN/XRP"        # Pool name/identifier
url: "https://..."       # Source URL
issuer: "r..."           # Token issuer address
metrics:                 # Real-time metrics
  tvl: 0                 # Total Value Locked (XRP)
  volume_24h: 0          # 24h Volume (XRP)
  apr: 0.0              # Annual Percentage Rate (%)
  fees_24h: 0           # 24h Fees (XRP)
  lp_tokens: 0          # Total LP Tokens
  contributors: 0       # Number of Contributors
```

### 5.2 Common Types
```typescript
type Decimal = string;  // Decimal numbers as strings
type Timestamp = string;  // ISO-8601 in UTC
type PositionID = string;  // UUID v4
type PortfolioID = string;  // UUID v4
```

### 5.2 Error Format
```json
{
    "error": {
        "code": string,
        "message": string,
        "details": object|null,
        "retry_after": integer|null
    },
    "request_id": string,
    "timestamp": string
}
```

## 6. Service Level Objectives

### 6.1 Performance SLOs
- API Latency: p99 < 100ms
- Position Updates: p99 < 1s
- Strategy Execution: p99 < 5s
- Event Processing: p99 < 500ms

### 6.2 Reliability SLOs
- Service Availability: 99.99%
- Data Accuracy: 99.999%
- Event Delivery: 99.99%

## 7. Integration Patterns

### 7.1 Circuit Breaker
```typescript
interface CircuitBreaker {
    failure_threshold: number;    // 5 failures
    reset_timeout: number;        // 30 seconds
    half_open_timeout: number;    // 5 seconds
}
```

### 7.2 Retry Policy
```typescript
interface RetryPolicy {
    max_attempts: number;         // 3 attempts
    initial_delay: number;        // 1 second
    max_delay: number;           // 5 seconds
    backoff_multiplier: number;  // 2.0
}
```

### 7.3 Rate Limiting
```typescript
interface RateLimit {
    requests_per_second: number;  // 50 requests
    burst_size: number;          // 100 requests
    timeout: number;             // 30 seconds
}
```

## 8. Security

### 8.1 Authentication Headers
```http
Authorization: Bearer {jwt_token}
X-API-Key: {api_key}
X-Request-ID: {uuid}
X-Portfolio-ID: {portfolio_id}
```

### 8.2 Authorization Scopes
```yaml
scopes:
  - portfolio.read      # Read portfolio data
  - portfolio.write     # Manage portfolios
  - position.execute    # Execute positions
  - strategy.manage     # Manage strategies
```

## 9. Versioning

### 9.1 API Versioning
- Version in URL path: /v1/
- API version header: X-API-Version
- Deprecation header: Deprecated: true

### 9.2 Event Versioning
- Schema version field
- Forward/backward compatibility
- Migration support


## LedgerTimingOptimization Interfaces
Added: 2025-09-13

Interface changes TBD
