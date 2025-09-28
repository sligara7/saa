# Interface Control Document: XRPL Service (ICD-XRP-001)

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
This document defines all interfaces for the XRPL Service, which provides blockchain interaction, transaction management, and cross-chain bridging capabilities.

### 1.2 Interface Summary
| Interface | Type | Protocol | Purpose |
|-----------|------|----------|----------|
| XRPL | External | WebSocket/JSON-RPC | Network interaction |
| Axelar | External | gRPC | Bridge operations |
| Message Bus | Internal | AMQP | Event communication |
| REST API | External | HTTPS | Service control |

## 2. XRPL Network Interface

### 2.1 WebSocket Connection
```typescript
interface XRPLConnection {
    url: string;
    credentials?: {
        key: string;
        certificate: string;
    };
    options: {
        max_connections: number;
        keep_alive: boolean;
        timeout: number;
        retry_interval: number;
    };
}
```

### 2.2 Request Types
```typescript
// Account requests
interface AccountRequest {
    command: "account_info" | "account_lines" | "account_objects";
    account: string;
    ledger_index: "validated" | "current" | number;
}

// Transaction requests
interface TransactionRequest {
    command: "submit" | "tx" | "transaction_entry";
    tx_blob?: string;
    tx_json?: object;
    transaction?: string;
}

// AMM requests
interface AMMRequest {
    command: "amm_info";
    asset: {
        currency: string;
        issuer?: string;
    };
    asset2: {
        currency: string;
        issuer?: string;
    };
}
```

### 2.3 Response Types
```typescript
interface XRPLResponse {
    id: number;
    status: "success" | "error";
    type: "response";
    result: {
        // Common fields
        ledger_index: number;
        ledger_hash: string;
        validated: boolean;
        
        // Operation-specific data
        [key: string]: any;
    };
    error?: {
        code: number;
        message: string;
        data?: any;
    };
}
```

## 3. Axelar Bridge Interface

### 3.1 gRPC Service Definition
```protobuf
service AxelarBridge {
    // Bridge operations
    rpc InitiateBridge(BridgeRequest) returns (BridgeResponse);
    rpc TrackBridgeStatus(BridgeQuery) returns (stream BridgeStatus);
    rpc ValidateProof(ProofRequest) returns (ProofValidation);
    
    // State management
    rpc GetBridgeState(BridgeStateQuery) returns (BridgeState);
    rpc MonitorBridgeHealth(HealthQuery) returns (stream HealthStatus);
}

message BridgeRequest {
    string source_chain = 1;
    string destination_chain = 2;
    string source_asset = 3;
    string destination_asset = 4;
    string amount = 5;
    string recipient = 6;
    bytes proof_data = 7;
}
```

### 3.2 Bridge Events
```protobuf
message BridgeEvent {
    string event_id = 1;
    string bridge_id = 2;
    BridgeStatus status = 3;
    BridgeDetails details = 4;
    int64 timestamp = 5;
}

message BridgeStatus {
    enum Status {
        INITIATED = 0;
        PENDING = 1;
        COMPLETED = 2;
        FAILED = 3;
    }
    Status status = 1;
    string message = 2;
    repeated BridgeStep steps = 3;
}
```

## 4. Message Bus Interface

### 4.1 Published Events

#### 4.1.1 Transaction Events
```protobuf
message TransactionEvent {
    string transaction_hash = 1;
    string ledger_hash = 2;
    uint64 ledger_index = 3;
    TransactionStatus status = 4;
    TransactionDetails details = 5;
    int64 timestamp = 6;
}

message AMMEvent {
    string pool_id = 1;
    PoolState state = 2;
    repeated Trade trades = 3;
    int64 timestamp = 4;
}
```

#### 4.1.2 Network Events
```protobuf
message NetworkEvent {
    string node_id = 1;
    NetworkStatus status = 2;
    map<string, string> metrics = 3;
    int64 timestamp = 4;
}

message BridgeNetworkEvent {
    string network = 1;
    BridgeStatus status = 2;
    map<string, string> metrics = 3;
    int64 timestamp = 4;
}
```

