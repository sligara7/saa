# LLM Execution Guide for Architecture Workflow

## Quick Start

**YOU ARE HERE TO EXECUTE**: `/home/ajs7/project/saa/architecture_workflow.json`

This guide explains how to efficiently execute the machine-readable architecture workflow while maintaining context and avoiding process derailment.

---

## Core Execution Protocol

### Before EVERY Operation

```
1. READ: systems/<system_name>/current_focus.md (What am I doing RIGHT NOW?)
2. CHECK: systems/<system_name>/step_progress_tracker.json (Where am I?)
3. VERIFY: operations_since_refresh counter <= 4
4. CONFIRM: I know the system name, current step, current substep, next action
```

**If ANY of the above is unclear → EXECUTE CONTEXT REFRESH IMMEDIATELY**

---

## Context Refresh Protocol (CRITICAL)

### When to Refresh

Refresh context when **ANY** of these occur:
- ✅ Operation count >= 4
- ✅ 12+ minutes have passed
- ✅ Transitioning to new step or substep
- ✅ Uncertainty about what to do next
- ✅ Any degradation signal detected (see below)

### Degradation Signals (STOP AND REFRESH)

```
🚨 DEGRADATION DETECTED IF:
- Asking about system name (it's in working_memory.json)
- Forgetting current step/substep (it's in step_progress_tracker.json)
- Repeating questions about completed work
- Using wrong template format
- Creating files in wrong directory
- Not updating progress tracking files
```

### Refresh Sequence

```
1. PAUSE   → Stop all operations immediately
2. SAVE    → Update step_progress_tracker.json and working_memory.json
3. RELOAD  → Read /home/ajs7/project/saa/definitions/architectural_definitions.json
4. RELOAD  → Read all /home/ajs7/project/saa/templates/* files
5. RELOAD  → Read /home/ajs7/project/saa/architecture_workflow.json (this entire workflow)
6. READ    → systems/<system_name>/current_focus.md
7. CONFIRM → State: "System: <name>, Step: <X>, Substep: <Y>, Next action: <specific action>"
8. RESUME  → Continue with confirmed action
```

---

## Workflow Execution Flow

### Step 0: Setup and Verification
- **Goal**: Initialize system directory and verify all tools exist
- **Key Actions**: Check tools, create directories, initialize tracking files
- **Success**: All prerequisites present, tracking files created

### Step 1: System Analysis and Classification
- **Goal**: Determine hierarchy level and list all components
- **Key Decision**: Level 0 classification (System-of-Systems / Individual System / Major Component)
- **Success**: Hierarchy identified, component list complete

### Step 2: Service Decomposition and Interface Deduction (MOST CRITICAL)
- **Goal**: Create all service_architecture.json files and deduce interfaces
- **Key Actions**:
  - Perform RAG retrieval for best practices
  - Apply Two-Level Rule (minimum 2 levels of decomposition)
  - Create service_architecture.json for each component (batch size: 5, then refresh)
  - Build system graph and infer end-to-end interfaces
  - Update ALL services with deduced interfaces
  - Create index.json with absolute paths
  - Generate ICDs using generate_interface_contracts.py
- **Context Management**: Refresh after every 5 services created
- **Success**: All services created, index complete, ICDs generated

### Step 3: Parse Global Architecture Constraints (Optional)
- **Goal**: Document system-wide constraints
- **Skip If**: No ARCHITECTURE.json exists
- **Success**: Constraints documented in working_memory.json

### Step 4: Structured Object Translation
- **Goal**: Validate all service_architecture.json files
- **Key Tool**: validate_architecture.py
- **Success**: All files pass validation

### Step 5: Deployment Architecture Validation
- **Goal**: Reconcile logical architecture with deployment reality
- **Key Actions**: Scan deployment configs, compare with service_architecture.json, update mismatches
- **Success**: Logical and deployment architectures aligned

### Step 5.5: Interface Implementation Analysis (Conditional)
- **Trigger**: Any objective decomposition trigger met
- **Goal**: Create Level 3 decomposition for complex interfaces
- **Success**: Complex interfaces have implementation guidance

