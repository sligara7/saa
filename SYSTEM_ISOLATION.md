# System Isolation Guidelines

## Overview
To prevent cross-system contamination during architecture development, strict isolation rules are enforced for each system under `/home/ajs7/project/saa/systems/`.

## Problem Addressed
During development, the LLM agent accidentally switched from working on the `brain` system to the `dnd` system without proper context boundaries. This could lead to:
- Files created in wrong system directories
- Cross-contamination of artifacts
- Confusion about current system state
- Invalid cross-system references

## Solution

### 1. Mandatory Working Directory Verification
**BEFORE EVERY OPERATION:**
```bash
pwd  # Must equal /home/ajs7/project/saa/systems/<system_name>
```

If working directory doesn't match the system from `working_memory.json`, **STOP immediately** and correct.

### 2. System Context Files Location
All context management files MUST be in the current system directory:
```
/home/ajs7/project/saa/systems/<system_name>/
├── current_focus.md          # Current task focus
├── working_memory.json        # System state and metadata
├── step_progress_tracker.json # Workflow progress
├── process_log.md             # Detailed activity log
└── context_checkpoint.md      # Recovery checkpoint
```

### 3. Cross-Contamination Prevention Rules
- **NEVER** reference files from other system directories
- **NEVER** modify files outside current system directory
- All file paths must be:
  - Relative to current system directory, OR
  - Absolute paths that include and verify the current system_name
- Before reading ANY file, verify path contains correct system_name

### 4. Step/Substep Directory Changes
At the START of EVERY step and substep:
```bash
cd /home/ajs7/project/saa/systems/<system_name>
pwd  # Verify
```

### 5. Degradation Detection
Immediate red flags indicating wrong-system context:
- pwd doesn't match system_name from working_memory.json
- Creating files with paths containing different system names
- Referencing service architectures from other systems
- Reading context files from other system directories

## Workflow Integration

### Updated architecture_workflow.json
The workflow file now includes:

1. **System Isolation Section** (lines 10-22)
   - Mandatory working directory checks
   - Path verification rules
   - Cross-contamination prevention
   - Sanity checks

2. **Enhanced Validation** (lines 30-36)
   - pwd verification before operations
   - Confirmation that no other systems will be modified

3. **New Degradation Signals** (lines 55-57)
   - Wrong system directory detection
   - Cross-system file references
   - pwd mismatch detection

4. **New Cleanup Step 9.0** (lines 644-656)
   - Remove empty/redundant directories
   - Verify directory structure consistency
   - Document cleanup actions

## Usage Example

### Correct Approach
```bash
# Starting work on brain system
cd /home/ajs7/project/saa/systems/brain
pwd  # Verify: /home/ajs7/project/saa/systems/brain

# Read context
cat current_focus.md
cat working_memory.json

# Verify system name matches
# system_name in working_memory.json should be "brain"

# Perform operations...
# All file paths relative to /home/ajs7/project/saa/systems/brain/
```

### Wrong Approach (AVOID)
```bash
# ❌ Working in wrong directory
cd /home/ajs7/project/saa/systems/dnd
cat /home/ajs7/project/saa/systems/brain/current_focus.md  # WRONG!

# ❌ Cross-system file references
cp /home/ajs7/project/saa/systems/dnd/services/api_gateway/service_architecture.json \
   /home/ajs7/project/saa/systems/brain/services/  # WRONG!

# ❌ Not verifying pwd
# Just assuming you're in the right place  # WRONG!
```

## Recovery Procedure

If you detect you're in the wrong system:

1. **STOP immediately** - Don't create/modify any more files
2. **Document the error** in current system's process_log.md
3. **Return to correct system**:
   ```bash
   cd /home/ajs7/project/saa/systems/<correct_system_name>
   pwd  # Verify
   ```
4. **Read working_memory.json** to reestablish context
5. **Read current_focus.md** to understand current task
6. **Resume work** with verified context

## Benefits

1. **Prevents contamination** - Each system develops independently
2. **Clear boundaries** - No ambiguity about which system is active
3. **Easy recovery** - Clear signals when context is lost
4. **Audit trail** - process_log.md tracks all system-specific work
5. **Parallel development** - Multiple systems can coexist without interference

## Implementation Date
2025-10-08

## Related Files
- `/home/ajs7/project/saa/architecture_workflow.json` - Updated workflow
- `/home/ajs7/project/saa/systems/brain/process_log.md` - Cleanup documentation
