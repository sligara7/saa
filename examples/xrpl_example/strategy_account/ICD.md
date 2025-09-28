# Interface Control Document: Strategy Account Service (ICD-SAS-001)

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
This document defines all external interfaces for the Strategy Account Service, which manages fund allocation and transfer between trading strategies.

### 1.2 Interface Summary
| Interface | Type | Protocol | Purpose |
|-----------|------|----------|----------|
| REST API | External | HTTPS | Account operations |
| Message Bus | Internal | AMQP | Event communication |
| Database | Internal | MySQL | State persistence |
| Metrics | Internal | Prometheus | System monitoring |

## 2. REST API Interface

### 2.1 Endpoint Base
```
https://api.{domain}/v1/strategy
```

### 2.2 Authentication
- Type: API Key + JWT
- Headers: X-API-Key, Authorization

### 2.3 Endpoints

#### 2.3.0 Accounting Reports
```http
GET /accounting/profit-loss
Response:
{
    "timeframe": "daily|weekly|monthly|yearly",
    "strategies": [
        {
            "strategy_id": string,
            "realized_pl": string,
            "unrealized_pl": string,
            "fees_paid": string,
            "fees_earned": string
        }
    ],
    "totals": {
        "realized_pl": string,
        "unrealized_pl": string,
        "fees_paid": string,
        "fees_earned": string
    }
}

GET /accounting/tax-summary
Response:
{
    "tax_year": number,
    "summaries": [
        {
            "category": "trading_income|capital_gains|fee_income|yield_income",
            "amount": string,
            "transaction_count": number
        }
    ],
    "cost_basis": [
        {
            "token": string,
            "acquisition_date": string,
            "amount": string,
            "cost_basis": string
        }
    ]
}

GET /accounting/strategy-performance
Response:
{
    "strategy_id": string,
    "metrics": {
        "roi": string,
        "sharpe_ratio": string,
        "max_drawdown": string
    },
    "fee_analysis": {
        "paid": string,
        "earned": string,
        "net": string
    },
    "historical_performance": [
        {
            "timestamp": string,
            "value": string,
            "pl_daily": string
        }
    ]
}
```

#### 2.3.1 Strategy Management
```http
POST /strategies
Content-Type: application/json

Request:
{
    "name": string,
    "description": string,
    "risk_level": number,
    "config": object
}

Response:
{
    "strategy_id": string,
    "status": "active",
    "created_at": string
}

GET /strategies/{strategy_id}

Response:
{
    "strategy_id": string,
    "name": string,
    "description": string,
    "risk_level": number,
    "config": object,
    "status": string,
    "balances": {
        "token": string,
        "amount": string
    }[],
    "metrics": object
}
```

#### 2.3.2 Cross-Strategy Transfers
```http
POST /transfers
Content-Type: application/json

Request:
{
    "source_strategy": string,
    "target_strategy": string,
    "token": string,
    "amount": string,
    "priority": "normal|expedited|emergency",
    "max_slippage": string,
    "max_time_seconds": number
}

Response:
{
    "transfer_id": string,
    "status": "queued|executing|completed",
    "estimated_completion_time": string,
    "steps": [
        {
            "type": "withdraw_lp|allocate",
            "amount": string,
            "status": string
        }
    ],
    "fees": {
        "network": string,
        "slippage": string
    }
}

GET /transfers/{transfer_id}

Response:
{
    "transfer_id": string,
    "status": string,
    "details": object
}
```

#### 2.3.3 LP Management
```http
POST /withdrawals/lp
Content-Type: application/json

Request:
{
    "strategy_id": string,
    "pool_id": string,
    "amount": string,
    "max_slippage": string
}

Response:
{
    "withdrawal_id": string,
    "estimated_completion_time": string
}

GET /positions/lp
Response:
{
    "positions": [
        {
            "pool_id": string,
            "strategy_id": string,
            "amount": string,
            "value_xrp": string
        }
    ]
}
```

