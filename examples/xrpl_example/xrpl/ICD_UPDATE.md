# Interface Control Document: XRPL Service (ICD-XRP-001)

[Previous sections unchanged...]

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

// New message type for ledger timing
message LedgerCycleEvent {
    uint64 ledger_index = 1;
    string ledger_hash = 2;
    int64 cycle_start_time = 3;
    int64 estimated_close_time = 4;
    int64 previous_cycle_duration = 5;
    bool is_cycle_start = 6;
}
```

### 5.2 Request Types
```typescript
// Add timing preference to transaction requests
interface TransactionRequest {
    command: "submit" | "tx" | "transaction_entry";
    tx_blob?: string;
    tx_json?: object;
    transaction?: string;
    timing_preference?: {
        target_cycle_position: "start" | "middle" | "end";
        max_wait_ms: number;
    };
}
```

### 6.1 Prometheus Metrics
```
# Existing metrics...

# New Ledger Timing Metrics
xrpl_ledger_cycle_duration_seconds gauge
xrpl_ledger_cycle_position gauge
xrpl_transaction_submission_timing_seconds histogram
xrpl_optimal_submission_window_seconds gauge
```

[Previous sections unchanged...]