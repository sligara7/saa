# Interface Control Document: Database Service (ICD-DB-001)

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


Revision History:
- 1.0 (2025-08-29): Initial version
- 1.1 (2025-09-14): Added service-specific interfaces and expanded data models
- 1.2 (2025-09-15): Added financial and risk tracking interfaces, enhanced backup/recovery, and updated metrics

## 1. Interface Overview

### 1.1 Purpose
This document defines all interfaces for the Database Service, which provides centralized data storage and management capabilities for the XRPL LP Optimization System.

### 1.2 Interface Summary
| Interface | Type | Protocol | Purpose |
|-----------|------|----------|----------|
| Query | Primary | gRPC/HTTP | Data operations |
| Admin | Management | HTTPS | Service management |
| Migration | Internal | HTTP | Schema management |
| Backup | Internal | HTTP/gRPC | Backup control |
| Portfolio | Service | gRPC | LP Portfolio data |
| Strategy | Service | gRPC | Strategy Account data |
| Security | Service | gRPC | Wallet Security data |
| Analytics | Service | gRPC | Metrics and Analytics data |
| Financial | Service | gRPC | Financial records and tracking |
| Risk | Service | gRPC | Risk metrics and monitoring |

## 2. Query Interface

### 2.1 Base Service Definition
```protobuf
service DatabaseQuery {
    // Basic Operations
    rpc Query(QueryRequest) returns (QueryResponse);
    rpc Execute(ExecuteRequest) returns (ExecuteResponse);
    rpc Batch(BatchRequest) returns (BatchResponse);
    rpc Stream(StreamRequest) returns (stream StreamResponse);
    
    // Transaction Management
    rpc BeginTransaction(TransactionRequest) returns (TransactionResponse);
    rpc Commit(TransactionId) returns (CommitResponse);
    rpc Rollback(TransactionId) returns (RollbackResponse);
}

message QueryRequest {
    string query = 1;
    map<string, Value> parameters = 2;
    QueryOptions options = 3;
    string transaction_id = 4;
}

message ExecuteRequest {
    string statement = 1;
    map<string, Value> parameters = 2;
    ExecuteOptions options = 3;
    string transaction_id = 4;
}
```

### 2.2 Data Operations
```typescript
interface DataOperations {
    // CRUD Operations
    create(data: object): Promise<Result>;
    read(query: Query): Promise<Result>;
    update(criteria: object, data: object): Promise<Result>;
    delete(criteria: object): Promise<Result>;
    
    // Batch Operations
    batchCreate(items: object[]): Promise<Result[]>;
    batchUpdate(operations: Operation[]): Promise<Result[]>;
    
    // Transaction Operations
    transaction<T>(fn: (tx: Transaction) => Promise<T>): Promise<T>;
}
```

### 2.3 Query Options
```typescript
interface QueryOptions {
    timeout: number;
    consistency: "strong" | "eventual";
    retryPolicy: RetryPolicy;
    maxRows: number;
    fetchSize: number;
}

interface ExecuteOptions {
    timeout: number;
    consistency: "strong" | "eventual";
    retryPolicy: RetryPolicy;
    batchSize: number;
}
```

## 3. Service-Specific Interfaces

### 3.1 Portfolio Service Interface
```protobuf
service PortfolioData {
    // Strategy Management
    rpc GetStrategy(StrategyRequest) returns (Strategy);
    rpc ListStrategies(ListRequest) returns (StrategyList);
    rpc TrackPerformance(StrategyId) returns (stream PerformanceMetrics);

    // Risk Management
    rpc GetRiskMetrics(RiskRequest) returns (RiskMetrics);
    rpc TrackImpermanentLoss(PoolId) returns (stream ILMetrics);
    
    // Fee Optimization
    rpc GetFeeHistory(FeeRequest) returns (FeeHistory);
    rpc OptimizeFees(OptimizationRequest) returns (OptimizationResult);
}

message Strategy {
    string id = 1;
    string name = 2;
    map<string, string> parameters = 3;
    RiskProfile risk_profile = 4;
    repeated Constraint constraints = 5;
}

message PerformanceMetrics {
    string strategy_id = 1;
    int64 timestamp = 2;
    double returns = 3;
    double fees_earned = 4;
    double impermanent_loss = 5;
}
```