#### 2.3.4 Wallet Transition Support
```http
POST /wallet/transition/{transition_id}/prepare
Content-Type: application/json

Request:
{
    "max_time_minutes": number,
    "max_slippage": string
}

Response:
{
    "transition_id": string,
    "status": "started",
    "estimated_completion_time": string
}

GET /wallet/transition/{transition_id}/status
Response:
{
    "transition_id": string,
    "status": "liquidating|verifying|completed",
    "completion_percentage": number,
    "current_position": {
        "pool_id": string,
        "amount": string,
        "status": string
    },
    "positions_remaining": number
}
```

## 3. Message Bus Interface

### 3.1 Events Published

#### 3.1.0 Accounting Events
```protobuf
message ProfitLossCalculated {
    string strategy_id = 1;
    string realized_pl = 2;
    string unrealized_pl = 3;
    string timestamp = 4;
}

message TaxEventRecorded {
    string strategy_id = 1;
    string category = 2;
    string amount = 3;
    string timestamp = 4;
}

message CostBasisUpdated {
    string token = 1;
    string amount = 2;
    string cost_basis = 3;
    string timestamp = 4;
}
```

#### 3.1.1 Transfer Events
```protobuf
message TransferInitiated {
    string transfer_id = 1;
    string source_strategy = 2;
    string target_strategy = 3;
    string token = 4;
    string amount = 5;
    string timestamp = 6;
}

message TransferCompleted {
    string transfer_id = 1;
    string source_strategy = 2;
    string target_strategy = 3;
    string token = 4;
    string amount = 5;
    string timestamp = 6;
}
```

#### 3.1.2 Transition Events
```protobuf
message TransitionProgress {
    string transition_id = 1;
    int32 total_positions = 2;
    int32 positions_liquidated = 3;
    string status = 4;
    string timestamp = 5;
}

message TransitionReadiness {
    string transition_id = 1;
    bool is_ready = 2;
    string status = 3;
    string timestamp = 4;
}
```

### 3.2 Events Consumed

```protobuf
message WalletTransitionStarted {
    string wallet_id = 1;
    string transition_id = 2;
    string timestamp = 3;
}

message WalletActivated {
    string wallet_id = 1;
    string activation_id = 2;
    string timestamp = 3;
}
```

## 4. Metrics Interface

### 4.1 Prometheus Metrics

#### 4.1.0 Accounting Metrics
```
# Profit/Loss Metrics
strategy_realized_pl{strategy_id="*"} gauge
strategy_unrealized_pl{strategy_id="*"} gauge
strategy_fees_paid{strategy_id="*"} counter
strategy_fees_earned{strategy_id="*"} counter

# Cost Basis Metrics
token_cost_basis{token="*"} gauge
token_unrealized_gain{token="*"} gauge

# Tax Metrics
tax_events_total{category="*"} counter
tax_calculation_errors{type="*"} counter
```
```
# Strategy Metrics
strategy_balance{strategy_id="*",token="*"} gauge
strategy_operations_total{strategy_id="*",operation_type="*"} counter
strategy_transfers_total{status="*"} counter

# LP Metrics
lp_positions{strategy_id="*",pool_id="*"} gauge
lp_value_xrp{strategy_id="*",pool_id="*"} gauge
lp_withdrawals_total{status="*"} counter

# Transition Metrics
transition_duration_seconds histogram
transition_positions_total gauge
transition_positions_liquidated gauge
```

### 4.2 Health Check
```http
GET /health

Response:
{
    "status": "up|down|degraded",
    "components": {
        "database": "up|down",
        "message_bus": "up|down",
        "lp_manager": "up|down"
    },
    "metrics": {
        "active_transfers": number,
        "active_transitions": number,
        "error_rate": number
    }
}
```

## 5. Data Formats

### 5.1 Common Types
```typescript
type StrategyID = string;    // UUID v4
type TransferID = string;    // UUID v4
type TransitionID = string;  // UUID v4
type Amount = string;        // Decimal as string
type Timestamp = string;     // ISO-8601 in UTC
```

