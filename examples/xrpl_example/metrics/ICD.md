# Interface Control Document: Metrics Service (ICD-MET-001)

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
This document defines all interfaces for the Metrics Service, which provides system-wide observability, monitoring, and alerting capabilities.

### 1.2 Interface Summary
| Interface | Type | Protocol | Purpose |
|-----------|------|----------|----------|
| Metrics | Collection | HTTP/Protobuf | Metric ingestion |
| Query | API | HTTP/gRPC | Metric querying |
| Alert | API | HTTP/WebSocket | Alert management |
| Admin | API | HTTP | Service management |

## 2. Metrics Collection Interface

### 2.1 Prometheus Exposition Format
```text
# HELP metric_name Description of the metric
# TYPE metric_name counter|gauge|histogram|summary
metric_name{label1="value1",label2="value2"} value timestamp
```

### 2.2 OpenTelemetry Format
```protobuf
message Metric {
    string name = 1;
    string description = 2;
    string unit = 3;
    Data data = 4;
    map<string, string> attributes = 5;
}

message Data {
    oneof value {
        Gauge gauge = 1;
        Sum sum = 2;
        Histogram histogram = 3;
        Summary summary = 4;
    }
}
```

### 2.3 StatsD Format
```text
metric.name:value|type[|@sample_rate][|#tag1:value1,tag2:value2]
```

## 3. Query API Interface

### 3.1 REST Endpoints

#### 3.1.1 Instant Query
```http
GET /api/v1/query
Parameters:
- query: PromQL expression
- time: RFC3339 timestamp

Response:
{
    "status": "success",
    "data": {
        "resultType": "vector",
        "result": [
            {
                "metric": {
                    "label": "value"
                },
                "value": [timestamp, "value"]
            }
        ]
    }
}
```

#### 3.1.2 Range Query
```http
GET /api/v1/query_range
Parameters:
- query: PromQL expression
- start: RFC3339 timestamp
- end: RFC3339 timestamp
- step: duration

Response:
{
    "status": "success",
    "data": {
        "resultType": "matrix",
        "result": [
            {
                "metric": {
                    "label": "value"
                },
                "values": [
                    [timestamp, "value"],
                    [timestamp, "value"]
                ]
            }
        ]
    }
}
```

### 3.2 gRPC Interface
```protobuf
service MetricsQuery {
    rpc Query(QueryRequest) returns (QueryResponse);
    rpc QueryRange(RangeQueryRequest) returns (RangeQueryResponse);
    rpc Labels(LabelsRequest) returns (LabelsResponse);
    rpc Series(SeriesRequest) returns (SeriesResponse);
}

message QueryRequest {
    string query = 1;
    int64 time = 2;
    Timeout timeout = 3;
}

message RangeQueryRequest {
    string query = 1;
    int64 start = 2;
    int64 end = 3;
    string step = 4;
    Timeout timeout = 5;
}
```

## 4. Alert API Interface

### 4.1 Alert Rule Management
```http
POST /api/v1/alerts/rules
Content-Type: application/json

Request:
{
    "name": string,
    "query": string,
    "duration": string,
    "labels": {
        "severity": string,
        "team": string
    },
    "annotations": {
        "summary": string,
        "description": string
    },
    "conditions": [
        {
            "type": "threshold",
            "operator": ">",
            "value": number
        }
    ]
}

Response:
{
    "rule_id": string,
    "status": string,
    "created_at": string
}
```

### 4.2 Alert State Stream
```protobuf
service AlertStream {
    rpc StreamAlerts(AlertStreamRequest) returns (stream Alert);
    rpc StreamStates(StateStreamRequest) returns (stream AlertState);
}

message Alert {
    string alert_id = 1;
    string rule_id = 2;
    AlertState state = 3;
    map<string, string> labels = 4;
    map<string, string> annotations = 5;
    int64 started_at = 6;
}

message AlertState {
    string alert_id = 1;
    State state = 2;
    string reason = 3;
    int64 timestamp = 4;
}
```

## 5. Admin API Interface