### 3.2 Strategy Account Interface
```protobuf
service StrategyAccount {
    // Financial Records
    rpc GetCostBasis(AssetRequest) returns (CostBasisRecord);
    rpc TrackProfitLoss(AccountRequest) returns (stream PLRecord);
    rpc GetTaxEvents(TaxRequest) returns (TaxEventList);

    // Fund Management
    rpc GetFundAllocations(AllocationRequest) returns (AllocationList);
    rpc GetTransferHistory(TransferRequest) returns (TransferList);
    rpc GetFinancialStatements(StatementRequest) returns (FinancialStatement);
}

message CostBasisRecord {
    string asset_id = 1;
    string account_id = 2;
    repeated AcquisitionLot lots = 3;
    TaxLotMethod method = 4;
}

message PLRecord {
    string account_id = 1;
    int64 timestamp = 2;
    double realized_pl = 3;
    double unrealized_pl = 4;
    map<string, double> positions = 5;
}
```

### 3.3 Security Service Interface
```protobuf
service SecurityData {
    // HSM Operations
    rpc GetHSMOperationLog(HSMRequest) returns (HSMOperationLog);
    rpc TrackKeyRotations(KeyRequest) returns (stream KeyRotationEvent);

    // Key Management
    rpc GetMultiSigConfig(MultiSigRequest) returns (MultiSigConfig);
    rpc GetRegularKeyHistory(RegularKeyRequest) returns (KeyHistory);

    // Permission Management
    rpc GetPermissionConfig(PermissionRequest) returns (PermissionConfig);
    rpc GetSecurityAuditLog(AuditRequest) returns (SecurityAuditLog);
}

message KeyRotationEvent {
    string key_id = 1;
    int64 rotation_timestamp = 2;
    string key_type = 3;
    string status = 4;
    bytes previous_key_hash = 5;
    bytes new_key_hash = 6;
}

message SecurityAuditLog {
    string resource_id = 1;
    repeated AuditEvent events = 2;
    string compliance_status = 3;
}
```

### 3.4 Analytics Service Interface

```protobuf
service AnalyticsData {
    // Time Series Data
    rpc GetMetricData(MetricRequest) returns (stream MetricPoint);
    rpc GetAggregations(AggregationRequest) returns (AggregationResult);

    // Configuration
    rpc GetAlertConfig(AlertRequest) returns (AlertConfig);
    rpc GetDashboardConfig(DashboardRequest) returns (DashboardConfig);

    // SLO/SLA Tracking
    rpc GetSLOMetrics(SLORequest) returns (SLOMetrics);
    rpc TrackSLACompliance(SLARequest) returns (stream ComplianceStatus);
}

message MetricPoint {
    string metric_name = 1;
    int64 timestamp = 2;
    double value = 3;
    map<string, string> labels = 4;
}

message SLOMetrics {
    string service_id = 1;
    double availability = 2;
    double latency_p99 = 3;
    double error_rate = 4;
    map<string, double> custom_metrics = 5;
}
```

### 3.5 Financial Service Interface

```protobuf
service FinancialData {
    // Transaction Records
    rpc GetTransactionHistory(TransactionHistoryRequest) returns (TransactionHistoryResponse);
    rpc TrackTransactionStream(TransactionStreamRequest) returns (stream TransactionEvent);
    
    // Balance Management
    rpc GetBalanceSheet(BalanceSheetRequest) returns (BalanceSheet);
    rpc GetProfitLossStatement(PLStatementRequest) returns (PLStatement);
    
    // Financial Analytics
    rpc GetFinancialMetrics(FinancialMetricsRequest) returns (FinancialMetrics);
    rpc TrackFinancialKPIs(KPIRequest) returns (stream KPIMetrics);
}

message TransactionEvent {
    string transaction_id = 1;
    int64 timestamp = 2;
    TransactionType type = 3;
    Amount amount = 4;
    string status = 5;
    map<string, string> metadata = 6;
}

message BalanceSheet {
    int64 timestamp = 1;
    repeated Asset assets = 2;
    repeated Liability liabilities = 3;
    Amount total_equity = 4;
    map<string, Amount> reserves = 5;
}

message PLStatement {
    int64 start_time = 1;
    int64 end_time = 2;
    Amount gross_profit = 3;
    Amount net_profit = 4;
    repeated Revenue revenues = 5;
    repeated Expense expenses = 6;
}
```

### 3.6 Risk Management Interface

