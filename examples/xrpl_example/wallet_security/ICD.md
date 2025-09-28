# Interface Control Document: Wallet Security Service (ICD-WSS-001)

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
This document defines all external interfaces for the Wallet Security Service, a secure enclave for wallet import and transaction signing following the diode pattern.

### 1.2 Interface Summary
| Interface | Type | Protocol | Purpose |
|-----------|------|----------|----------|
| REST API | External | HTTPS | Wallet operations |
| Message Bus | Internal | AMQP | Event communication |
| HSM | Internal | PKCS#11 | Key management |
| Metrics | Internal | Prometheus | System monitoring |

## 2. REST API Interface

### 2.1 Endpoint Base
```
https://api.{domain}/v1/wallet-security
```

### 2.2 Authentication
- Type: API Key + JWT + mTLS
- Headers: X-API-Key, Authorization
- TLS: Client certificate required

### 2.3 Endpoints

#### 2.3.1 One-Way Secure Import
```http
POST /import/queue
Content-Type: application/json

Request:
{
    "client_id": string,
    "timestamp": string,
    "transition_config": {
        "max_time_minutes": number,
        "max_slippage": string,
        "require_xrp_only": boolean
    }
}

Response:
{
    "import_id": string,
    "encryption_key": string,  # One-time public key
    "signing_key": string,     # One-time signing key
    "transition_id": string
}

POST /import/secure
Content-Type: application/json

Request:
{
    "import_id": string,
    "encrypted_package": {
        "encrypted_data": string,
        "encrypted_key": string,
        "nonce": string,
        "signature": string,
        "verification_hash": string
    }
}

Response:
{
    "wallet_id": string,
    "status": "pending|ready",
    "transition_status": {
        "id": string,
        "status": string,
        "completion_percentage": number
    }
}
```

#### 2.3.2 Transaction Signing
```http
POST /transactions/sign
Content-Type: application/json

Request:
{
    "wallet_id": string,
    "operation_type": string,
    "transaction": {
        "network": "xrpl|axelar",
        "type": string,
        "payload": object,
        "max_fee": string
    },
    "authorization": {
        "operation_id": string,
        "timestamp": string,
        "nonce": string
    }
}

Response:
{
    "signed_transaction": string,
    "signature": string,
    "expiration": string
}
```

#### 2.3.3 Permission Management
```http
PUT /permissions/{wallet_id}
Content-Type: application/json

Request:
{
    "permissions": {
        "operation_type": boolean,
        "max_amount": string,
        "time_limit": string
    }[]
}

Response:
{
    "wallet_id": string,
    "permissions": object,
    "updated_at": string
}
```

## 3. Message Bus Interface

### 3.1 Events Published

#### 3.1.1 Transaction Events
```protobuf
message TransactionSigned {
    string wallet_id = 1;
    string operation_type = 2;
    string transaction_hash = 3;
    string network = 4;
    string timestamp = 5;
}

message WalletTransitionStarted {
    string wallet_id = 1;
    string transition_id = 2;
    string timestamp = 3;
}

message WalletTransitionCompleted {
    string wallet_id = 1;
    string transition_id = 2;
    string timestamp = 3;
}
```

#### 3.1.2 Security Events
```protobuf
message SecurityAlert {
    string wallet_id = 1;
    string client_id = 2;
    string alert_type = 3;
    string severity = 4;
    string description = 5;
    float risk_score = 6;
    map<string, string> metadata = 7;
    string timestamp = 8;

    message WalletChangeMetadata {
        uint32 changes_last_24h = 1;
        uint32 consecutive_changes = 2;
        string last_change = 3;
        float frequency_score = 4;
    }
}

message WalletActivated {
    string wallet_id = 1;
    int32 wallet_version = 2;
    string activation_id = 3;
    string timestamp = 4;
}
```

### 3.2 Events Consumed

```protobuf
message TransitionReadiness {
    string transition_id = 1;
    bool is_ready = 2;
    string status = 3;
    string timestamp = 4;
}

message OperationRequest {
    string operation_id = 1;
    string wallet_id = 2;
    string operation_type = 3;
    bytes operation_data = 4;
    string timestamp = 5;
}
```

## 4. HSM Interface

### 4.1 Key Operations
```typescript
interface HSMOperations {
    // Key management
    generateKey(type: string): Promise<KeyPair>;
    importKey(key: Buffer): Promise<KeyHandle>;
    exportPublicKey(handle: KeyHandle): Promise<Buffer>;
    
    // Signing operations
    sign(handle: KeyHandle, data: Buffer): Promise<Buffer>;
    verify(handle: KeyHandle, signature: Buffer, data: Buffer): Promise<boolean>;
    
    // Encryption operations
    encrypt(handle: KeyHandle, data: Buffer): Promise<Buffer>;
    decrypt(handle: KeyHandle, data: Buffer): Promise<Buffer>;
}
```

