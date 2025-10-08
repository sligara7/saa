# Architecture Workflow Visual Reference

## Process Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                   START: Architecture Workflow                       │
│                                                                       │
│  Input: System description document or existing SRDs/ICDs            │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Step 0: Setup       │◄─── Context Refresh
                    │   - Verify tools      │     Before Step
                    │   - Create dirs       │
                    │   - Init tracking     │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Step 1: Analysis      │◄─── Context Refresh
                    │ - Identify hierarchy  │     Before Step
                    │ - List components     │
                    │ - Document metadata   │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │   Decision Point:     │
                    │   What is Level 0?    │
                    └─┬─────────┬─────────┬─┘
                      │         │         │
        ┌─────────────┘         │         └─────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
  System-of-          Individual System         Major Component
  Systems                                            
  L1: Systems         L1: Components           L1: Submodules
  L2: Components      L2: Submodules           L2: Functions/Classes
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                                ▼
        ┌───────────────────────────────────────────────┐
        │ Step 2: Decomposition & Interface Deduction   │◄─── Context Refresh
        │ ⚠️  MOST CRITICAL STEP - HIGH CONTEXT RISK    │     Before Step +
        │                                                │     Every 5 Services
        │ Actions:                                       │
        │ 2.1 Perform RAG retrieval                      │
        │ 2.2 Apply Two-Level Rule                       │
        │ 2.3 Create service_architecture.json (batch 5) │
        │ 2.4 Build system graph                         │
        │ 2.5 Deduce & update interfaces                 │
        │ 2.6 Create/update index.json                   │
        │ 2.7 Generate ICDs                              │
        └───────────────────────┬───────────────────────┘
                                │
                ┌───────────────▼────────────────┐
                │   Level 3 Decomposition?       │
                │   (Check objective triggers)   │
                └──┬─────────────────────────┬───┘
                   │ YES                     │ NO
                   ▼                         │
        ┌──────────────────────┐             │
        │  Step 5.5:           │             │
        │  Interface Impl      │             │
        │  Analysis            │             │
        │  - Request source    │             │
        │  - Analyze code      │             │
        │  - Create Level 3    │             │
        └──────────┬───────────┘             │
                   └─────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Step 3: Parse Global  │
                    │ Architecture          │
                    │ Constraints           │
                    │ (Optional)            │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Step 4: Validate      │◄─── Context Refresh
                    │ Structured Objects    │     Before Step
                    │ - Run validation tool │
                    │ - Fix violations      │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Step 5: Deployment    │◄─── Context Refresh
                    │ Architecture          │     Before Step
                    │ Validation            │
                    │ - Scan configs        │
                    │ - Reconcile logical   │
                    │   with deployment     │
                    └───────────┬───────────┘
                                │
                                ▼
        ┌───────────────────────────────────────────────┐
        │ Step 6: Incremental Validation & Persistence  │◄─── Context Refresh
        │ ⚠️  CRITICAL CHECKPOINT                        │     Before Step
        │                                                │
        │ 6.1 Template validation                        │
        │ 6.2 Graph consistency (detect cycles)          │
        │ 6.3 Resolve architectural issues ◄─┐           │
        │ 6.4 Integration readiness          │ Iterate   │
        │ 6.5 Index validation               │ Until     │
        │ 6.6 Update process log             │ Pass      │
        └───────────────────────┬────────────┘           │
                                │                        │
                        ┌───────▼──────────┐             │
                        │ All validations  │             │
                        │ pass?            │             │
                        └──┬────────────┬──┘             │
                           │ NO         │ YES            │
                           └────────────┘                │
                                                         │
                                ▼                        │
                    ┌───────────────────────┐            │
                    │ Step 7: Water-Tight   │◄─── Context Refresh
                    │ Specification         │     Before Step
                    │ Verification          │
                    │ - Verify completeness │
                    │ - Verify integration  │
                    │   guarantee           │
                    └───────────┬───────────┘
                                │
                                ▼
        ┌───────────────────────────────────────────────┐
        │ Step 8: Generate Implementation-Ready         │◄─── Context Refresh
        │ Artifacts                                      │     Before Step +
        │ ⚠️  COMPLEX - HIGHEST CONTEXT RISK             │     Every 2-3 Svcs
        │                                                │     per Substep
        │ For EACH substep, iterate through ALL services:│
        │                                                │
        │ 8.1 API Contract Definitions                   │
        │     ├─ service_1                               │
        │     ├─ service_2                               │
        │     └─ service_N  ◄── Refresh every 3          │
        │                                                │
        │ 8.2 Data Model Specifications                  │
        │     ├─ service_1                               │
        │     ├─ service_2                               │
        │     └─ service_N  ◄── Refresh every 3          │
        │                                                │
        │ 8.3 Integration Test Specifications            │
        │     └─ (all services)  ◄── Refresh every 3     │
        │                                                │
        │ 8.4 Infrastructure and Deployment              │
        │     └─ (all services)  ◄── Refresh every 2     │
        │                                                │
        │ 8.5 Development Support Materials              │
        │     └─ (all services)  ◄── Refresh every 2     │
        │                                                │
        │ 8.6 Quality Assurance Framework                │
        │     └─ (all services)  ◄── Refresh every 2     │
        └───────────────────────┬───────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Step 9: Completion &  │◄─── Context Refresh
                    │ Build Preparation     │     Before Step
                    │ - Cleanup artifacts   │
                    │ - Create build index  │
                    │ - Create instructions │
                    │ - Create test strategy│
                    └───────────┬───────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │     WORKFLOW COMPLETE         │
                │                               │
                │ Deliverables:                 │
                │ ✓ All service_architecture    │
                │ ✓ All ICDs                    │
                │ ✓ System graph                │
                │ ✓ All Step 8 artifacts        │
                │ ✓ build_ready_index.json      │
                │ ✓ BUILD_INSTRUCTIONS.md       │
                │ ✓ FUNCTIONAL_TEST_STRATEGY.md │
                └───────────────────────────────┘