```protobuf
service RiskData {
    // Risk Metrics
    rpc GetRiskProfile(RiskProfileRequest) returns (RiskProfile);
    rpc TrackRiskMetrics(RiskMetricsRequest) returns (stream RiskMetrics);
    
    // Portfolio Risk
    rpc GetPortfolioRisk(PortfolioRiskRequest) returns (PortfolioRisk);
    rpc TrackRiskExposure(ExposureRequest) returns (stream RiskExposure);
    
    // Risk Alerts
    rpc GetRiskAlerts(RiskAlertRequest) returns (RiskAlertList);
    rpc SubscribeToRiskAlerts(RiskAlertSubscription) returns (stream RiskAlert);
}

message RiskProfile {
    string profile_id = 1;
    RiskLevel risk_level = 2;
    map<string, double> risk_factors = 3;
    repeated RiskLimit limits = 4;
    RiskToleranceConfig tolerance = 5;
}

message RiskMetrics {
    string asset_id = 1;
    int64 timestamp = 2;
    double volatility = 3;
    double var_95 = 4;  // Value at Risk (95% confidence)
    double max_drawdown = 5;
    map<string, double> correlation_matrix = 6;
}

message RiskExposure {
    string portfolio_id = 1;
    int64 timestamp = 2;
    map<string, double> asset_exposure = 3;
    double total_exposure = 4;
    RiskMetrics portfolio_risk = 5;
    repeated RiskAlert active_alerts = 6;
}
```

### 3.7 Analytics Service Interface
```protobuf
service AnalyticsData {
    // Time Series Data
    rpc GetMetricData(MetricRequest) returns (stream MetricPoint);
    rpc GetAggregations(AggregationRequest) returns (AggregationResult);

    // Configuration
    rpc GetAlertConfig(AlertRequest) returns (AlertConfig);
    rpc GetDashboardConfig(DashboardRequest) returns (DashboardConfig);

    // SLO/SLA Tracking
    rpc GetSLOMetrics(SLORequest) returns (SLOMetrics);
    rpc TrackSLACompliance(SLARequest) returns (stream ComplianceStatus);
}

message MetricPoint {
    string metric_name = 1;
    int64 timestamp = 2;
    double value = 3;
    map<string, string> labels = 4;
}

message SLOMetrics {
    string service_id = 1;
    double availability = 2;
    double latency_p99 = 3;
    double error_rate = 4;
    map<string, double> custom_metrics = 5;
}
```

## 4. Schema Management Interface

### 3.1 Migration API
```http
POST /api/v1/schema/migrations
Content-Type: application/json

Request:
{
    "version": string,
    "description": string,
    "statements": string[],
    "rollback_statements": string[],
    "options": {
        "transaction": boolean,
        "timeout": number,
        "validate": boolean
    }
}

Response:
{
    "migration_id": string,
    "status": string,
    "execution_time": number,
    "affected_tables": string[]
}
```

### 3.2 Schema Validation
```http
POST /api/v1/schema/validate
Content-Type: application/json

Request:
{
    "schema": {
        "tables": [
            {
                "name": string,
                "columns": [
                    {
                        "name": string,
                        "type": string,
                        "constraints": object
                    }
                ],
                "indexes": object[],
                "foreign_keys": object[]
            }
        ],
        "version": string
    }
}

Response:
{
    "valid": boolean,
    "errors": [
        {
            "type": string,
            "message": string,
            "location": object
        }
    ],
    "warnings": object[]
}
```

## 4. Backup Interface

### 4.1 Backup Operations
```http
POST /api/v1/backup/create
Content-Type: application/json

Request:
{
    "type": "full" | "incremental" | "snapshot",
    "destination": {
        "type": "s3" | "gcs" | "azure" | "local",
        "path": string,
        "credentials": object
    },
    "options": {
        "compress": boolean,
        "encrypt": boolean,
        "validate": boolean
    }
}

Response:
{
    "backup_id": string,
    "status": string,
    "start_time": string,
    "size": number,
    "checksum": string
}
```

### 4.2 Recovery Operations
```http
POST /api/v1/backup/restore
Content-Type: application/json

Request:
{
    "backup_id": string,
    "point_in_time": string,
    "options": {
        "validate": boolean,
        "parallel_workers": number,
        "target_database": string
    }
}

Response:
{
    "restore_id": string,
    "status": string,
    "progress": number,
    "estimated_completion": string
}
```

## 5. Admin Interface

### 5.1 Service Management
```http
GET /api/v1/admin/status

Response:
{
    "status": "healthy|degraded|unhealthy",
    "components": {
        "primary": {
            "status": "up|down",
            "connections": number,
            "active_queries": number
        },
        "replica": {
            "status": "up|down",
            "lag": number
        },
        "backup": {
            "status": "up|down",
            "last_success": string
        }
    },
    "metrics": {
        "queries_per_second": number,
        "average_latency": number,
        "storage_used": number
    }
}
```

### 5.2 Configuration Management
```http
PUT /api/v1/admin/config
Content-Type: application/json

Request:
{
    "database": {
        "max_connections": number,
        "connection_timeout": number,
        "idle_timeout": number
    },
    "pools": {
        "min_size": number,
        "max_size": number,
        "idle_timeout": number
    },
    "storage": {
        "max_size": number,
        "auto_extend": boolean,
        "extend_size": number
    }
}
```

