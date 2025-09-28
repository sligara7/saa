# Interface Control Document: LP Portfolio Service (ICD-LPP-001)

[Previous sections unchanged...]

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
        "fee_limit": decimal,
        "timing_preference": {
            "target_cycle_position": "start" | "middle" | "end",
            "max_wait_ms": number
        }
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
        "timestamp": string,
        "ledger_cycle_metrics": {
            "ledger_index": number,
            "cycle_position": number,
            "cycle_start_time": string
        }
    }
}
```

### 3.1 Events Published

#### 3.1.1 Portfolio Events
```protobuf
message PositionUpdate {
    string position_id = 1;
    string portfolio_id = 2;
    string pool_id = 3;
    double size = 4;
    double value = 5;
    string status = 6;
    string timestamp = 7;
    LedgerExecutionMetrics ledger_metrics = 8;
}

message LedgerExecutionMetrics {
    uint64 ledger_index = 1;
    double cycle_position = 2;  // 0.0 to 1.0, representing position in cycle
    int64 cycle_start_time = 3;
    int64 execution_delay_ms = 4;
}
```

### 4.1 Prometheus Metrics
```
# Existing metrics...

# New Timing Metrics
position_execution_cycle_position gauge
position_execution_delay_ms histogram
position_optimal_timing_success_ratio gauge
position_timing_opportunity_cost gauge
```

[Previous sections unchanged...]