```

---

## Context Refresh Cycle Visualization

```
┌────────────────────────────────────────────────────────────┐
│                   Context Refresh Cycle                     │
└────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │  Operation 1 │  ─┐
    └──────────────┘   │
                       │
    ┌──────────────┐   │
    │  Operation 2 │   │  Normal Work
    └──────────────┘   │  Track Counter
                       │
    ┌──────────────┐   │
    │  Operation 3 │   │
    └──────────────┘   │
                       │
    ┌──────────────┐   │
    │  Operation 4 │  ─┘
    └──────────────┘
           │
           ▼
    ┌──────────────────┐
    │ TRIGGER REACHED  │ ◄── Automatic or Manual
    │ (Count = 4)      │
    └────────┬─────────┘
             │
             ▼
    ┌─────────────────────────┐
    │  PAUSE ALL OPERATIONS   │
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │  SAVE CURRENT STATE     │
    │  - step_progress.json   │
    │  - working_memory.json  │
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │  RELOAD FOUNDATIONS     │
    │  - definitions.json     │
    │  - templates/*          │
    │  - workflow.json        │
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │  READ CONTEXT FILES     │
    │  - current_focus.md     │
    │  - process_log.md       │
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │  CONFIRM UNDERSTANDING  │
    │  State: System, Step,   │
    │  Substep, Next Action   │
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │  RESET COUNTER TO 0     │
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │  RESUME OPERATIONS      │
    │  Continue with          │
    │  refreshed context      │
    └─────────────────────────┘
             │
             ▼
    Back to Operation 1 with fresh context
```

---

## Decision Tree: Hierarchy Classification (Step 1)

```
                    ┌──────────────────────┐
                    │  Analyze System      │
                    │  Description         │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  What is Level 0?    │
                    └─┬────────┬────────┬──┘
                      │        │        │
    ┌─────────────────┘        │        └──────────────────┐
    │                          │                           │
    ▼                          ▼                           ▼
┌────────────────┐    ┌─────────────────┐      ┌──────────────────┐
│ System-of-     │    │ Individual      │      │ Major Component  │
│ Systems        │    │ System          │      │                  │
└────────┬───────┘    └────────┬────────┘      └────────┬─────────┘
         │                     │                        │
         ▼                     ▼                        ▼
┌────────────────┐    ┌─────────────────┐      ┌──────────────────┐
│ Decompose to:  │    │ Decompose to:   │      │ Decompose to:    │
│                │    │                 │      │                  │
│ L1: Systems    │    │ L1: Major Comp  │      │ L1: Submodules   │
│ L2: Components │    │ L2: Submodules  │      │ L2: Functions    │
└────────┬───────┘    └────────┬────────┘      └────────┬─────────┘
         │                     │                        │
         └─────────────────────┼────────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Proceed to Step 2   │
                    └──────────────────────┘
```

---

## Decision Tree: Level 3 Decomposition (Step 2.2, 5.5)

```
                    ┌──────────────────────────┐
                    │  Analyze Each Interface  │
                    └──────────┬───────────────┘
                               │
                    ┌──────────▼──────────────┐
                    │  Check Objective        │
                    │  Decomposition Triggers │
                    └──────────┬──────────────┘
                               │
    ┌──────────────────────────┼──────────────────────────┐
    │                          │                          │
    ▼                          ▼                          ▼
┌────────────┐          ┌──────────────┐         ┌──────────────┐
│ Interface  │          │ Requires >3  │         │ Safety/      │
│ marked     │    OR    │ method calls │   OR    │ Security     │
│ recommended│          │ or transform │         │ Critical     │
└─────┬──────┘          └──────┬───────┘         └──────┬───────┘
      │                        │                        │
      └────────────────────────┼────────────────────────┘
                               │
    ┌──────────────────────────┼──────────────────────────┐
    │                          │                          │
    ▼                          ▼                          ▼
┌────────────┐          ┌──────────────┐         ┌──────────────┐
│ Coordinates│          │ Bridges with │         │ Performance  │
│ >2 services│    OR    │ external     │   OR    │ bottleneck   │
│            │          │ systems      │         │ (>5 connects)│
└─────┬──────┘          └──────┬───────┘         └──────┬───────┘
      │                        │                        │
      └────────────────────────┼────────────────────────┘
                               │
                    ┌──────────▼──────────────┐
                    │  ANY trigger met?       │
                    └──┬───────────────────┬──┘
                       │ YES               │ NO
                       ▼                   ▼
            ┌──────────────────┐   ┌──────────────┐
            │ Proceed to       │   │ Level 2      │
            │ Level 3          │   │ decomposition│
            │ Decomposition    │   │ sufficient   │
            │                  │   │              │
            │ - Request source │   └──────────────┘
            │ - Analyze code   │
            │ - Create Level 3 │
            │   service_arch   │
            └──────────────────┘
```

---

## Decision Tree: Validation Failure Response (Steps 4, 6)

```
                    ┌──────────────────────────┐
                    │  Validation Failed       │
                    └──────────┬───────────────┘
                               │
                    ┌──────────▼──────────────┐
                    │  Which validation type? │
                    └─┬────┬────┬────┬────┬──┘
                      │    │    │    │    │
         ┌────────────┘    │    │    │    └─────────────┐
         │                 │    │    │                  │
         ▼                 ▼    ▼    ▼                  ▼
┌────────────────┐  ┌─────────────┐  ┌─────────┐  ┌──────────┐
│ Template       │  │ Graph       │  │ Missing │  │ Deploy   │
│ Violation      │  │ Cycles      │  │ Ifaces  │  │ Mismatch │
└────────┬───────┘  └──────┬──────┘  └────┬────┘  └─────┬────┘
         │                 │              │             │
         ▼                 ▼              ▼             ▼
┌────────────────┐  ┌─────────────┐  ┌─────────┐  ┌──────────┐
│ Fix JSON       │  │ Resolve     │  │ Return  │  │ Update   │
│ formatting     │  │ circular    │  │ to      │  │ service_ │
│                │  │ deps        │  │ Step 2  │  │ arch to  │
│ Re-run         │  │             │  │         │  │ match    │
│ validate_      │  │ Use event-  │  │ Deduce  │  │ deploy   │
│ architecture   │  │ driven or   │  │ missing │  │          │
│                │  │ msg queues  │  │ ifaces  │  │ Verify   │
└────────┬───────┘  └──────┬──────┘  └────┬────┘  └─────┬────┘
         │                 │              │             │
         └─────────────────┼──────────────┼─────────────┘
                           │              │
                ┌──────────▼──────────────▼────┐
                │  Re-run Validation            │
                └──────────┬────────────────────┘
                           │
                ┌──────────▼──────────┐
                │  Pass?              │
                └──┬─────────────┬────┘
                   │ YES         │ NO
                   ▼             │
            ┌──────────────┐     │
            │  Proceed to  │     │
            │  Next Step   │     │
            └──────────────┘     │
                                 │
                                 └─► Iterate until pass
```

---

## Step 8 Substep Iteration Pattern

```
Step 8: Generate Implementation-Ready Artifacts

┌─────────────────────────────────────────────────────────┐
│                     Substep Pattern                      │
│                                                          │
│  For EACH substep (8.1 through 8.6):                    │
│                                                          │
│    ┌─────────────────────────────────────┐              │
│    │  Substep 8.X (e.g., API Contracts)  │              │
│    └────────────┬────────────────────────┘              │
│                 │                                        │
│                 ▼                                        │
│    ┌─────────────────────────────────────┐              │
│    │  Iterate through ALL services:      │              │
│    │                                     │              │
│    │  ┌──────────────────────────────┐  │              │
│    │  │  Service 1                   │  │              │
│    │  │  - Create artifact           │  │              │
│    │  │  - Update progress tracker   │  │              │
│    │  │  - operations_count++        │  │              │
│    │  └──────────────────────────────┘  │              │
│    │                                     │              │
│    │  ┌──────────────────────────────┐  │              │
│    │  │  Service 2                   │  │              │
│    │  │  - Create artifact           │  │              │
│    │  │  - Update progress tracker   │  │              │
│    │  │  - operations_count++        │  │              │
│    │  └──────────────────────────────┘  │              │
│    │                                     │              │
│    │  ┌──────────────────────────────┐  │              │
│    │  │  Service 3                   │  │              │
│    │  │  - Create artifact           │  │              │
│    │  │  - Update progress tracker   │  │              │
│    │  │  - operations_count++        │  │              │
│    │  └──────────────────────────────┘  │              │
│    │           │                         │              │
│    │           ▼                         │              │
│    │  ┌──────────────────────────────┐  │              │
│    │  │  CONTEXT REFRESH CHECKPOINT  │◄─┼─── Every    │
│    │  │  (Every 2-3 services)        │  │    2-3 svcs  │
│    │  └──────────────────────────────┘  │              │
│    │           │                         │              │
│    │           ▼                         │              │
│    │  Continue with remaining services  │              │
│    │                                     │              │
│    └─────────────────────────────────────┘              │
│                 │                                        │
│                 ▼                                        │
│    ┌─────────────────────────────────────┐              │
│    │  All services complete for          │              │
│    │  current substep                    │              │
│    └────────────┬────────────────────────┘              │
│                 │                                        │
│                 ▼                                        │
│    Move to next substep (8.X+1)                         │
│                                                          │
└─────────────────────────────────────────────────────────┘

Final result: All 6 substeps × All N services = Complete Step 8
```

---

## Tracking Files Relationship Diagram

```
┌──────────────────────────────────────────────────────────────┐
│              Context Management Files Ecosystem               │
└──────────────────────────────────────────────────────────────┘

┌────────────────────────┐
│  current_focus.md      │ ◄─── READ FIRST, ALWAYS
│                        │      "What am I doing RIGHT NOW?"
│  - Immediate next      │
│    action              │
│  - Current context     │
│  - Step-by-step guide  │
│  - Reminders           │
└───────────┬────────────┘
            │
            │ References
            ▼
┌────────────────────────┐
│ step_progress_         │ ◄─── UPDATE AFTER EVERY OPERATION
│ tracker.json           │      "Where am I in the process?"
│                        │
│  - current_step        │
│  - current_substep     │
│  - services_completed  │
│  - services_remaining  │
│  - operations_since_   │
│    refresh             │
└───────────┬────────────┘
            │
            │ Feeds into
            ▼
┌────────────────────────┐
│  working_memory.json   │ ◄─── SYSTEM STATE PERSISTENCE
│                        │      "What system? What constraints?"
│  - system_name         │
│  - hierarchy_level     │
│  - component_list      │
│  - global_constraints  │
│  - operations_counter  │
└───────────┬────────────┘
            │
            │ Logged in
            ▼
┌────────────────────────┐
│  process_log.md        │ ◄─── DECISION TRAIL
│                        │      "What happened? Why?"
│  - Chronological log   │
│  - Decisions made      │
│  - Issues encountered  │
│  - Resolutions applied │
│  - Context refreshes   │
└───────────┬────────────┘
            │
            │ Summarized in
            ▼
┌────────────────────────┐
│  context_checkpoint.md │ ◄─── QUICK RESTORE POINT
│                        │      "Emergency context summary"
│  - Condensed critical  │
│    context             │
│  - Key decisions       │
│  - Current state       │
└────────────────────────┘

         ALL FILES SUPPORT
                ▼
    ┌───────────────────────┐
    │   Context Refresh     │
    │   Protocol            │
    │                       │
    │   Reload → Restore    │
    │   → Resume            │
    └───────────────────────┘
```

---

## Summary: Key Navigation Points

### Most Critical Steps
1. **Step 2** - Service decomposition and interface deduction (context refresh every 5 services)
2. **Step 6** - Incremental validation (iterative until pass)
3. **Step 8** - Implementation artifacts (context refresh every 2-3 services per substep)

### Context Refresh Mandatory Points
- Before each major step (0-9)
- Every 4 operations
- Every 12 minutes
- When transitioning substeps
- When any degradation signal detected

### Decision Points That Branch Workflow
1. **Step 1**: Hierarchy classification (3 options)
2. **Step 2.2**: Level 3 decomposition triggers (6 trigger types)
3. **Step 3**: Skip if no global constraints
4. **Step 5.5**: Conditional based on triggers
5. **Step 6**: Iterate until validation passes

### Files That Must Always Exist
- `current_focus.md` - Read before every operation
- `step_progress_tracker.json` - Update after every operation
- `working_memory.json` - System state
- `process_log.md` - Decision trail
- `index.json` - Service registry
