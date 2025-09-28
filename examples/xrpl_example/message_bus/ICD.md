# Interface Control Document: Message Bus Service (ICD-MBS-001)

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
This document defines all interfaces for the Message Bus Service, which provides the central communication infrastructure for the XRPL LP Optimization System.

### 1.2 Interface Summary
| Interface | Type | Protocol | Purpose |
|-----------|------|----------|----------|
| AMQP | Primary | AMQP 1.0 | Message exchange |
| REST API | Management | HTTPS | Service management |
| Metrics | Monitoring | Prometheus | System monitoring |
| gRPC | Service Discovery | gRPC | Service registry |

## 2. Message Exchange Interface

### 2.1 AMQP Interface

#### 2.1.1 Connection
```typescript
interface ConnectionConfig {
    host: string;
    port: number;
    vhost: string;
    credentials: {
        username: string;
        password: string;
    };
    tls: {
        enabled: boolean;
        cert_path: string;
        key_path: string;
        ca_path: string;
    };
    heartbeat: number;  // seconds
}
```

#### 2.1.2 Channel Configuration
```typescript
interface ChannelConfig {
    prefetch: number;
    confirm: boolean;
    publisher_confirms: boolean;
    consumer_cancel_notify: boolean;
    persistent: boolean;
}
```

#### 2.1.3 Exchange Types
```typescript
enum ExchangeType {
    DIRECT = "direct",
    TOPIC = "topic",
    FANOUT = "fanout",
    HEADERS = "headers"
}

interface ExchangeConfig {
    name: string;
    type: ExchangeType;
    durable: boolean;
    auto_delete: boolean;
    internal: boolean;
    arguments: Map<string, any>;
}
```

### 2.2 Message Format

#### 2.2.1 Message Envelope
```protobuf
message MessageEnvelope {
    // Message metadata
    string message_id = 1;
    string correlation_id = 2;
    string reply_to = 3;
    int64 timestamp = 4;
    
    // Routing information
    string source_service = 5;
    string destination_service = 6;
    string routing_key = 7;
    
    // Message content
    string content_type = 8;
    bytes content = 9;
    map<string, string> headers = 10;
    
    // Control
    int32 priority = 11;
    int64 expiration = 12;
    bool persistent = 13;
}
```

#### 2.2.2 Message Types
```protobuf
// Command message
message Command {
    string command_id = 1;
    string command_type = 2;
    bytes payload = 3;
    map<string, string> parameters = 4;
}

// Event message
message Event {
    string event_id = 1;
    string event_type = 2;
    bytes payload = 3;
    int64 timestamp = 4;
}

// Query message
message Query {
    string query_id = 1;
    string query_type = 2;
    bytes parameters = 3;
    int64 timeout = 4;
}

// Response message
message Response {
    string response_id = 1;
    string correlation_id = 2;
    bytes payload = 3;
    ResponseStatus status = 4;
}
```

## 3. Management API Interface

### 3.1 REST Endpoints

#### 3.1.1 Service Registration
```http
POST /api/v1/services/register
Content-Type: application/json

Request:
{
    "service_id": string,
    "service_type": string,
    "version": string,
    "endpoints": {
        "amqp": string,
        "http": string,
        "grpc": string
    },
    "capabilities": string[],
    "metadata": object
}

Response:
{
    "registration_id": string,
    "status": string,
    "timestamp": string
}
```

#### 3.1.2 Exchange Management
```http
POST /api/v1/exchanges
Content-Type: application/json

Request:
{
    "name": string,
    "type": string,
    "configuration": {
        "durable": boolean,
        "auto_delete": boolean,
        "internal": boolean,
        "arguments": object
    }
}

Response:
{
    "exchange_id": string,
    "status": string
}
```

#### 3.1.3 Queue Management
```http
POST /api/v1/queues
Content-Type: application/json

Request:
{
    "name": string,
    "configuration": {
        "durable": boolean,
        "exclusive": boolean,
        "auto_delete": boolean,
        "arguments": object
    },
    "bindings": [
        {
            "exchange": string,
            "routing_key": string,
            "arguments": object
        }
    ]
}

Response:
{
    "queue_id": string,
    "status": string
}
```

## 4. Service Discovery Interface

### 4.1 gRPC Service Definition
```protobuf
service ServiceRegistry {
    // Register service
    rpc Register(ServiceRegistration) returns (RegistrationResponse);
    
    // Deregister service
    rpc Deregister(ServiceDeregistration) returns (DeregistrationResponse);
    
    // Discover services
    rpc Discover(ServiceQuery) returns (ServiceList);
    
    // Watch service changes
    rpc Watch(ServiceQuery) returns (stream ServiceChange);
}

message ServiceRegistration {
    string service_id = 1;
    string service_type = 2;
    string version = 3;
    ServiceEndpoints endpoints = 4;
    repeated string capabilities = 5;
    map<string, string> metadata = 6;
}

message ServiceEndpoints {
    string amqp = 1;
    string http = 2;
    string grpc = 3;
}
```

## 5. Metrics Interface

### 5.1 Prometheus Metrics
```
# Message Metrics
message_bus_messages_total{service="*",type="*",status="*"} counter
message_bus_message_size_bytes{service="*",type="*"} histogram
message_bus_message_latency_seconds{service="*"} histogram

# Queue Metrics
message_bus_queue_length{queue="*"} gauge
message_bus_queue_consumers{queue="*"} gauge
message_bus_queue_memory_bytes{queue="*"} gauge

# Service Metrics
message_bus_services_total{status="*"} gauge
message_bus_service_uptime_seconds{service="*"} gauge
message_bus_service_health{service="*"} gauge

# Performance Metrics
message_bus_channel_count gauge
message_bus_connection_count gauge
message_bus_consumer_count gauge
```

### 5.2 Health Check
```http
GET /health

Response:
{
    "status": "up|down|degraded",
    "components": {
        "amqp": "up|down",
        "api": "up|down",
        "discovery": "up|down"
    },
    "metrics": {
        "message_rate": number,
        "queue_depth": number,
        "consumer_count": number
    },
    "version": string,
    "timestamp": string
}
```

## 6. Integration Patterns

### 6.1 Message Exchange Patterns
```typescript
// Request-Reply Pattern
interface RequestReplyConfig {
    timeout: number;        // milliseconds
    retry_count: number;    // number of retries
    reply_queue: string;    // temporary queue name
}

// Publish-Subscribe Pattern
interface PubSubConfig {
    topic: string;
    durable: boolean;
    auto_delete: boolean;
}

// Work Queue Pattern
interface WorkQueueConfig {
    prefetch: number;
    priority: boolean;
    dead_letter: string;
}
```

### 6.2 Error Handling
```typescript
interface ErrorHandling {
    retry: {
        max_attempts: number;
        delay: number;
        backoff: number;
    };
    dead_letter: {
        exchange: string;
        routing_key: string;
    };
    timeout: number;
}
```

## 7. Security

### 7.1 Authentication
```http
# Service Authentication
Authorization: Bearer {service_token}
X-Service-ID: {service_id}
X-Service-Key: {service_key}
```

### 7.2 Access Control
```yaml
permissions:
  exchanges:
    - name: "service.*"
      operations: [declare, delete, bind]
  queues:
    - name: "service.*"
      operations: [declare, delete, consume, publish]
```

## 8. Versioning

### 8.1 Message Versioning
```protobuf
message VersionedMessage {
    int32 version = 1;
    bytes content = 2;
    string content_type = 3;
    string schema_url = 4;
}
```

### 8.2 Interface Versioning
- AMQP Interface: v1.0
- Management API: v1
- Service Discovery: v1
- Metrics: v1