### 4.2 Consumed Events
```protobuf
message TransactionRequest {
    string request_id = 1;
    TransactionType type = 2;
    bytes transaction_data = 3;
    SigningDetails signing = 4;
    int64 deadline = 5;
}

message BridgeRequest {
    string request_id = 1;
    BridgeOperation operation = 2;
    bytes operation_data = 3;
    int64 deadline = 4;
}
```

## 5. REST API Interface

### 5.1 Transaction Endpoints
```http
POST /api/v1/transactions/submit
Content-Type: application/json

Request:
{
    "transaction": {
        "TransactionType": string,
        "Account": string,
        "Fee": string,
        "Sequence": number,
        "LastLedgerSequence": number,
        ...additional fields
    },
    "options": {
        "auto_fill": boolean,
        "fail_hard": boolean
    }
}

Response:
{
    "hash": string,
    "status": string,
    "result": object,
    "ledger_index": number
}
```

### 5.2 AMM Endpoints
```http
GET /api/v1/amm/pools/{pool_id}/performance

Response:
{
    "pool_id": "RLUSD+rMxCKbEDwqr76QuheSUMdEGf4B9xJ8m5De_XRP+XRP",
    "timestamp": "2025-08-30T00:42:00Z",
    "current_liquidity_xrp": "50000.0",
    "current_price": "0.5123",
    "last_hour": {
        "window_start": "2025-08-29T23:42:00Z",
        "window_end": "2025-08-30T00:42:00Z",
        "earnings_xrp": "10.5",
        "earnings_rate_xrp": "10.5",
        "volume_xrp": "25000.0",
        "avg_slippage": "0.001",
        "price_volatility": "0.5",
        "missed_trades": 2,
        "opportunity_cost_xrp": "2.5"
    },
    "last_day": {
        // Similar structure to last_hour
    },
    "last_week": {
        // Similar structure to last_hour
    },
    "withdrawal_slippage_estimate": "0.002",
    "withdrawal_time_estimate": 300,
    "estimated_next_hour_earnings_xrp": "11.2",
    "confidence_score": "0.85"
}

GET /api/v1/amm/performance

Response:
{
    "timestamp": "2025-08-30T00:42:00Z",
    "total_managed_xrp": "100000.0",
    "total_value_usd": "50000.0",
    "pool_metrics": {
        // Detailed metrics per pool
    },
    "total_earnings_24h_xrp": "250.0",
    "total_earnings_rate_xrp": "10.42",
    "portfolio_risk_score": "0.3",
    "fastest_withdrawal_seconds": 300,
    "total_withdrawal_seconds": 900,
    "projected_next_hour_earnings_xrp": "11.5",
    "projected_confidence": "0.82"
}

GET /api/v1/amm/pools/{pool_id}

Response:
{
    "pool_id": string,
    "asset_a": {
        "currency": string,
        "issuer": string,
        "amount": string
    },
    "asset_b": {
        "currency": string,
        "issuer": string,
        "amount": string
    },
    "lp_token": {
        "currency": string,
        "amount": string
    },
    "trading_fee": string,
    "timestamp": string
}
```

### 5.3 Bridge Endpoints
```http
POST /api/v1/bridge/transfer
Content-Type: application/json

Request:
{
    "source_chain": string,
    "destination_chain": string,
    "asset": {
        "currency": string,
        "issuer": string,
        "amount": string
    },
    "recipient": string,
    "options": {
        "max_fee": string,
        "timeout": number
    }
}

Response:
{
    "bridge_id": string,
    "status": string,
    "estimated_completion": string,
    "steps": [
        {
            "step": string,
            "status": string,
            "estimated_time": string
        }
    ]
}
```

## 6. Metrics Interface

### 6.1 Performance Metrics
NOTE: For all performance metrics related to LP activities, please refer to the Metrics Service (/api/v1/performance/account-metrics)
for the account-level view appropriate for cross-chain portfolio management.