### 4.3 Performance Metrics API
```http
GET /api/v1/performance/account-metrics

Response:
{
    "timestamp": "2025-08-30T00:42:00Z",
    "total_allocated_xrp": "100000.0",
    "available_balance_xrp": "20000.0",
    "locked_balance_xrp": "80000.0",
    "current_earnings_rate_xrp": "10.5",
    "avg_earnings_rate_24h_xrp": "9.8",
    "total_earnings_24h_xrp": "235.2",
    "earnings_volatility_24h": "0.15",
    "instant_withdrawal_xrp": "20000.0",
    "one_hour_withdrawal_xrp": "50000.0",
    "withdrawal_cost_basis": "0.002",
    "risk_adjusted_apy": "15.5",
    "projected_next_hour_earnings_xrp": "11.2",
    "projected_confidence": "0.85",
    "opportunity_cost_if_withdrawn_xrp": "10.5"
}

GET /api/v1/performance/metrics

Response:
{
    "timestamp": "2025-08-30T00:42:00Z",
    "total_managed_xrp": "100000.0",
    "total_value_usd": "50000.0",
    "pool_metrics": {
        "POOL_ID": {
            "pool_id": "RLUSD+rMxCKbEDwqr76QuheSUMdEGf4B9xJ8m5De_XRP+XRP",
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
                // ... additional metrics
            },
            // ... last_day and last_week metrics
            "withdrawal_slippage_estimate": "0.002",
            "withdrawal_time_estimate": 300,
            "estimated_next_hour_earnings_xrp": "11.2",
            "confidence_score": "0.85"
        }
    },
    "total_earnings_24h_xrp": "250.0",
    "total_earnings_rate_xrp": "10.42",
    "portfolio_risk_score": "0.3",
    "fastest_withdrawal_seconds": 300,
    "total_withdrawal_seconds": 900,
    "projected_next_hour_earnings_xrp": "11.5",
    "projected_confidence": "0.82"
}

GET /api/v1/performance/pools/{pool_id}/metrics

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
        // ... additional metrics
    },
    // ... last_day and last_week metrics
    "withdrawal_slippage_estimate": "0.002",
    "withdrawal_time_estimate": 300,
    "estimated_next_hour_earnings_xrp": "11.2",
    "confidence_score": "0.85"
}
```

### 5.1 Configuration Management
```http
PUT /api/v1/admin/config
Content-Type: application/json

Request:
{
    "retention": {
        "raw_metrics": "30d",
        "aggregated_metrics": "1y",
        "alerts": "2y"
    },
    "scrape_configs": [
        {
            "job_name": string,
            "scrape_interval": string,
            "static_configs": [
                {
                    "targets": string[],
                    "labels": object
                }
            ]
        }
    ],
    "alert_configs": {
        "routes": [
            {
                "match": object,
                "receiver": string
            }
        ],
        "receivers": [
            {
                "name": string,
                "webhook_configs": [
                    {
                        "url": string,
                        "headers": object
                    }
                ]
            }
        ]
    }
}
```

### 5.2 Status API
```http
GET /api/v1/admin/status

Response:
{
    "status": "healthy|degraded|unhealthy",
    "components": {
        "ingestion": {
            "status": "up|down",
            "metrics": {
                "rate": number,
                "errors": number
            }
        },
        "storage": {
            "status": "up|down",
            "metrics": {
                "capacity": number,
                "used": number
            }
        },
        "alerting": {
            "status": "up|down",
            "metrics": {
                "active_rules": number,
                "firing_alerts": number
            }
        }
    },
    "version": string,
    "uptime": number
}
```

## 6. Data Formats