### Step 6: Incremental Validation and Persistence (CRITICAL)
- **Goal**: Comprehensive validation with issue resolution
- **Key Actions**:
  - Template validation (validate_architecture.py)
  - Graph validation (system_of_systems_graph.py)
  - Resolve architectural issues (circular dependencies, missing interfaces)
  - Verify integration readiness
  - Validate index.json paths
- **Iterative**: Continue until all validations pass
- **Success**: No critical issues, all validations pass

### Step 7: Water-Tight Specification Verification
- **Goal**: Confirm independent development readiness
- **Success**: All services have complete SRDs, ICDs, and dependencies

### Step 8: Generate Implementation-Ready Artifacts (COMPLEX - HIGH CONTEXT RISK)
- **Goal**: Create comprehensive development artifacts for each service
- **6 Substeps**: API Contracts → Data Models → Integration Tests → Infrastructure → Dev Support → QA
- **Per-Service Iteration**: Complete each substep for ALL services before moving to next substep
- **Context Management**: 
  - Refresh before starting Step 8
  - Refresh after every 2-3 services (varies by substep)
  - Update current_focus.md before each service
- **Success**: All 6 substeps completed for all services

### Step 9: Process Completion and Build Preparation
- **Goal**: Finalize and archive artifacts
- **Key Actions**: Clean up temporary files, create build_ready_index.json, create BUILD_INSTRUCTIONS.md, create test strategy
- **Success**: All completion artifacts created, process documented

---

## Decision Flow Reference

### Hierarchy Classification (Step 1)

```
INPUT: System description
DECISION: What is Level 0?

IF System-of-Systems:
  → Decompose to Level 1 (Individual Systems) → Level 2 (Components)
  → Example: Microservices platform → Services → Modules

IF Individual System:
  → Decompose to Level 1 (Major Components) → Level 2 (Submodules)
  → Example: Web app → Frontend/Backend/DB → React components/Routes/Tables

IF Major Component:
  → Decompose to Level 1 (Submodules) → Level 2 (Functions/Classes)
  → Example: Auth service → User mgmt/Token handling → Classes/Methods
```

### Level 3 Decomposition Triggers (Step 2.2)

```
Apply Level 3 decomposition if ANY trigger met:

1. Interface marked 'recommended' with no existing implementation
2. Interface requires >3 method calls or data transformation
3. Interface is safety/security critical
4. Interface coordinates >2 services
5. Interface bridges with external systems
6. Interface is performance bottleneck (>5 connections)

IF any trigger met → Create Level 3 decomposition
ELSE → Level 2 is sufficient
```

### Validation Failure Response (Steps 4, 6)

```
IF template_violation:
  → Fix service_architecture.json formatting
  → Re-run validate_architecture.py

IF graph_cycles:
  → Resolve circular dependencies
  → Use event-driven pattern or message queues
  → Re-run system_of_systems_graph.py

IF missing_interfaces:
  → Return to Step 2
  → Deduce missing interfaces
  → Update affected services

IF deployment_mismatch:
  → Update service_architecture.json to match deployment reality
  → Verify with deployment configs

IF incomplete_specs:
  → Complete missing SRD/ICD information
  → Request source code references if needed
```

---

## Tool Usage Quick Reference

### validate_architecture.py
```bash
python3 /home/ajs7/project/saa/tools/validate_architecture.py /home/ajs7/project/saa/systems/<system_name>
```
**When**: After creating/updating service files, before proceeding to next step

### system_of_systems_graph.py
```bash
python3 /home/ajs7/project/saa/tools/system_of_systems_graph.py /home/ajs7/project/saa/systems/<system_name> --format json --output systems/<system_name>/system_of_systems_graph.json
```
**When**: Step 6 validation, after major architecture changes

### generate_interface_contracts.py
```bash
python3 /home/ajs7/project/saa/tools/generate_interface_contracts.py /home/ajs7/project/saa/systems/<system_name>/
```
**When**: After interface deduction in Step 2, when interfaces change

### analyze_features.py
```bash
python3 /home/ajs7/project/saa/tools/analyze_features.py /home/ajs7/project/saa/systems/<system_name>/feature_summary.md
```
**When**: Step 1 system analysis, verifying requirements coverage

---

## Key Principles (MEMORIZE THESE)