### 6.2 Prometheus Metrics
```
# XRPL Metrics
xrpl_node_connections{node_id="*"} gauge
xrpl_transaction_count{type="*",status="*"} counter
xrpl_transaction_latency_seconds histogram
xrpl_ledger_lag_seconds gauge

# AMM Metrics
xrpl_amm_pools_total gauge
xrpl_amm_tvl{pool_id="*"} gauge
xrpl_amm_volume_24h{pool_id="*"} gauge
xrpl_amm_trades_total counter
xrpl_amm_earnings{pool_id="*",type="total|fees|il"} counter
xrpl_amm_earnings_rate{pool_id="*"} gauge
xrpl_amm_missed_trades{pool_id="*"} counter
xrpl_amm_opportunity_cost{pool_id="*"} gauge
xrpl_amm_price_volatility{pool_id="*"} gauge
xrpl_amm_market_depth{pool_id="*"} gauge
xrpl_amm_market_activity{pool_id="*"} gauge
xrpl_amm_risk_score{pool_id="*"} gauge
xrpl_amm_withdrawal_slippage{pool_id="*"} gauge
xrpl_amm_withdrawal_time{pool_id="*"} gauge

# Bridge Metrics
bridge_operations_total{network="*",status="*"} counter
bridge_operation_duration_seconds histogram
bridge_tvl{network="*"} gauge
bridge_health{network="*"} gauge
```

### 6.2 Health Check
```http
GET /health

Response:
{
    "status": "up|down|degraded",
    "components": {
        "xrpl": {
            "status": "up|down",
            "nodes": {
                "connected": number,
                "total": number
            },
            "ledger_lag": number
        },
        "bridge": {
            "status": "up|down",
            "networks": {
                "xrpl": "up|down",
                "axelar": "up|down"
            }
        }
    },
    "version": string,
    "timestamp": string
}
```

## 7. Data Formats

### 7.1 Common Types
```typescript
type Hash = string;         // 64-character hex
type Address = string;      // XRPL address format
type Amount = string;       // Decimal as string
type LedgerIndex = number; // Unsigned integer
type Timestamp = string;   // ISO-8601 in UTC
```

### 7.2 Error Format
```json
{
    "error": {
        "code": string,
        "message": string,
        "details": object|null,
        "ledger_index": number|null
    },
    "request_id": string,
    "timestamp": string
}
```

## 8. Service Level Objectives

### 8.1 Performance SLOs
- Transaction Submit: p99 < 100ms
- State Query: p99 < 50ms
- Bridge Operations: p99 < 500ms
- Event Processing: p99 < 100ms

### 8.2 Reliability SLOs
- Service Availability: 99.99%
- Transaction Success Rate: 99.9%
- Bridge Operation Success: 99.9%
- Data Accuracy: 100%

## 9. Security

### 9.1 Authentication
```http
Authorization: Bearer {token}
X-API-Key: {api_key}
X-Request-ID: {uuid}
```

### 9.2 Authorization Scopes
```yaml
scopes:
  - xrpl.read        # Read network data
  - xrpl.write       # Submit transactions
  - amm.read         # Read AMM data
  - amm.write        # Manage AMM positions
  - bridge.operate   # Bridge operations
```

## 10. Integration Patterns

### 10.1 Circuit Breaker
```typescript
interface CircuitBreaker {
    failure_threshold: number;    // 5 failures
    reset_timeout: number;        // 30 seconds
    half_open_timeout: number;    // 5 seconds
}
```

### 10.2 Retry Policy
```typescript
interface RetryPolicy {
    max_attempts: number;         // 3 attempts
    initial_delay: number;        // 1 second
    max_delay: number;           // 5 seconds
    backoff_multiplier: number;  // 2.0
}
```

## 11. Versioning

### 11.1 API Versioning
- Version in URL path: /v1/
- API version header: X-API-Version
- Deprecation header: Deprecated: true

### 11.2 Event Versioning
- Schema version field
- Forward/backward compatibility
- Migration support


## LedgerTimingOptimization Interfaces
Added: 2025-09-13

Interface changes TBD


## LedgerTimingOptimization Interfaces
Added: 2025-09-13

Interface changes TBD


## LedgerTimingOptimization Interfaces
Added: 2025-09-13

Interface changes TBD