### 4.2 Attributes
```typescript
interface KeyAttributes {
    algorithm: string;
    keySize: number;
    usage: string[];
    extractable: boolean;
    expiration: string;
}
```

## 5. Metrics Interface

### 5.1 Prometheus Metrics
```
# Operation Metrics
wallet_operations_total{operation_type="*",status="*"} counter
wallet_operation_duration_seconds{operation_type="*"} histogram
wallet_operation_errors_total{error_type="*"} counter

# Security Metrics
wallet_key_accesses_total{wallet_id="*"} counter
wallet_permission_changes_total{wallet_id="*"} counter
wallet_security_alerts_total{severity="*"} counter

# Performance Metrics
wallet_signing_duration_seconds histogram
wallet_permission_check_duration_seconds histogram
wallet_import_duration_seconds histogram

# Transition Metrics
wallet_transition_duration_seconds histogram
wallet_transition_status{status="*"} gauge

# Rate Limiting Metrics
wallet_import_rate_limited_total{client_id="*"} counter
wallet_import_cooldown_active{client_id="*"} gauge
wallet_import_lockout_total{client_id="*"} counter

# Anomaly Detection Metrics
wallet_change_frequency_score{client_id="*"} gauge
wallet_suspicious_patterns_detected_total{pattern="*"} counter
wallet_security_alerts_triggered_total{severity="*",type="*"} counter
```

### 5.2 Health Check
```http
GET /health

Response:
{
    "status": "up|down|degraded",
    "components": {
        "hsm": "up|down",
        "database": "up|down",
        "cache": "up|down"
    },
    "metrics": {
        "signing_latency": number,
        "success_rate": number,
        "error_rate": number
    },
    "version": string,
    "timestamp": string
}
```

## 6. Data Formats

### 6.1 Common Types
```typescript
type WalletID = string;      // UUID v4
type OperationID = string;   // UUID v4
type TransitionID = string;  // UUID v4
type NetworkType = "xrpl" | "axelar";
type Amount = string;        // Decimal as string
type Timestamp = string;     // ISO-8601 in UTC
```

### 6.2 Error Format
```json
{
    "error": {
        "code": string,
        "message": string,
        "details": object|null,
        "operation_id": string|null
    },
    "request_id": string,
    "timestamp": string
}
```

## 7. Service Level Objectives

### 7.1 Performance SLOs
- Sign Operation: p99 < 100ms
- Permission Check: p99 < 10ms
- Key Access: p99 < 50ms
- Import Process: p99 < 5s

### 7.2 Reliability SLOs
- Service Availability: 99.999%
- Operation Success Rate: 99.999%
- Data Accuracy: 100%

## 8. Security

### 8.1 Authentication Headers
```http
Authorization: Bearer {jwt_token}
X-API-Key: {api_key}
X-Request-ID: {uuid}
X-Operation-ID: {operation_id}
```

### 8.2 Authorization Scopes
```yaml
scopes:
  - wallet.sign        # Sign transactions
  - wallet.import      # Import wallet data
  - wallet.manage      # Manage permissions
```

## 9. Integration Patterns

### 9.1 Circuit Breaker
```typescript
interface CircuitBreaker {
    failure_threshold: number;    // 3 failures
    reset_timeout: number;        // 60 seconds
    half_open_timeout: number;    // 10 seconds
}
```

### 9.2 Retry Policy
```typescript
interface RetryPolicy {
    max_attempts: number;         // 2 attempts
    initial_delay: number;        // 1 second
    max_delay: number;           // 3 seconds
    backoff_multiplier: number;  // 2.0
}
```

### 9.3 Rate Limiting
```typescript
interface RateLimit {
    operations_per_second: number;  // 100 operations
    burst_size: number;            // 200 operations
    timeout: number;               // 30 seconds
}

interface WalletImportRateLimit {
    max_imports_per_hour: number;      // 2 imports
    cooldown_minutes: number;          // 30 minutes
    consecutive_failures_limit: number; // 3 failures
    lockout_duration_minutes: number;   // 60 minutes
}
```

### 9.4 Anomaly Detection
```typescript
interface WalletChangePattern {
    client_id: string;
    change_frequency: number;      // changes per day
    last_change_timestamp: string; // ISO-8601
    consecutive_changes: number;   // reset after cooldown
    risk_score: number;           // 0-100
}

interface SecurityAlert {
    alert_type: "wallet_change" | "anomaly" | "rate_limit" | "suspicious_pattern";
    severity: "low" | "medium" | "high" | "critical";
    description: string;
    client_data: WalletChangePattern;
    timestamp: string;            // ISO-8601
    requires_action: boolean;
}
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


## Amendment: Credentials

### API Changes
No breaking changes. Enhanced functionality available through existing endpoints.

### Implementation Date
2025-09-13