### 5.2 Error Format
```json
{
    "error": {
        "code": string,
        "message": string,
        "details": object|null,
        "transfer_id": string|null
    },
    "request_id": string,
    "timestamp": string
}
```

## 6. Service Level Objectives

### 6.1 Performance SLOs
- Transfer Initiation: p99 < 50ms
- Balance Updates: p99 < 10ms
- LP Withdrawals: p99 < 30s
- Full Position Liquidation: p99 < 30m

### 6.2 Reliability SLOs
- Service Availability: 99.99%
- Transfer Success Rate: 99.99%
- Data Accuracy: 100%

## 7. Security

### 7.1 Authentication Headers
```http
Authorization: Bearer {jwt_token}
X-API-Key: {api_key}
X-Request-ID: {uuid}
X-Transfer-ID: {transfer_id}
```

### 7.2 Authorization Scopes
```yaml
scopes:
  - strategy.create    # Create strategies
  - strategy.manage    # Manage strategies
  - strategy.transfer  # Transfer between strategies
  - strategy.withdraw  # LP withdrawals
```

## 8. Integration Patterns

### 8.1 Circuit Breaker
```typescript
interface CircuitBreaker {
    failure_threshold: number;    // 3 failures
    reset_timeout: number;        // 60 seconds
    half_open_timeout: number;    // 10 seconds
}
```

### 8.2 Retry Policy
```typescript
interface RetryPolicy {
    max_attempts: number;         // 3 attempts
    initial_delay: number;        // 1 second
    max_delay: number;           // 5 seconds
    backoff_multiplier: number;  // 2.0
}
```

### 8.3 Rate Limiting
```typescript
interface RateLimit {
    transfers_per_second: number;  // 50 operations
    burst_size: number;           // 100 operations
    timeout: number;              // 30 seconds
}
```

## 9. Database Schema

### 9.1 Strategy Table

#### 9.1.0 Accounting Tables
```sql
CREATE TABLE profit_loss (
    id UUID PRIMARY KEY,
    strategy_id UUID REFERENCES strategies(id),
    realized_pl DECIMAL(20,8) NOT NULL,
    unrealized_pl DECIMAL(20,8) NOT NULL,
    fees_paid DECIMAL(20,8) NOT NULL,
    fees_earned DECIMAL(20,8) NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

CREATE TABLE tax_events (
    id UUID PRIMARY KEY,
    strategy_id UUID REFERENCES strategies(id),
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(20,8) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    details JSONB
);

CREATE TABLE cost_basis (
    id UUID PRIMARY KEY,
    token VARCHAR(10) NOT NULL,
    amount DECIMAL(20,8) NOT NULL,
    cost_basis DECIMAL(20,8) NOT NULL,
    acquisition_date TIMESTAMP NOT NULL,
    disposal_date TIMESTAMP,
    status VARCHAR(20) NOT NULL
);
```
```sql
CREATE TABLE strategies (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    risk_level INTEGER NOT NULL,
    config JSONB,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

### 9.2 Balance Table
```sql
CREATE TABLE balances (
    strategy_id UUID REFERENCES strategies(id),
    token VARCHAR(10) NOT NULL,
    amount DECIMAL(20,8) NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (strategy_id, token)
);
```

### 9.3 Transfer Table
```sql
CREATE TABLE transfers (
    id UUID PRIMARY KEY,
    source_strategy UUID REFERENCES strategies(id),
    target_strategy UUID REFERENCES strategies(id),
    token VARCHAR(10) NOT NULL,
    amount DECIMAL(20,8) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP
);
```

## 10. Versioning

### 10.1 API Versioning
- Version in URL path: /v1/
- API version header: X-API-Version
- Deprecation header: Deprecated: true

### 10.2 Event Versioning
- Schema version field
- Forward/backward compatibility
- Migration support