1. **Use exact template formats** from `/home/ajs7/project/saa/templates/`
2. **Mark implementation_status** (existing/recommended/hypothetical) with justification
3. **Update progress tracking** after EVERY operation
4. **Validate frequently** - after every 5-7 services created
5. **Request source code** when making recommendations
6. **Document ALL decisions** in process_log.md
7. **Absolute paths only** in index.json
8. **Context refresh is mandatory** - not optional

---

## Emergency Context Recovery

If you find yourself completely lost:

```
1. STOP everything
2. READ: /home/ajs7/project/saa/systems/<system_name>/current_focus.md
3. READ: /home/ajs7/project/saa/systems/<system_name>/step_progress_tracker.json
4. READ: /home/ajs7/project/saa/systems/<system_name>/process_log.md (last 20 lines)
5. EXECUTE: Full context refresh protocol (see above)
6. IF STILL UNCLEAR: Ask human for clarification
```

---

## Progress Tracking Example

### step_progress_tracker.json structure:
```json
{
  "system_name": "example_system",
  "current_step": "2",
  "current_substep": "service_creation",
  "services_created": ["service_a", "service_b"],
  "services_remaining": ["service_c", "service_d"],
  "operations_since_refresh": 3,
  "last_updated": "2025-10-08T15:30:00Z"
}
```

### current_focus.md structure:
```markdown
# Current Focus - Updated: 2025-10-08 15:30:00

## IMMEDIATE NEXT ACTION
Create service_architecture.json for service_c

## CURRENT CONTEXT
- System: example_system
- Step: 2 (Service Decomposition and Interface Deduction)
- Substep: service_creation (action 2.3)
- Service: service_c (3 of 4 total)
- Operations since refresh: 3

## WHAT TO DO RIGHT NOW
1. Load service_architecture_template.json
2. Populate fields for service_c based on system description
3. Mark implementation_status appropriately
4. Save to systems/example_system/service_c/service_architecture.json
5. Update step_progress_tracker.json
6. Increment operations_since_refresh
7. Move to service_d or refresh if threshold reached

## DO NOT FORGET
- Use absolute paths
- Mark implementation_status with justification
- Update index.json after creation
```

---

## Workflow Completion Checklist

Before declaring workflow complete, verify:

- [ ] All steps 0-9 completed
- [ ] All services have service_architecture.json
- [ ] index.json contains all services with absolute paths
- [ ] All interfaces have ICDs
- [ ] No critical issues in architectural_issues report
- [ ] All Step 8 substeps completed for all services
- [ ] build_ready_index.json created
- [ ] BUILD_INSTRUCTIONS.md created
- [ ] FUNCTIONAL_TEST_STRATEGY.md created
- [ ] Temporary files archived
- [ ] Final process log entry written

---

## Context Management Math

**Maximum operations between refreshes: 4**

Example operation count:
- Create service_architecture.json: 1 operation
- Update index.json: 1 operation
- Validate with tool: 1 operation
- Update process_log.md: 1 operation
→ Total: 4 operations → **MANDATORY REFRESH**

---

## Summary: The Golden Rules

1. **Read current_focus.md before EVERY operation**
2. **Refresh context every 4 operations (non-negotiable)**
3. **Use exact template formats (no variations)**
4. **Update tracking files after EVERY operation**
5. **Validate after every 5-7 services**
6. **Document EVERYTHING in process_log.md**
7. **When in doubt → Read current_focus.md → Refresh context**

**The workflow JSON is your specification. This guide is your execution strategy.**

---

## FAQ

**Q: Do I really need to refresh context every 4 operations?**  
A: YES. This is non-negotiable. Context drift causes process derailment, especially in Step 8.

**Q: Can I skip Step 8 substeps?**  
A: NO. All 6 substeps are mandatory for independent development guarantee.

**Q: What if validation fails?**  
A: Follow the validation_failure decision flow. Fix issues and re-validate. Do not proceed until validation passes.

**Q: Can I use relative paths in index.json?**  
A: NO. Only absolute paths. This ensures scripts can reliably access artifacts.

**Q: What if I forget the system name?**  
A: This is a degradation signal. STOP. Read working_memory.json. Execute full context refresh.

**Q: How do I know if I'm doing well?**  
A: Check step_progress_tracker.json regularly. If operations_since_refresh is accurate and all tracking files are updated, you're doing well.

---

**Remember: Finite context is your enemy. Systematic context management is your friend.**