### 6.1 Metric Types
```typescript
interface Metric {
    name: string;
    type: "counter" | "gauge" | "histogram" | "summary";
    help: string;
    unit?: string;
    labels: Record<string, string>;
}

interface Sample {
    value: number;
    timestamp: number;
    labels: Record<string, string>;
}

interface TimeWindowMetrics {
    window_start: string;      // ISO8601 timestamp
    window_end: string;        // ISO8601 timestamp
    earnings_xrp: string;      // Decimal as string
    earnings_token: string;    // Decimal as string
    fee_earnings_xrp: string;  // Decimal as string
    fee_earnings_token: string; // Decimal as string
    earnings_rate_xrp: string;  // XRP per hour
    earnings_rate_token: string; // Token per hour
    volume_xrp: string;
    volume_token: string;
    avg_liquidity_xrp: string;
    avg_liquidity_token: string;
    avg_slippage: string;      // Percentage
    max_slippage: string;      // Percentage
    impermanent_loss_xrp: string;
    impermanent_loss_token: string;
    price_volatility: string;  // Percentage
    sharpe_ratio: string;
    missed_trades: number;
    opportunity_cost_xrp: string;
}

interface PoolPerformanceMetrics {
    pool_id: string;
    asset1: Currency;
    asset2: Currency;
    current_liquidity_xrp: string;
    current_liquidity_token: string;
    current_price: string;
    last_hour: TimeWindowMetrics;
    last_day: TimeWindowMetrics;
    last_week: TimeWindowMetrics;
    pending_opportunities: number;
    estimated_next_hour_earnings_xrp: string;
    confidence_score: string;        // 0-1
    market_depth_score: string;      // 0-1
    market_activity_score: string;   // 0-1
    risk_score: string;              // 0-1
    il_risk_next_hour: string;
    withdrawal_slippage_estimate: string;
    withdrawal_time_estimate: number; // seconds
    timestamp: string;               // ISO8601
}

interface LPAccountMetrics {
    total_allocated_xrp: string;
    total_value_usd: string;
    available_balance_xrp: string;
    locked_balance_xrp: string;
    current_earnings_rate_xrp: string;
    avg_earnings_rate_24h_xrp: string;
    total_earnings_24h_xrp: string;
    earnings_volatility_24h: string;
    pending_opportunities: number;
    max_opportunity_size_xrp: string;
    opportunity_time_window: number;
    opportunity_confidence: string; // 0-1
    capital_utilization: string; // percentage
    risk_adjusted_apy: string; // percentage
    portfolio_risk_score: string; // 0-1
    risk_breakdown: Record<string, string>;
    instant_withdrawal_xrp: string;
    one_hour_withdrawal_xrp: string;
    withdrawal_cost_basis: string;
    projected_next_hour_earnings_xrp: string;
    projected_confidence: string; // 0-1
    opportunity_cost_if_withdrawn_xrp: string;
    timestamp: string; // ISO8601
}

interface ServicePerformanceMetrics {
    total_managed_xrp: string;
    total_value_usd: string;
    pool_metrics: Record<string, PoolPerformanceMetrics>;
    total_earnings_24h_xrp: string;
    total_earnings_rate_xrp: string;
    service_uptime: number;          // percentage
    portfolio_risk_score: string;    // 0-1
    portfolio_diversification_score: string; // 0-1
    fastest_withdrawal_seconds: number;
    total_withdrawal_seconds: number;
    weighted_avg_slippage: string;   // percentage
    projected_next_hour_earnings_xrp: string;
    projected_confidence: string;    // 0-1
    timestamp: string;              // ISO8601
}
```

### 6.2 Alert Format
```typescript
interface Alert {
    id: string;
    name: string;
    state: "inactive" | "pending" | "firing" | "resolved";
    labels: Record<string, string>;
    annotations: Record<string, string>;
    value: number;
    activeAt: string;
    resolvedAt?: string;
}
```

## 7. Integration Patterns

### 7.1 Service Discovery
```yaml
scrape_configs:
  - job_name: 'service_discovery'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

### 7.2 Label Management
```yaml
metric_relabel_configs:
  - source_labels: [__name__]
    regex: 'service_(.+)'
    target_label: metric_name
    replacement: '$1'
```

## 8. Security

### 8.1 Authentication
```http
Authorization: Bearer {token}
X-API-Key: {api_key}
```

### 8.2 Authorization
```yaml
rules:
  - name: metrics_read
    resources: ["metrics", "queries"]
    verbs: ["get", "list"]
  - name: alerts_manage
    resources: ["alerts", "rules"]
    verbs: ["get", "list", "create", "update", "delete"]
```

## 9. Service Level Objectives

### 9.1 Performance SLOs
- Ingestion Latency: p99 < 10ms
- Query Latency: p99 < 100ms
- Alert Processing: p99 < 1s
- API Response: p99 < 500ms

### 9.2 Reliability SLOs
- Service Availability: 99.99%
- Data Accuracy: 100%
- Alert Delivery: 99.9%
- No Data Loss

## 10. Error Handling

### 10.1 Error Format
```json
{
    "error": {
        "code": string,
        "message": string,
        "details": object|null
    },
    "request_id": string,
    "timestamp": string
}
```

### 10.2 Error Codes
```typescript
enum ErrorCode {
    INVALID_REQUEST = "INVALID_REQUEST",
    QUERY_TIMEOUT = "QUERY_TIMEOUT",
    STORAGE_ERROR = "STORAGE_ERROR",
    ALERT_ERROR = "ALERT_ERROR",
    INTERNAL_ERROR = "INTERNAL_ERROR"
}
```

## 11. Versioning

### 11.1 API Versioning
- Version in URL path: /v1/
- API version header: X-API-Version
- Deprecation header: Deprecated: true

### 11.2 Metric Versioning
- Metric naming: service_version_metric_name
- Label versioning: version="1.0"
- Compatibility handling
- Migration support