## 6. Metrics Interface

### 6.1 Service Metrics

```protobuf
service MetricsService {
    // Performance Metrics
    rpc GetServicePerformance(PerformanceRequest) returns (PerformanceMetrics);
    rpc TrackLatency(LatencyRequest) returns (stream LatencyMetrics);
    
    // Resource Metrics
    rpc GetResourceUtilization(ResourceRequest) returns (ResourceMetrics);
    rpc TrackResourceUsage(UsageRequest) returns (stream UsageMetrics);
    
    // Business Metrics
    rpc GetBusinessMetrics(BusinessMetricsRequest) returns (BusinessMetrics);
    rpc TrackUserActivity(ActivityRequest) returns (stream ActivityMetrics);
}
```

### 6.2 Prometheus Metrics
```
# Connection Metrics
db_connections_total{state="active|idle"} gauge
db_connection_errors_total counter
db_connection_timeouts_total counter

# Query Metrics
db_queries_total{type="select|insert|update|delete"} counter
db_query_duration_seconds{type="*"} histogram
db_query_errors_total{type="*"} counter

# Storage Metrics
db_storage_bytes{type="data|index|wal"} gauge
db_storage_used_percent gauge
db_free_space_bytes gauge

# Service-Specific Metrics
db_portfolio_operations_total{operation="create|read|update|delete"} counter
db_financial_transactions_total{type="deposit|withdrawal|transfer"} counter
db_risk_alerts_total{severity="high|medium|low"} counter
db_backup_duration_seconds{type="full|incremental"} histogram

# Replication Metrics
db_replication_lag_seconds gauge
db_replication_status{replica="*"} gauge
```

## 7. Data Formats

### 7.1 Common Types
```typescript
type Timestamp = string;    // ISO-8601
type UUID = string;        // RFC4122
type JSON = object | array;
type Binary = Buffer;
```

### 7.2 Error Format
```json
{
    "error": {
        "code": string,
        "message": string,
        "details": {
            "query": string|null,
            "parameters": object|null,
            "constraint": string|null
        }
    },
    "transaction_id": string|null,
    "timestamp": string
}
```

## 8. Security

### 8.1 Authentication
```http
Authorization: Bearer {token}
X-API-Key: {api_key}
X-Client-ID: {client_id}
```

### 8.2 Access Control
```yaml
permissions:
  - role: read_only
    operations: [SELECT]
    tables: ["public.*"]
  - role: read_write
    operations: [SELECT, INSERT, UPDATE, DELETE]
    tables: ["public.*"]
  - role: admin
    operations: [ALL]
    tables: ["*"]
```

## 9. Service Level Objectives

### 9.1 Performance SLOs

#### General Performance
- Query Latency: p99 < 50ms
- Write Latency: p99 < 100ms
- Connection Setup: p99 < 10ms
- Backup Time: < 1 hour per TB

#### Service-Specific Performance
- Portfolio Operations: p99 < 75ms
- Financial Transactions: p99 < 150ms
- Risk Calculations: p99 < 200ms
- Analytics Queries: p99 < 300ms
- Query Latency: p99 < 50ms
- Write Latency: p99 < 100ms
- Connection Setup: p99 < 10ms
- Backup Time: < 1 hour per TB

### 9.2 Reliability SLOs

#### Core Reliability
- Service Availability: 99.999%
- Data Durability: 99.999999999%
- Replication Lag: < 10ms
- Backup Success Rate: 99.99%

#### Service-Specific Reliability
- Financial Data Accuracy: 100%
- Risk Alert Delivery: < 1s
- Portfolio Data Consistency: 100%
- Analytics Data Freshness: < 5min
- Service Availability: 99.999%
- Data Durability: 99.999999999%
- Replication Lag: < 10ms
- Backup Success Rate: 99.99%

## 10. Integration Patterns

### 10.1 Connection Management
```typescript
interface ConnectionPool {
    min_size: number;
    max_size: number;
    idle_timeout: number;
    max_lifetime: number;
    validation_query: string;
}
```

### 10.2 Retry Policy
```typescript
interface RetryPolicy {
    max_attempts: number;
    initial_delay: number;
    max_delay: number;
    multiplier: number;
    retryable_errors: string[];
}
```

## 11. Versioning

### 11.1 API Versioning
- Version in URL path: /v1/
- API version header: X-API-Version
- Deprecation header: Deprecated: true

### 11.2 Schema Versioning
- Schema version tracking
- Migration scripts
- Backward compatibility
- Version validation
