# Step-by-Step: LLM-Driven Translation of System Descriptions to Service JSON Objects (System-Agnostic)

## Architectural Definitions

This process uses standardized architectural definitions based on the Unified Architecture Framework (UAF). All terms, concepts, and hierarchical structures are defined in:

**📁 `/definitions/architectural_definitions.json`**

## Required Tools and Dependencies

**CRITICAL: Before starting the workflow, verify all required tools are available:**

1. **Check Required Scripts:**
   ```bash
   # Core tools
   REQUIRED_TOOLS=(
     "/project/saa/tools/validate_architecture.py"
     "/project/saa/tools/system_of_systems_graph.py"
     "/project/saa/tools/analyze_features.py"
     "/project/saa/tools/cleanup_system.py"
   )
   
   for tool in "${REQUIRED_TOOLS[@]}"; do
     if [ ! -f "$tool" ]; then
       echo "ERROR: Required tool $tool not found"
       exit 1
     fi
   done
   ```

2. **Install Dependencies:**
   ```bash
   # Python packages
   pip3 install networkx matplotlib pygraphviz
   
   # System packages (if needed)
   sudo apt-get install -y graphviz graphviz-dev
   ```

3. **Verify Tool Functionality:**
   ```bash
   # Test each tool
   python3 /project/saa/tools/validate_architecture.py --help
   python3 /project/saa/tools/system_of_systems_graph.py --help
   python3 /project/saa/tools/analyze_features.py --help
   python3 /project/saa/tools/cleanup_system.py --help
   ```

## Standard Templates

To ensure consistent format and prevent integration issues, LLM agents MUST use the standardized templates:

**📁 `/templates/index_template.json`** - Standard format for system index files
**📁 `/templates/service_architecture_template.json`** - Standard format for individual service architecture files
**📁 `/templates/service_architecture_schema.json`** - JSON schema for validation
**📁 `/templates/README.md`** - Complete usage instructions and validation rules

LLM agents MUST reference these templates to ensure consistent terminology for:
- Service vs Interface vs Function distinctions
- Hierarchical structure (Tier 0: System-of-Systems, Tier 1: Systems, Tier 2: Components)
- Communication patterns and dependency types
- UAF-based precision improvements over DoDAF
- Validation criteria and decomposition rules
- File path conventions and JSON structure standards

## Overview: System-Agnostic, LLM-Driven Decomposition and JSON Representation

This process is designed to be agnostic to the domain, language, or granularity of the system being analyzed. It can be applied to:
- Software codebases (from individual functions/packages to high-level services)
- Systems-of-systems (e.g., distributed architectures, warfighting systems, biological systems)
- Any complex system where components ("nodes") and their interfaces ("edges") can be described

The only requirement is that the system can be described in text (free-form, markdown, structured docs, etc.). The LLM agent is responsible for decomposing, structuring, and serializing the system into a set of JSON objects representing each component and its interfaces, ready for further analysis (e.g., with NetworkX or other tools).

**Final Objective:** Create a **water-tight set of individual `service_architecture.json` files** where each service can be built/developed independently with **guaranteed integration success**. By performing comprehensive due diligence on functions (SRDs) and interfaces (ICDs) upfront, we ensure that when individual teams develop their services according to these specifications, the system will integrate seamlessly without interface conflicts or missing dependencies.

## Retrieval Augmented Generation (RAG) Requirements

### Mandatory RAG Integration

**CRITICAL REQUIREMENT**: LLM agents MUST use Retrieval Augmented Generation (RAG) throughout this process to ensure access to the latest information, established best practices, and authoritative technical knowledge.

**RAG Usage Priority:**
1. **Step 2 - HIGHEST PRIORITY**: Decomposition and interface design require current best practices
2. **All Steps**: Latest technical standards, security practices, and architectural patterns
3. **Domain-Specific**: Current state-of-the-art for the specific system domain being analyzed

### RAG Source Categories

**Technical Standards and Best Practices:**
- IEEE standards for system architecture and interfaces
- NIST cybersecurity frameworks and guidelines
- Industry-specific standards (e.g., EPICS for scientific instruments, REST API best practices)
- Cloud-native architecture patterns and microservices design principles
- DevOps and deployment automation best practices

**Latest Technology Information:**
- Current API design patterns and communication protocols
- Security vulnerabilities and mitigation strategies
- Performance optimization techniques and patterns
- Container orchestration and service mesh technologies
- Modern authentication and authorization frameworks

**Domain-Specific Knowledge:**
- Scientific computing and instrument control best practices
- Real-time systems and safety-critical design patterns
- Distributed systems coordination and consensus algorithms
- Web frontend architectures and modern React patterns
- Database design and data management strategies

**Implementation References:**
- Open source project architectures and design decisions
- Production deployment patterns and operational practices
- Testing strategies and quality assurance approaches
- Documentation standards and API specification formats
- Error handling and resilience patterns

### RAG Integration Points

**Before Each Major Step:**
- Query RAG for latest best practices relevant to the current step
- Validate current approach against established patterns
- Identify potential security, performance, or maintainability concerns

**During Decomposition (Step 2):**
- **MANDATORY RAG QUERIES**:
  - "Latest microservices architecture best practices [current year]"
  - "Modern API design patterns and interface standards"
  - "Security best practices for [specific domain] systems"
  - "Performance optimization strategies for [relevant technology stack]"
  - "Container deployment and orchestration current practices"
- Cross-reference proposed interfaces with current industry standards
- Validate communication patterns against established architectural patterns
- Ensure security and safety mechanisms align with current best practices

**During Interface Design:**
- Query for latest API versioning and backward compatibility strategies
- Validate message formats against current standards (OpenAPI, AsyncAPI)
- Check authentication and authorization patterns against current security frameworks
- Ensure error handling follows established best practices

**During Validation Steps:**
- Compare proposed architecture against reference architectures
- Validate deployment strategies against current DevOps practices
- Check testing approaches against current quality assurance standards

### RAG Quality Validation

**Source Authority Requirements:**
- Prioritize official standards bodies (IEEE, NIST, W3C, IETF)
- Use established open source project documentation
- Reference peer-reviewed technical literature when available
- Validate against multiple authoritative sources
- Avoid outdated information (prefer sources <2 years old unless fundamental)

**Knowledge Integration:**
- Synthesize information from multiple sources
- Identify conflicts between sources and document trade-offs
- Adapt general best practices to specific system requirements
- Document rationale for deviations from standard practices

**Continuous Learning:**
- Update RAG knowledge base with lessons learned from each system analysis
- Track emerging patterns and technologies relevant to system architecture
- Maintain awareness of security vulnerabilities and evolving threat models

## LLM Context Management and Memory Strategy

### Critical Context Preservation and Validation

**CONTEXT MANAGEMENT PROTOCOL**: This process includes systematic context refresh, validation, and tracking mechanisms to ensure consistency and completeness throughout the operation. **CRITICAL: With the expanded artifact generation in Step 8, context management becomes even more essential to prevent process derailment.**

#### Mandatory Context Refresh Strategy

**AGGRESSIVE REFRESH SCHEDULE** (Enhanced for Step 8 complexity):
- **Every 3-5 operations** (reduced from 5-7 due to increased complexity)
- **Every 10-12 minutes** (reduced from 15-20 to prevent context drift)
- **Before and after each major step** (mandatory checkpoints)
- **Before generating any new artifact type** (API contracts, data models, etc.)
- **When transitioning between artifact categories** (from core specs to implementation specs)

#### Enhanced Context Management Files
The following files MUST be maintained and updated throughout the process:

```bash
# Initialize enhanced context management files
CONTEXT_FILES=(
  "process_log.md"              # Chronological log of decisions and operations
  "working_memory.json"         # Current state and system requirements
  "context_checkpoint.md"       # Latest context snapshot
  "step_progress_tracker.json"  # NEW: Detailed step-by-step progress tracking
  "artifact_generation_plan.json" # NEW: Comprehensive artifact generation roadmap
  "current_focus.md"            # NEW: What the LLM should be working on RIGHT NOW
)

for file in "${CONTEXT_FILES[@]}"; do
  if [ ! -f "/systems/<system_name>/$file" ]; then
    cp "/templates/${file}_template" "/systems/<system_name>/$file"
  fi
  chmod u+w "/systems/<system_name>/$file"
done
```

#### Mandatory Pre-Operation Context Validation
Before EVERY operation, the LLM agent MUST execute this validation sequence:

```bash
# MANDATORY CONTEXT VALIDATION SEQUENCE
echo "🔍 CONTEXT VALIDATION - $(date)"

# 1. Verify current location in process
CURRENT_STEP=$(jq -r '.current_step' /systems/<system_name>/step_progress_tracker.json)
CURRENT_SUBSTEP=$(jq -r '.current_substep' /systems/<system_name>/step_progress_tracker.json)
echo "Current Position: Step $CURRENT_STEP, Substep: $CURRENT_SUBSTEP"

# 2. Check what should be done next
cat /systems/<system_name>/current_focus.md

# 3. Verify system name and objectives haven't been forgotten
SYSTEM_NAME=$(jq -r '.system_name' /systems/<system_name>/working_memory.json)
echo "Working on system: $SYSTEM_NAME"

# 4. Check operation count since last refresh
OPERATIONS_COUNT=$(jq -r '.operations_since_refresh' /systems/<system_name>/working_memory.json)
echo "Operations since refresh: $OPERATIONS_COUNT"

# 5. Force refresh if threshold exceeded
if [ $OPERATIONS_COUNT -ge 4 ]; then
  echo "🚨 MANDATORY REFRESH TRIGGERED"
  python3 /tools/manage_context.py /systems/<system_name> refresh
fi
```

#### Enhanced Step Progress Tracking

**NEW: `step_progress_tracker.json` Format:**
```json
{
  "system_name": "system_name",
  "current_step": "8",
  "current_substep": "api_contracts",
  "step_8_progress": {
    "api_contracts": {
      "status": "in_progress",
      "services_completed": ["service_a", "service_b"],
      "services_remaining": ["service_c", "service_d"],
      "current_service": "service_c"
    },
    "data_models": {
      "status": "not_started",
      "services_completed": [],
      "services_remaining": ["service_a", "service_b", "service_c", "service_d"],
      "current_service": null
    },
    "integration_tests": {"status": "not_started"},
    "infrastructure": {"status": "not_started"},
    "development_support": {"status": "not_started"},
    "quality_assurance": {"status": "not_started"}
  },
  "completed_steps": ["1", "2", "3", "4", "5", "6", "7"],
  "total_services": 4,
  "last_updated": "2025-10-04T15:30:00Z"
}
```

#### Enhanced Context Refresh Protocol

**MANDATORY CONTEXT REFRESH SEQUENCE** (Enhanced):
```markdown
🔄 **ENHANCED CONTEXT REFRESH PROTOCOL**

**IMMEDIATE ACTIONS (Execute in order):**
1. **PAUSE** - Stop all current operations immediately
2. **SAVE** - Write current state to working_memory.json and step_progress_tracker.json
3. **RELOAD FOUNDATIONS**:
   - Re-read `/definitions/architectural_definitions.json`
   - Re-read `/templates/` directory contents
   - Re-read the main step-by-step process from this document
4. **RESTORE SYSTEM CONTEXT**:
   - System name: [from working_memory.json]
   - Current step: [from step_progress_tracker.json]
   - Current substep: [from step_progress_tracker.json]
   - Current focus: [from current_focus.md]
5. **VERIFY PROGRESS**:
   - Check process_log.md for recent decisions
   - Verify completed artifacts against step_progress_tracker.json
   - Confirm current service being worked on
6. **UPDATE FOCUS**:
   - Write next specific action to current_focus.md
   - Update step_progress_tracker.json with current position
7. **RESUME** - Continue with explicit confirmation of next action

**CONTEXT REFRESH CONFIRMATION REQUIRED:**
After refresh, LLM agent MUST state:
- "Context refreshed for system: [SYSTEM_NAME]"
- "Currently executing: Step [X], Substep: [Y]"
- "Next action: [SPECIFIC ACTION]"
- "Working on service: [SERVICE_NAME] (X of Y total)"
```

#### New Artifact: Current Focus Tracker

**NEW: `current_focus.md` Format:**
```markdown
# Current Focus - Updated: 2025-10-04 15:30:00

## IMMEDIATE NEXT ACTION
Generate API contract definitions for service_c (/systems/system_name/service_c/api_contracts.json)

## CURRENT CONTEXT
- **System**: system_name
- **Step**: 8 (Generate Implementation-Ready Development Artifacts)
- **Substep**: api_contracts (1 of 6 substeps in Step 8)
- **Service**: service_c (3 of 4 total services)
- **Progress**: 2/4 services completed for API contracts

## WHAT TO DO RIGHT NOW
1. Load service_c service_architecture.json
2. Extract interface specifications
3. Generate OpenAPI spec for each interface
4. Save to /systems/system_name/service_c/api_contracts.json
5. Update step_progress_tracker.json
6. Move to service_d or next substep

## DO NOT FORGET
- Use exact template format from /templates/
- Mark implementation_status for each interface
- Include authentication/authorization requirements
- Update progress tracking after completion
```

#### Automatic Step 8 Artifact Generation Management

**Enhanced Artifact Generation Plan:**
```json
{
  "step_8_artifact_plan": {
    "total_substeps": 6,
    "current_substep": 1,
    "substeps": [
      {
        "name": "api_contracts",
        "description": "Create API Contract Definitions",
        "files_per_service": ["api_contracts.json"],
        "estimated_operations": 2,
        "dependencies": ["service_architecture.json"]
      },
      {
        "name": "data_models", 
        "description": "Develop Data Model Specifications",
        "files_per_service": ["data_models.json"],
        "estimated_operations": 2,
        "dependencies": ["service_architecture.json", "api_contracts.json"]
      },
      {
        "name": "integration_tests",
        "description": "Generate Integration Test Specifications", 
        "files_per_service": ["integration_tests.json"],
        "estimated_operations": 2,
        "dependencies": ["api_contracts.json"]
      },
      {
        "name": "infrastructure",
        "description": "Create Infrastructure and Deployment Artifacts",
        "files_per_service": ["infrastructure.json", "config_templates/", "cicd_pipeline.json"],
        "estimated_operations": 3,
        "dependencies": ["service_architecture.json"]
      },
      {
        "name": "development_support",
        "description": "Produce Development Support Materials",
        "files_per_service": ["implementation_guide.md", "stubs/", "dev_setup/"],
        "estimated_operations": 3,
        "dependencies": ["api_contracts.json", "data_models.json"]
      },
      {
        "name": "quality_assurance",
        "description": "Establish Quality Assurance Framework",
        "files_per_service": ["testing_requirements.json", "observability.json", "compliance.json", "runbooks/"],
        "estimated_operations": 4,
        "dependencies": ["all_previous_artifacts"]
      }
    ]
  }
}
```

#### Context Degradation Detection and Recovery

**Enhanced Degradation Detection:**
```bash
# CONTEXT DEGRADATION DETECTION SCRIPT
#!/bin/bash

DEGRADATION_SIGNALS=(
  "Asking about system name when it's in working_memory.json"
  "Forgetting current step when it's in step_progress_tracker.json"
  "Repeating questions about completed artifacts"
  "Using wrong template format"
  "Creating files in wrong directory structure"
  "Forgetting UAF terminology"
  "Not updating progress tracking files"
)

# Check for degradation indicators
for signal in "${DEGRADATION_SIGNALS[@]}"; do
  if detect_degradation_signal "$signal"; then
    echo "🚨 CONTEXT DEGRADATION DETECTED: $signal"
    echo "🔄 EXECUTING EMERGENCY CONTEXT REFRESH"
    python3 /tools/manage_context.py /systems/<system_name> emergency_refresh
    break
  fi
done
```

#### Emergency Context Recovery Protocol

**NEW: Emergency Recovery for Severe Context Loss:**
```bash
# EMERGENCY CONTEXT RECOVERY
python3 /tools/manage_context.py /systems/<system_name> emergency_refresh

# This will:
# 1. Create full context snapshot
# 2. Reload ALL foundational documents
# 3. Regenerate current_focus.md with explicit next steps
# 4. Force LLM to confirm understanding before continuing
# 5. Log emergency recovery event
```

#### Pre-Step Validation
Before starting ANY major step:
```bash
# 1. Review workflow state
cat /systems/<system_name>/process_log.md

# 2. Load architectural definitions
cat /definitions/architectural_definitions.json

# 3. Verify working directory and files
ls -la /systems/<system_name>/

# 4. Check system requirements coverage
python3 /tools/validate_system_coverage.py /systems/<system_name>

# 5. Validate interface consistency
python3 /tools/validate_architecture.py /systems/<system_name>
```

#### Post-Step Validation
After completing ANY major step:
```bash
# 1. Verify file creation/updates
find /systems/<system_name> -type f -mmin -60

# 2. Update interface registry
python3 /tools/validate_architecture.py /systems/<system_name>

# 3. Document decisions
echo "[$(date -Iseconds)] Completed step: $STEP_NAME" >> /systems/<system_name>/process_log.md

# 4. Create context checkpoint
cp /templates/context_checkpoint_template.md /systems/<system_name>/context_checkpoint.md
```

#### Context Refresh Trigger Points and Actions

**Mandatory Refresh Points:**
1. **Every N operations** (recommended: 5-10 service files or 15-20 minutes of processing)
   ```bash
   # Check operation count
   OPERATION_COUNT=$(jq '.context_state.operations_since_refresh' /systems/<system_name>/working_memory.json)
   if [ $OPERATION_COUNT -ge 7 ]; then
     python3 /tools/manage_context.py /systems/<system_name> refresh
   fi
   ```

2. **Before starting each major step** (Steps 1, 2, 3, 4, 5, 6)
   ```bash
   # Perform full context refresh
   python3 /tools/manage_context.py /systems/<system_name> refresh
   
   # Verify system requirements
   python3 /tools/analyze_features.py /systems/<system_name>/dnd_service_feature_summary.md
   python3 /tools/validate_system_coverage.py /systems/<system_name>
   ```

3. **When context appears degraded** (inconsistent naming, forgotten constraints, template violations)
   ```bash
   # Check for context degradation
   python3 /tools/validate_architecture.py /systems/<system_name>
   
   # Force context refresh if issues found
   if [ $? -ne 0 ]; then
     python3 /tools/manage_context.py /systems/<system_name> refresh
   fi
   ```

4. **After handling interruptions** (user questions, clarifications, error corrections)
   ```bash
   # Log interruption
   echo "[$(date -Iseconds)] Interruption handled: $DESCRIPTION" >> /systems/<system_name>/process_log.md
   
   # Refresh context
   python3 /tools/manage_context.py /systems/<system_name> refresh
   ```

5. **Before complex operations** (Level 3 decomposition, graph analysis, deployment validation)
   ```bash
   # Create pre-operation checkpoint
   python3 /tools/manage_context.py /systems/<system_name> checkpoint
   
   # Verify system state
   python3 /tools/validate_architecture.py /systems/<system_name>
   ```

#### Context Refresh Protocol
```markdown
**MANDATORY CONTEXT REFRESH SEQUENCE:**
1. **PAUSE** current operation
2. **RELOAD** architectural definitions from `/definitions/architectural_definitions.json`
3. **REFRESH** template requirements from `/templates/`
4. **RESTATE** current step objectives and constraints
5. **VERIFY** current system context (name, description, progress)
6. **RESUME** operation with full context
```

#### Persistent Context Anchors
- **Process Log File**: `/systems/<system_name>/process_log.md` - tracks decisions, progress, context refresh points
- **Working Memory File**: `/systems/<system_name>/working_memory.json` - stores current state, constraints, decisions
- **Context Checkpoint File**: `/systems/<system_name>/context_checkpoint.md` - condensed version of all critical context




### LLM-Human Partnered, Graph-Based Process
This process leverages an LLM agent and human collaboration to:
- Accept any human-provided input, including:
   - Individual SRDs/ICDs for each component, service, or package (in any format)
   - A high-level system description, architectural goal, or system-of-systems overview (free-form text, markdown, etc.)
- Decompose the system into individual components/services (nodes) and their interfaces (edges) if not already done
- Draft or parse SRDs (system requirements) and ICDs (interface control) for each component/service
- **Build a global system graph to infer all end-to-end paths and interfaces across the entire system**
- **Update all relevant service artifacts in coordinated batches to ensure consistency and completeness**
- Use a domain-appropriate template (e.g., SAA `base_models.py` for software) to build structured objects (e.g., `BaseSRD`, `BaseICD`, `ServiceArchitecture`)
- Serialize each component/service as a JSON file (with versioning) in its folder, designed for both machine-actionability and human readability
- Support both bottom-up (component-by-component) and top-down (system goal) engineering workflows
- Optionally, allow for a high-level architecture object (e.g., `ARCHITECTURE.json`) to capture system-wide goals, constraints, or integration intent





### Detailed Steps (as performed in this project)

1. **Human Input**
   - The human provides either:
     - A high-level system description (text, markdown, etc.)
     - Or, a set of individual SRDs/ICDs for each component/service (in any format)

1.1. **Automated Source Code Integration (Enhanced)**
   - **GitHub Repository Collection**: Request and collect GitHub repository URLs for all mentioned components/services
   - **Automated API Discovery**: Use GitHub API or repository analysis tools to:
     - Scan source code for existing API endpoints, interfaces, and method signatures
     - Extract actual class/method names for interface implementation
     - Identify existing configuration files (nginx.conf, docker-compose.yml, etc.)
     - Parse package.json, requirements.txt, or similar dependency files
   - **Implementation Status Automation**: Automatically categorize interfaces as:
     - **"existing"**: Found in source code with specific file/line references
     - **"needs_verification"**: Mentioned in documentation but not found in code
     - **"missing"**: Required for system function but not implemented
   - **Source Reference Generation**: Create automatic links to source files, API documentation, and configuration examples
   - **Fallback Protocol**: If repositories are private/unavailable, clearly document this limitation and proceed with manual analysis



2. **LLM-Human Partnered, Batch-Oriented Path Inference and Interface Deduction (Graph-Based with RAG Enhancement)**
   
   **🔄 MANDATORY CONTEXT AND RAG REFRESH**: Before starting Step 2, LLM agent MUST:
   1. Reload architectural definitions and templates
   2. Restate system name, description, and decomposition objectives
   3. Confirm current working directory and file structure
   4. Review any previous decisions logged in process_log.md
   5. **🔍 MANDATORY RAG QUERIES**: Execute comprehensive RAG retrieval for:
      - **"Latest microservices architecture patterns and best practices [current year]"**
      - **"Modern API design standards and interface specifications"**
      - **"Current security frameworks and authentication patterns"**
      - **"[Domain-specific] system architecture best practices"** (e.g., "scientific instrument control", "distributed computing", "web application architecture")
      - **"Container orchestration and service deployment strategies"**
      - **"Performance optimization and scalability patterns"**
   6. **📋 RAG SYNTHESIS**: Create a condensed best practices summary (2-3 paragraphs) covering:
      - Key architectural principles identified from RAG sources
      - Security and safety considerations specific to the domain
      - Interface design patterns and communication protocols
      - Deployment and operational best practices
      - Any domain-specific constraints or requirements identified
   
   - The LLM agent and human partner collaborate to:
      - **Identify the starting hierarchy level** (Level 0) of the input system description.
      - **Apply the Two-Level Rule with Conditional Deeper Decomposition:** Decompose the system at least two levels down from the starting level to ensure sufficient granularity for risk and gap analysis:
        - If Level 0 = System-of-Systems → decompose to Level 1 (Individual Systems) → Level 2 (System Components/Packages)
        - If Level 0 = Individual System → decompose to Level 1 (Major Components) → Level 2 (Minor Components/Submodules)
        - If Level 0 = Major Component → decompose to Level 1 (Minor Components) → Level 2 (Functions/Classes/Modules)
        - **Interface Implementation Analysis with Objective Triggers:** Apply Level 3 decomposition when ANY of these objective criteria are met:
          - **Recommended Interface Trigger**: Any interface marked as "recommended" with no existing implementation
          - **Complexity Trigger**: Interface requires >3 method calls or involves data transformation/protocol translation
          - **Safety/Security Trigger**: Interface is critical for safety (coordination service) or security (authentication)
          - **Multi-Service Integration Trigger**: Interface requires coordination between >2 services
          - **External System Bridge Trigger**: Interface bridges internal services with external/non-modifiable systems
          - **Performance Critical Trigger**: Interface is identified as potential bottleneck (>5 connections in graph analysis)
        - **Level 3 Decomposition Process**:
          - Identify the specific classes, methods, or functions within each component that will handle the interface
          - Create additional Level 3 decomposition files for the relevant internal components
          - Document the exact integration points (e.g., "coordination_service.LockManager.acquire_lock() ↔ ophyd_websocket.DeviceManager.check_coordination_status()")
          - This enables precise implementation guidance for development teams
      - **Capture Complete Communication Flows:** Include ALL nodes in end-to-end communication paths, even if they are not primary services or are non-modifiable external systems (e.g., IOCs, databases, legacy systems).
 - **Capture Complete Communication Flows:** Include ALL nodes in end-to-end communication paths, even if they are not primary services or are non-modifiable external systems (e.g., IOCs, databases, legacy systems).
   - **🔍 RAG-ENHANCED INTERFACE DOCUMENTATION**: For every interface or dependency documented in a `service_architecture.json` file, the LLM agent MUST:
     - **Query RAG sources** for current best practices related to the specific interface type and domain
     - **Provide a concise, authoritative summary** (1-2 paragraphs) describing the physiological, technical, or functional basis of the connection
     - **Reference only authoritative sources** enhanced by RAG retrieval: peer-reviewed scientific literature, official standards (IEEE, NIST, RFC), current industry best practices, government/industry documentation, primary technical manuals, and established open source project patterns
     - **Validate against current standards**: Compare proposed interface against latest API design patterns, security frameworks, and communication protocols identified through RAG
     - **Document best practice alignment**: Explicitly note how the interface follows or deviates from current industry best practices, with rationale for any deviations
     - **TV shows, pop culture, or non-authoritative sources MUST NEVER be used** or referenced in any artifact or summary, regardless of system domain
   - Where multiple reputable sources confirm the existence and nature of an interface, the LLM agent MUST mark the `implementation_status` as "existing" and the `source_verification` as "Existing - verified by authoritative sources", rather than "educated guess".
   - If the interface or dependency is debated, hypothetical, or only partially supported by evidence (e.g., dark matter in cosmology, or disputed biological mechanisms), the LLM agent MUST provide a reasoned, evidence-based statement for why the connection is proposed, including references to competing hypotheses or observed effects. The `implementation_status` should be set to "hypothetical" or "educated guess" as appropriate, and the `source_verification` must include a summary of the rationale, context, and any supporting or contradictory studies.
   - The `documentation_links` field MUST include direct links to relevant scientific, technical, or standards-based resources (e.g., NCBI, PubMed, Wikipedia, IEEE, RFCs), and may also include links to review articles, preprints, or debates when authoritative consensus is lacking.
   - This ensures that all generated artifacts are not only machine-actionable, but also traceable to authoritative knowledge or reasoned expert judgment, supporting both human review and downstream automation.
      - **Handle External/Non-Modifiable Systems:** For systems where functionality cannot be changed (e.g., IOCs, third-party services, legacy databases):
        - Create minimal `service_architecture.json` files with basic functionality and interface requirements
        - Document their role in the communication flow and interface contracts
        - Mark them as "external" or "non-modifiable" in their service architecture
        - This ensures complete system-of-systems capture without requiring detailed internal decomposition
      - Decompose the system into components/services (nodes) and their interfaces (edges), using all available documentation.
      - Draft or parse SRDs and ICDs for each component/service at the **final decomposition level** to enable identification of risks, gaps, and integration issues.
   - **RAG-Enhanced Batch Path Inference:**
    - **Enhanced Periodic Context Refresh / Self-Check with RAG Validation:**
       - **AUTOMATIC REFRESH TRIGGERS**: After generating every batch of 5-7 service_architecture.json files, or every 15-20 minutes of processing, the LLM agent MUST execute the full context refresh protocol including RAG validation.
       - **CONTEXT DEGRADATION DETECTION**: Monitor for signs of context loss:
         - Inconsistent naming conventions (switching between camelCase/snake_case)
         - Template format violations or missing required fields
         - Forgotten system constraints or objectives
         - Repetitive questions about previously established facts
         - Deviation from UAF terminology or hierarchical structure
       - **MANDATORY REFRESH SEQUENCE**:
         1. **SAVE CURRENT STATE**: Write current progress to `/systems/<system_name>/working_memory.json`
         2. **RELOAD FOUNDATIONS**: Re-read `/definitions/architectural_definitions.json` and `/templates/`
         3. **RESTORE SYSTEM CONTEXT**: Re-read system description and current objectives
         4. **VERIFY PROGRESS**: Check process_log.md for previous decisions and constraints
         5. **VALIDATE CONSISTENCY**: Ensure current work aligns with established patterns
         6. **RESUME WITH CONFIRMATION**: Explicitly state what will be done next
       - **CONTEXT RESTORATION FILES**:
         - `/systems/<system_name>/process_log.md`: Detailed log of all decisions, issues, and context refresh points
         - `/systems/<system_name>/working_memory.json`: Current state, active constraints, decision cache
         - `/systems/<system_name>/context_checkpoint.md`: Condensed critical context for quick restoration
       - **HUMAN ESCALATION**: If context appears severely degraded or inconsistent, request human intervention for context restoration.
      - Build a global directed graph (e.g., with NetworkX) representing all services **and their constituent components at the final decomposition level** with their dependencies/interfaces.
      - Infer all end-to-end communication paths and required interfaces for the entire system using efficient graph algorithms (BFS, DFS, etc.).
      - Store deduced interfaces and message formats in a central registry or mapping.
   - **RAG-Informed Coordinated Artifact Update:**
         - **🔍 Pre-Update RAG Validation**: Before updating service_architecture.json files, query RAG for:
           - Current interface design patterns for the specific communication type
           - Latest message format standards (JSON Schema, OpenAPI, AsyncAPI)
           - Security best practices for the identified communication patterns
           - Error handling and resilience patterns for the interface type
         - **Apply RAG-Informed Updates**: For each inferred path or interface, update all relevant `service_architecture.json` files incorporating RAG-identified best practices
         - **Ensure Standards Compliance**: The format and content of messages/data must be consistent with current industry standards and across all services in a path, unless a transformation is explicitly specified at an intermediate service
         - **Document Best Practice Rationale**: Include brief justification for interface design choices based on RAG-retrieved best practices
         - Use the central registry to synchronize updates and avoid redundant or inconsistent changes.
         - **Directory Structure and Indexing:**
             - All artifacts for a given system-of-systems are stored under `/systems/<system_of_systems_name>/`.
             - Each individual service/component has its own subdirectory:
                `/systems/<system_of_systems_name>/<individual_system_A>/service_architecture.json`
             - **For hierarchical decomposition (Two-Level Rule), create nested directories reflecting the decomposition levels:**
                - Level 1: `/systems/<system_of_systems_name>/<level_1_component>/service_architecture.json`
                - Level 2: `/systems/<system_of_systems_name>/<level_1_component>/<level_2_component>/service_architecture.json`
             - **Include external/non-modifiable systems:** Create service_architecture.json files for ALL nodes in communication flows, including IOCs, databases, legacy systems, etc., even if they are not modifiable
             - The LLM agent must create and update a central index file that maps each component at all levels (including external systems) to the absolute path of its `service_architecture.json`:
                `/systems/<system_of_systems_name>/index.json`
             - This index file must be updated automatically as new or updated `service_architecture.json` files are created, and must always reflect the correct, directly usable absolute path for each component artifact at all decomposition levels (never use relative paths).
             - Any system-level graphs or additional artifacts should be saved at:
                `/systems/<system_of_systems_name>/`
   - **Human-LLM Review Loop:**
      - Artifacts (`service_architecture.json` files and the global graph) are designed to be both machine-actionable (for LLMs/automation) and human-readable (for review, collaboration, and traceability).
      - The human can review, edit, or annotate artifacts at any stage, and the LLM agent can incorporate feedback in the next batch update.
   - **Result:**
      - The process produces a set of **water-tight JSON artifacts** where each service specification is complete and unambiguous.
      - Each `service_architecture.json` contains all necessary information for independent development: complete functional requirements (SRD), validated interface contracts (ICD), and all deduced dependencies.
      - The artifacts are both machine-actionable (for LLMs/automation) and human-readable (for review, collaboration, and traceability).
      - **Independent Development Guarantee:** Teams can develop services independently according to their specifications, with confidence that system integration will succeed because all interface contracts have been validated and coordinated.
   
   - **Generate Interface Contract Documents (ICDs):**
      - After interface deduction, run `generate_interface_contracts.py` to create detailed Interface Contract Documents (ICDs)
      - Each ICD specifies complete input/output contracts, error handling, timing constraints, and integration test scenarios
      - ICDs are system-agnostic and support software, biological, social, and mechanical systems
      - Generated ICDs enable LLM-driven independent development with guaranteed integration success
      ```bash
      python3 /tools/generate_interface_contracts.py /systems/<system_name>/
      # Creates /systems/<system_name>/interfaces/<interface_id>.json for each interface
      # Creates interfaces_summary.json with overview of all interface contracts
      ```

3. **Parse High-Level Architecture Constraints (Preparation for Analysis):**
    - Read and parse `ARCHITECTURE.json` (or equivalent) for global system constraints and requirements
    - Represent high-level architecture goals as a structured object/JSON if provided
    - Prepare constraint validation rules for the automated analysis phase
    - **Purpose:** These constraints will be used in step 4 to identify compliance violations and architectural mismatches

4. **Translate to Structured Objects (Post-Interface Deduction)**
   - Use a domain-appropriate template (e.g., SAA's `base_models.py` for software)
   - For each component/service, create a structured object (e.g., `ServiceArchitecture` for software, or a domain-appropriate equivalent)
   - Include all deduced interfaces and message formats from the coordinated batch inference process

5. **Systematic Deployment Architecture Validation (Enhanced with RAG Best Practices)**
   - **🔍 RAG-Informed Deployment Analysis**: Before validation, query RAG for:
     - **"Current DevOps and deployment best practices [current year]"**
     - **"Container orchestration security and performance patterns"**
     - **"API gateway and reverse proxy configuration standards"**
     - **"Infrastructure as Code best practices and validation techniques"**
     - **"Service mesh and microservices deployment patterns"**
   - **Automated Deployment Artifact Discovery with Standards Validation**: Systematically scan and validate against RAG-identified best practices:
     - **Container Orchestration**: Docker Compose files, Kubernetes manifests, Helm charts (validate against current K8s best practices)
     - **Infrastructure as Code**: Ansible playbooks, Terraform configs, CloudFormation templates (check against IaC security standards)
     - **Reverse Proxies**: nginx.conf, Apache configs, HAProxy configurations (validate against performance and security best practices)
     - **Service Mesh**: Istio, Linkerd, Consul Connect configurations (align with current service mesh patterns)
     - **CI/CD Pipelines**: GitHub Actions, Jenkins, GitLab CI deployment scripts (validate against current CI/CD security practices)
   - **RAG-Enhanced Architecture Reconciliation**: Compare logical architecture with deployment reality using current best practices:
     - Parse nginx upstream definitions to identify actual service routing (validate against load balancing best practices)
     - Extract service dependencies from Docker Compose or K8s service definitions (check against microservices design patterns)
     - Identify load balancer rules and traffic routing policies (validate against current traffic management standards)
     - Detect authentication layers, API gateways, and security boundaries (verify against current security frameworks)
   - **Best Practice Compliance Warnings**: Generate warnings based on RAG-identified best practices:
     - Logical dependencies that don't match deployment routing
     - Missing services in deployment that exist in logical architecture
     - Security boundary violations (direct access bypassing gateways)
     - Protocol mismatches (HTTP logical but HTTPS deployment)
     - **Performance anti-patterns** identified through RAG analysis
     - **Security vulnerabilities** based on current threat models
     - **Operational complexity** issues identified from DevOps best practices
   - **Standards-Compliant Architecture Correction**: Update `service_architecture.json` files incorporating RAG-identified improvements
   - **Best Practice Documentation**: Document how deployment follows or deviates from current industry standards
   - **Example Validation**: Automatically detect that nginx proxies ALL traffic and update client dependencies accordingly

5.5. **Interface Implementation Analysis (Conditional Deeper Decomposition)**
   - **Identify Complex Interfaces**: For interfaces between components where implementation details are unclear, perform LLM-guided analysis:
     - **Request Source Code References**: If source code or documentation is not available, ask the human to provide:
       - GitHub repository URLs for relevant components
       - Documentation links or file paths
       - Existing API specifications or interface contracts
     - **Analyze Available Sources**: When references are provided, analyze the actual code/documentation to identify:
       - Specific classes, methods, or functions that will handle the interface
       - Existing APIs and their sufficiency for the required interface
       - Current implementation patterns and conventions
     - **Distinguish Facts from Recommendations**: Clearly categorize all interface specifications as:
       - **"existing"**: Based on actual source code analysis
       - **"recommended"**: LLM-suggested solutions for gaps in architecture with specific justification (e.g., "per REST API best practices", "following microservices pattern", "industry standard for authentication", "common pattern for event-driven architectures")
       - **"hypothetical"**: Educated guesses when source references are unavailable, with context explaining the reasoning (e.g., "typical implementation for this functionality", "inferred from similar systems", "standard approach for this use case")
   - **Conditional Level 3 Decomposition**: When interface complexity requires it, create additional decomposition:
     - Create subdirectories: `/systems/<system_name>/<component>/<internal_module>/`
     - Generate `service_architecture.json` files for internal modules (classes, significant methods)
     - **Mark implementation status** in each file: existing, recommended, or hypothetical
     - Document precise integration points and call flows with appropriate confidence levels
   - **Implementation Guidance Generation**: For each complex interface, create implementation specifications:
     - Exact method signatures needed (mark as existing/recommended/hypothetical)
     - Data structures to be shared
     - Error handling patterns
     - Integration testing requirements
     - **Source references** when available
   - **Example Analysis**: For coordination-service ↔ ophyd-websocket interface:
     ```
     coordination_service.LockManager.acquire_lock(beamline_id, user_id, duration) [RECOMMENDED - standard pattern for resource locking in distributed systems, follows semaphore design pattern]
     ↔ 
     ophyd_websocket.DeviceManager.check_coordination_status() → bool [HYPOTHETICAL - typical implementation for coordination-aware device management, common in scientific instrument control systems]
     ophyd_websocket.DeviceManager.block_device_commands() when locked [HYPOTHETICAL - standard safety pattern to prevent conflicts during exclusive operations]
     ```
   - **Request Clarification**: When making recommendations or hypothetical suggestions, explicitly ask:
     - "Please provide GitHub repository or documentation links for [component_name] to verify existing interfaces"
     - "This interface specification is recommended - please confirm if this aligns with your requirements"
     - "Unable to locate source code for [component] - these are suggested interfaces based on functional requirements"

6. **Incremental Validation and Persistence (Enhanced with RAG Quality Assurance)**
   - **🔍 RAG-Informed Validation Strategy**: Before validation, query RAG for:
     - **"Software architecture validation and testing best practices"**
     - **"API contract testing and integration validation techniques"**
     - **"DevOps quality assurance and deployment validation methods"**
     - **"Security architecture review and validation frameworks"**
   - **Validation Checkpoint System with Standards Compliance**: Implement validation at multiple stages:
     - **Post-Step 2 Validation**: Validate initial template conformance, hierarchical structure, and adherence to RAG-identified architectural principles
     - **Post-Step 4 Validation**: Validate graph consistency, detect cycles, verify communication paths against current API design patterns
     - **Post-Step 5 Validation**: Validate deployment architecture alignment, source code references, and compliance with DevOps best practices
     - **Final Validation**: Comprehensive validation incorporating all RAG-identified quality criteria and integration readiness
   
   - **Standards-Compliant Template Validation**:
     - Serialize each structured object to a JSON file (e.g., `service_architecture.json`) in the component/service's folder
     - **Use EXACT template format from `/templates/service_architecture_template.json`** enhanced with RAG-identified improvements
     - Include a `version` field using semver-date versioning (e.g., `1.0+2025-09-28`)
     - **RAG-Enhanced Schema Validation**: Validate against both template requirements and current industry standards
     - Run `python3 validate_templates.py systems/<system_name>/` after each batch of files with RAG-informed validation rules
   
   - **Best Practice Graph Consistency Validation**:
     - Build and analyze system graph after each major component addition using RAG-identified graph analysis patterns
     - Detect and resolve circular dependencies immediately
     - Validate communication path completeness and interface consistency
   
   - **Integration Readiness Validation**:
     - Verify all dependencies are resolvable within the system
     - Confirm all interfaces have corresponding implementations or clear specifications
     - Validate external system interfaces are properly marked and documented
   
   - **Index Management with Validation**:
     - **Automatically update a central JSON index file (e.g., `service_architecture_index.json`) with the absolute path to each `service_architecture.json` as it is created.**
     - **Use EXACT template format from `/templates/index_template.json`**
     - Validate index completeness and path accuracy at each checkpoint
     - The index must store the correct, directly usable absolute path for each file, so that downstream scripts can reliably access the artifacts without ambiguity or path errors.

6. **Artifacts**
   - JSON files for each component/service's combined SRD/ICD object (with versioning and deduced interfaces)
   - In-memory structured objects for each component/service
   - A global system graph (e.g., NetworkX DiGraph) with all services and their interfaces
   - **A central `service_architecture_index.json` file mapping each service to the absolute path of its JSON artifact (must be correct and directly usable by all scripts)**
   - A central interface registry or mapping for consistency validation
   - Parsed system constraints from `ARCHITECTURE.json` or equivalent (if provided)
   - All artifacts designed for both machine-actionability (LLM processing) and human readability (review and collaboration)

7. **Final Deliverable: Water-Tight Service Specifications for Independent Development**
   - **Complete Service Specifications:** Each `service_architecture.json` file contains everything needed for independent development:
      - Comprehensive functional requirements (SRD)
      - Validated interface contracts with exact message formats and protocols (ICD)
      - All required dependencies and their interface specifications
      - Security, performance, and compliance requirements
   - **Integration Guarantee:** Because all interfaces have been coordinated and validated across the entire system:
      - Services developed according to their specifications will integrate without interface conflicts
      - Message formats are consistent across all communication paths
      - All required intermediate interfaces have been identified and specified
      - Dependencies are complete and unambiguous
   - **Independent Development Ready:** Development teams can work in parallel on their services with confidence that the final system integration will succeed

8. **Generate Implementation-Ready Development Artifacts**
   - **Create API Contract Definitions**: For each service interface, generate OpenAPI/AsyncAPI specifications with:
     - Complete endpoint definitions with request/response schemas
     - Authentication and authorization requirements
     - Error handling and status code specifications
     - Rate limiting and throttling configurations
   - **Develop Data Model Specifications**: Create comprehensive data architecture artifacts:
     - Database schemas with relationships and constraints
     - Data validation rules and business logic specifications
     - Data flow diagrams and transformation requirements
     - Caching strategies and persistence layer definitions
   - **Generate Integration Test Specifications**: Create detailed testing frameworks:
     - Contract testing scenarios for each interface
     - Mock service definitions for external dependencies
     - Performance benchmarks and SLA requirements
     - End-to-end integration test scenarios
   - **Create Infrastructure and Deployment Artifacts**: Develop operations-ready specifications:
     - Resource requirements and scaling parameters
     - Environment-specific configuration templates
     - CI/CD pipeline definitions and deployment strategies
     - Monitoring, logging, and alerting configurations
   - **Produce Development Support Materials**: Generate developer-friendly resources:
     - Implementation guides with technology recommendations
     - Code stubs and mock implementations
     - Development environment setup instructions
     - Architecture decision records with rationale
   - **Establish Quality Assurance Framework**: Create comprehensive QA artifacts:
     - Testing requirements and coverage specifications
     - Security and compliance requirements
     - Monitoring and observability definitions
     - Operational runbooks and troubleshooting guides

## Process Artifacts

### **Core Architecture Specifications**
- JSON files for each component/service's combined SRD/ICD object (with versioning and deduced interfaces) in their respective subdirectories
- **Hierarchical JSON files following the Two-Level Rule decomposition** (e.g., separate files for Level 1 and Level 2 components)
- In-memory structured objects for each component/service at all decomposition levels
- A global system graph (e.g., NetworkX DiGraph) with all components at the final decomposition level and their interfaces, saved in `/systems/<system_of_systems_name>/`
- **A central `index.json` file mapping each component at all decomposition levels to the absolute path of its JSON artifact, saved in `/systems/<system_of_systems_name>/index.json`**
- A central interface registry or mapping for consistency validation
- Parsed system constraints from `ARCHITECTURE.json` or equivalent (if provided)

### **Implementation-Ready Technical Specifications**
- **API Contract Definitions** (`/systems/<system_name>/<service>/api_contracts.json`):
  - OpenAPI/AsyncAPI specifications for each service interface
  - Message schemas with validation rules
  - Error response definitions and status codes
  - Authentication/authorization requirements per endpoint
- **Data Model Specifications** (`/systems/<system_name>/<service>/data_models.json`):
  - Database schemas with field types, constraints, and relationships
  - Data validation rules and business logic constraints
  - Data flow diagrams and transformation specifications
  - Cache strategies and data persistence requirements
- **Integration Test Specifications** (`/systems/<system_name>/<service>/integration_tests.json`):
  - Test scenarios for each interface with expected inputs/outputs
  - Mock service definitions for external dependencies
  - Performance benchmarks and SLA requirements
  - Contract testing specifications for interface validation

### **Deployment and Operations Artifacts**
- **Infrastructure Requirements** (`/systems/<system_name>/<service>/infrastructure.json`):
  - Resource requirements (CPU, memory, storage, network)
  - Scaling parameters (min/max instances, auto-scaling triggers)
  - Environmental dependencies (databases, message queues, external services)
  - Security requirements (certificates, secrets, network policies)
- **Configuration Templates** (`/systems/<system_name>/<service>/config_templates/`):
  - Environment-specific configuration files (dev/staging/prod)
  - Feature flags and environment variables
  - Logging and monitoring configuration
  - Service discovery and load balancing settings
- **CI/CD Pipeline Specifications** (`/systems/<system_name>/<service>/cicd_pipeline.json`):
  - Build and deployment scripts
  - Quality gates and testing requirements
  - Deployment strategies (blue-green, canary, rolling)
  - Rollback procedures and health checks

### **Development Support Artifacts**
- **Implementation Guidance** (`/systems/<system_name>/<service>/implementation_guide.md`):
  - Technology stack recommendations with rationale
  - Code structure and design pattern suggestions
  - Key algorithms and business logic implementation notes
  - Performance optimization guidelines
- **Interface Stubs and Mocks** (`/systems/<system_name>/<service>/stubs/`):
  - Stub implementations for external service interfaces
  - Mock data generators for testing
  - Service simulation tools for integration testing
  - API client libraries and SDKs
- **Development Environment Setup** (`/systems/<system_name>/<service>/dev_setup/`):
  - Local development environment configuration
  - Docker compose files for service dependencies
  - Development database schemas and seed data
  - IDE configurations and debugging setups

### **Quality Assurance Artifacts**
- **Testing Requirements** (`/systems/<system_name>/<service>/testing_requirements.json`):
  - Unit test coverage requirements and critical path identification
  - Integration test scenarios with dependency mapping
  - Performance test specifications and acceptance criteria
  - Security test requirements and vulnerability scanning
- **Monitoring and Observability** (`/systems/<system_name>/<service>/observability.json`):
  - Metrics definitions and alerting thresholds
  - Logging specifications and structured log formats
  - Distributed tracing requirements
  - Health check endpoints and monitoring dashboards
- **Compliance and Security** (`/systems/<system_name>/<service>/compliance.json`):
  - Security requirements and threat model analysis
  - Regulatory compliance requirements (GDPR, HIPAA, etc.)
  - Audit trail specifications
  - Data privacy and encryption requirements

### **Process Management Files**
- **Context Management Files**:
  - `/systems/<system_name>/process_log.md`: Chronological log of decisions, context refreshes, and issue resolution
  - `/systems/<system_name>/working_memory.json`: Current state, active constraints, decision cache for context restoration
  - `/systems/<system_name>/context_checkpoint.md`: Condensed critical context summary for quick LLM restoration
- **Cross-Service Integration Matrix** (`/systems/<system_name>/integration_matrix.json`):
  - Service dependency mapping with interface versions
  - Integration testing coordination requirements
  - Deployment order and rollback dependencies
  - Cross-service transaction and consistency requirements

### **Validation and Verification Artifacts**
- **Interface Validation Scripts** (`/systems/<system_name>/validation/`):
  - Automated contract testing tools
  - Interface compatibility verification scripts
  - End-to-end integration test suites
  - Performance and load testing frameworks
- **System Integration Verification** (`/systems/<system_name>/integration_verification.json`):
  - System-wide test scenarios and acceptance criteria
  - Service mesh configuration and validation
  - End-to-end workflow verification
  - Production readiness checklists

### **Documentation and Knowledge Transfer**
- **Architecture Decision Records** (`/systems/<system_name>/adr/`):
  - Documented architectural decisions with rationale
  - Trade-off analysis and alternative options considered
  - Implementation constraints and assumptions
  - Review and approval history
- **Runbooks and Operational Procedures** (`/systems/<system_name>/<service>/runbooks/`):
  - Deployment procedures and rollback instructions
  - Troubleshooting guides and common issues
  - Scaling and capacity planning procedures
  - Disaster recovery and business continuity plans

All artifacts designed for both machine-actionability (LLM processing) and human readability (review and collaboration)

---


## Enhanced LLM Prompt Template (System-Agnostic with Aggressive Context Management)


> **Prompt:**
> "You are a systems architect assistant partnering with a human to analyze a system-of-systems using an enhanced automated workflow. **CRITICAL: You MUST implement AGGRESSIVE context refresh to prevent losing track of objectives during complex operations, especially during Step 8 artifact generation.**
> 
> **MANDATORY CONTEXT VALIDATION BEFORE EVERY OPERATION:**
> - **Read current_focus.md first** - This tells you EXACTLY what to do next
> - **Check step_progress_tracker.json** - Verify your current position in the process
> - **Verify working_memory.json** - Confirm system name and constraints
> - **Operations counter check** - If >3 operations since refresh, STOP and refresh context
> 
> **ENHANCED CONTEXT MANAGEMENT PROTOCOL:**
> - **AGGRESSIVE REFRESH SCHEDULE**: Every 3-5 operations, every 10-12 minutes, before each artifact type
> - **MANDATORY VALIDATION**: Before every operation, confirm current step/substep/service
> - **CONTEXT REFRESH TRIGGERS**: 
>   - Operation count ≥4 (reduced threshold)
>   - Any uncertainty about current task
>   - Switching between artifact types
>   - After completing any service's artifacts
>   - When asking about system name/step (degradation signal)
> - **REFRESH SEQUENCE**: (1) PAUSE, (2) Save state to step_progress_tracker.json, (3) Reload process document, (4) Read current_focus.md, (5) Confirm next action, (6) Resume
> - **DEGRADATION DETECTION**: Monitor for forgotten system names, repeated questions, wrong templates, incorrect file paths
> - **PERSISTENT MEMORY**: Maintain enhanced tracking files - step_progress_tracker.json, current_focus.md, artifact_generation_plan.json
> 
> **STEP 8 ARTIFACT GENERATION PROTOCOL:**
> - **6 substeps total**: api_contracts → data_models → integration_tests → infrastructure → development_support → quality_assurance
> - **Per-service iteration**: Complete each substep for ALL services before moving to next substep
> - **Progress tracking**: Update step_progress_tracker.json after each service completion
> - **Current focus updates**: Write next specific action to current_focus.md before each operation
> - **Template compliance**: Use exact formats from /templates/ directory
> 
> **MANDATORY CONFIRMATION PROTOCOL:**
> Before starting ANY operation, state:
> - "System: [SYSTEM_NAME]"
> - "Step: [CURRENT_STEP], Substep: [CURRENT_SUBSTEP]"  
> - "Service: [CURRENT_SERVICE] ([X] of [Y] total)"
> - "Next Action: [SPECIFIC_ACTION]"
> - "Operations since refresh: [COUNT]"
> 
> Use the exact template structures from `/templates/index_template.json` and `/templates/service_architecture_template.json` for all generated files. 
> 
> **ENHANCED SOURCE CODE INTEGRATION**: Request GitHub repository URLs for all components and use automated analysis to discover existing APIs, interfaces, and configurations. Automatically categorize interfaces as 'existing' (found in source code), 'needs_verification' (mentioned in docs but not found), or 'missing' (required but not implemented). Generate automatic links to source files and configuration examples.
> 
> **OBJECTIVE DECOMPOSITION TRIGGERS**: Apply Level 3 decomposition when ANY objective criteria are met: (1) Interface marked as 'recommended' with no existing implementation, (2) Interface requires >3 method calls or data transformation, (3) Interface is safety/security critical, (4) Interface coordinates >2 services, (5) Interface bridges with external systems, (6) Interface is performance bottleneck (>5 connections).
> 
> **SYSTEMATIC DEPLOYMENT VALIDATION**: Automatically scan and parse deployment artifacts (Docker Compose, K8s manifests, nginx.conf, Ansible playbooks) to validate logical architecture against deployment reality. Generate warnings for mismatches and automatically correct service dependencies to reflect true deployment patterns.
> 
> **INCREMENTAL VALIDATION CHECKPOINTS**: Implement validation at multiple stages: (1) Post-decomposition: template conformance and hierarchy, (2) Post-graph-building: cycles and communication paths, (3) Post-deployment-validation: architecture alignment, (4) Final: comprehensive integration readiness. Run validation scripts after each checkpoint and resolve issues before proceeding.
> 
> **EMERGENCY CONTEXT RECOVERY**: If you ever find yourself uncertain about what to do next, immediately:
> 1. Read /systems/<system_name>/current_focus.md
> 2. Check /systems/<system_name>/step_progress_tracker.json  
> 3. Execute context refresh if still uncertain
> 4. Ask human for clarification only as last resort
> 
> Given the following system description or SRDs/ICDs, identify the starting hierarchy level (Level 0) and apply the Two-Level Rule with objective decomposition triggers. **Capture complete communication flows** including external/non-modifiable systems. Build a global graph and infer all communication paths using graph algorithms. **Generate precise implementation guidance** with clear implementation status markers. Update all artifacts in coordinated batches with incremental validation. Create structured objects using domain-appropriate templates and serialize as JSON with semver-date versioning. The enhanced process produces water-tight service specifications enabling independent development with guaranteed integration success."

---

## System-of-Systems Graph Validation and Automated Issue Resolution

### Purpose and Workflow

The step involving `/tools/system_of_systems_graph.py` is primarily designed for the LLM agent to:

1. **Generate and review a comprehensive, machine-readable `system_of_systems_graph.json` file** representing the entire architecture as a directed graph (nodes = services/components, edges = interfaces/dependencies).
2. **Automated Architecture Validation**:
   - The LLM agent parses the JSON graph to identify architectural errors, issues, and gaps:
     - Missing or ambiguous interfaces
     - Unresolved dependencies
     - Circular dependencies
     - Incomplete communication paths
     - Security boundary violations
     - Performance bottlenecks
     - Orphaned nodes (unused services/components)
     - Inconsistent message formats or protocols
   - The agent uses graph algorithms (e.g., cycle detection, path analysis, dependency resolution) to systematically validate the architecture.
3. **Automated Issue Resolution**:
   - For each identified risk/issue/gap, the LLM agent:
     - Documents the problem in a machine-actionable format (e.g., `architecture_issues.json`)
     - Proposes and applies targeted fixes:
       - Adds missing interfaces or clarifies ambiguous ones
       - Resolves circular dependencies (e.g., by introducing message queues or refactoring service responsibilities)
       - Updates service specifications to close gaps
       - Harmonizes message formats and protocols
       - Adjusts security boundaries and access controls
       - Reassigns or removes orphaned nodes
     - Updates all affected artifacts (service_architecture.json, integration_matrix.json, etc.)
   - The process iterates until the graph is free of critical issues and all services are fully integrated.
4. **Human-Readable Visualization (Optional)**:
   - The visual graph output (e.g., PNG, SVG) is generated for human review **after** the architecture is validated and finalized.
   - This artifact is for documentation, presentation, and collaborative review, but is not required for automated validation or issue resolution.

### Key Principles
- **Machine-Readable First**: The JSON graph is the authoritative source for architecture validation and automated issue resolution.
- **Automated Correction**: The LLM agent is responsible for identifying and resolving all architectural issues before human review.
- **Iterative Improvement**: The process repeats until the architecture is robust, integrated, and free of critical gaps.
- **Human Visualization is Secondary**: Visual artifacts are generated only after the architecture is validated and are not used for automated correction.

---

## Process Completion and Build Preparation

When the step-by-step architecture process is complete, three critical final activities must be performed to prepare for the actual service/system implementation phase:

### 1. Artifact Cleanup and Organization

**Purpose**: Remove temporary files and organize final deliverables for the build phase.

**Cleanup Actions**:
```bash
# Execute cleanup and finalization script
python3 /tools/finalize_architecture.py /systems/<system_name>

# This script will:
# - Remove temporary files (working_memory.json, current_focus.md, step_progress_tracker.json)
# - Archive process logs (process_log.md) to /systems/<system_name>/archive/
# - Validate all final artifacts are present and complete
# - Generate cleanup report listing removed files
```

**Files to Remove** (temporary/process artifacts):
- `working_memory.json` - LLM context management
- `current_focus.md` - Step-by-step guidance
- `step_progress_tracker.json` - Progress tracking
- `artifact_generation_plan.json` - Generation roadmap
- `context_checkpoint.md` - Context snapshots
- Individual validation logs and intermediate files

**Files to Preserve** (final deliverables):
- All `service_architecture.json` files
- All Step 8 implementation artifacts (api_contracts.json, data_models.json, etc.)
- `system_of_systems_graph.json` - Validated architecture graph
- `index.json` - Master artifact registry
- `integration_matrix.json` - Service integration specifications
- Architecture Decision Records (ADRs)
- Final validation reports

### 2. Enhanced Index and Build Instructions

**Purpose**: Create comprehensive build guidance and artifact registry for development teams.

**Enhanced Index Structure** (`/systems/<system_name>/build_ready_index.json`):
```json
{
  "system_metadata": {
    "system_name": "system_name",
    "architecture_version": "1.0+2025-10-04",
    "completion_date": "2025-10-04T15:30:00Z",
    "total_services": 4,
    "technology_stack": {
      "language": "Python",
      "framework": "FastAPI",
      "deployment": "Docker + Traefik",
      "dependency_management": "Poetry"
    }
  },
  "build_instructions": {
    "recommended_build_order": [
      "core_services",
      "integration_services", 
      "api_gateway",
      "frontend_services"
    ],
    "dependency_groups": {
      "core_services": ["service_a", "service_b"],
      "integration_services": ["service_c"],
      "api_gateway": ["traefik_config"],
      "frontend_services": ["service_d"]
    },
    "parallel_build_candidates": ["service_a", "service_b"],
    "critical_path": ["service_a", "service_c", "service_d"]
  },
  "artifact_registry": {
    "service_specifications": {
      "service_a": {
        "service_architecture": "/systems/system_name/service_a/service_architecture.json",
        "api_contracts": "/systems/system_name/service_a/api_contracts.json",
        "data_models": "/systems/system_name/service_a/data_models.json",
        "integration_tests": "/systems/system_name/service_a/integration_tests.json",
        "infrastructure": "/systems/system_name/service_a/infrastructure.json",
        "implementation_guide": "/systems/system_name/service_a/implementation_guide.md",
        "testing_requirements": "/systems/system_name/service_a/testing_requirements.json"
      }
    },
    "system_wide_artifacts": {
      "architecture_graph": "/systems/system_name/system_of_systems_graph.json",
      "integration_matrix": "/systems/system_name/integration_matrix.json",
      "deployment_architecture": "/systems/system_name/deployment_architecture.json",
      "security_framework": "/systems/system_name/security_framework.json"
    },
    "build_support": {
      "docker_compose_template": "/systems/system_name/deployment/docker-compose.yml",
      "traefik_configuration": "/systems/system_name/deployment/traefik.yml",
      "environment_configs": "/systems/system_name/deployment/configs/",
      "ci_cd_pipelines": "/systems/system_name/cicd/"
    }
  },
  "validation_status": {
    "architecture_validated": true,
    "integration_verified": true,
    "security_reviewed": true,
    "performance_analyzed": true,
    "deployment_ready": true
  },
  "next_phase_guidance": {
    "implementation_teams": {
      "service_a_team": {
        "primary_artifacts": ["service_a/*"],
        "dependencies": ["service_b"],
        "estimated_effort": "4-6 weeks",
        "critical_interfaces": ["auth_service", "data_store"]
      }
    },
    "integration_strategy": {
      "contract_testing": "Use api_contracts.json for automated contract tests",
      "mock_services": "Use stubs/ directories for development mocking",
      "integration_order": "Follow dependency_groups build order"
    }
  }
}
```

**Build Phase Instructions** (`/systems/<system_name>/BUILD_INSTRUCTIONS.md`):
```markdown
# Build Phase Instructions

## Quick Start
1. Review `/systems/system_name/build_ready_index.json` for complete artifact registry
2. Follow recommended build order: core_services → integration_services → api_gateway → frontend_services
3. Use service-specific implementation guides in each service directory
4. Run integration tests after each service completion

## Development Team Assignments
- **Core Services Team**: service_a, service_b (can be built in parallel)
- **Integration Team**: service_c (depends on core services)
- **Infrastructure Team**: Traefik configuration, deployment automation
- **Frontend Team**: service_d (depends on all backend services)

## Artifact Usage Guide
- **service_architecture.json**: Complete functional and interface requirements
- **api_contracts.json**: OpenAPI specs for service implementation
- **data_models.json**: Database schemas and data validation rules
- **integration_tests.json**: Contract testing scenarios
- **infrastructure.json**: Deployment and scaling requirements
- **implementation_guide.md**: Technology-specific guidance and best practices

## Quality Gates
1. **Service Completion**: All individual service tests pass
2. **Interface Validation**: Contract tests pass between services
3. **Integration Verification**: End-to-end scenarios execute successfully
4. **Performance Validation**: Meets requirements in infrastructure.json
5. **Security Review**: Passes security compliance tests
```

### 3. Comprehensive Functional Test Strategy

**Purpose**: Define testing approach for individual services and integrated system validation.

**Test Strategy Document** (`/systems/<system_name>/FUNCTIONAL_TEST_STRATEGY.md`):
```markdown
# Functional Test Strategy

## Testing Hierarchy

### Level 1: Individual Service Testing
**Objective**: Validate each service meets its service_architecture.json specification

**Test Categories**:
- **Unit Tests**: Internal service logic and business rules
- **Contract Tests**: API compliance against api_contracts.json
- **Data Model Tests**: Database operations and data validation
- **Security Tests**: Authentication, authorization, input validation
- **Performance Tests**: Response times and throughput per infrastructure.json

**Automation**: 
- Use testing_requirements.json for coverage requirements
- Generate test stubs from api_contracts.json
- Automated execution in CI/CD pipeline

### Level 2: Interface Integration Testing
**Objective**: Validate service-to-service communication and data flow

**Test Scenarios**:
- **Contract Validation**: Verify API contracts between service pairs
- **Message Format Validation**: Ensure data consistency across interfaces
- **Error Handling**: Test failure scenarios and recovery mechanisms
- **Authentication Flow**: Validate security boundaries and token passing
- **Performance**: Test interface response times and throughput

**Automation**:
- Use integration_tests.json specifications
- Mock external dependencies using stubs/
- Automated regression testing for interface changes

### Level 3: End-to-End System Testing
**Objective**: Validate complete system functionality and user workflows

**Test Scenarios**:
- **User Journey Testing**: Complete workflows from system_of_systems_graph.json
- **Cross-Service Transactions**: Multi-service operations and consistency
- **System Load Testing**: Full system under expected traffic patterns
- **Disaster Recovery**: Failure scenarios and system resilience
- **Security Penetration**: Full system security validation

**Test Environment**:
- Full deployment using deployment_architecture.json
- Production-like data volumes and traffic patterns
- Monitoring and observability per observability.json

## Test Data Strategy
- **Service Level**: Use data_models.json for test data generation
- **Integration Level**: Realistic data flows between services
- **System Level**: Production-representative datasets

## Test Automation Framework
- **Individual Services**: Framework per implementation_guide.md
- **Integration**: Contract testing using api_contracts.json
- **End-to-End**: Selenium/Playwright for user workflows
- **Performance**: Load testing per infrastructure.json requirements

## Quality Gates and Success Criteria
1. **Individual Service**: 90%+ test coverage, all contract tests pass
2. **Integration**: All interface tests pass, performance within SLA
3. **System**: All user journeys complete, system meets performance requirements
4. **Production Readiness**: Security tests pass, monitoring operational

## Continuous Testing Strategy
- **Pre-commit**: Unit tests and contract validation
- **Integration Branch**: Full integration test suite
- **Release Candidate**: Complete end-to-end testing
- **Production**: Continuous monitoring and smoke tests
```

**Automated Test Generation** (`/systems/<system_name>/test_generation_plan.json`):
```json
{
  "test_generation_strategy": {
    "contract_tests": {
      "source": "api_contracts.json files",
      "framework": "OpenAPI contract testing",
      "automation": "Generate from specification",
      "coverage": "All endpoints and response codes"
    },
    "integration_tests": {
      "source": "integration_tests.json files", 
      "framework": "Service-to-service validation",
      "automation": "Mock external dependencies",
      "coverage": "All interface communication paths"
    },
    "performance_tests": {
      "source": "infrastructure.json requirements",
      "framework": "Load testing framework",
      "automation": "Automated threshold validation",
      "coverage": "All performance-critical interfaces"
    },
    "security_tests": {
      "source": "compliance.json requirements",
      "framework": "Security testing suite",
      "automation": "OWASP compliance validation",
      "coverage": "All authentication and authorization flows"
    }
  },
  "test_execution_order": [
    "unit_tests",
    "contract_tests", 
    "integration_tests",
    "performance_tests",
    "security_tests",
    "end_to_end_tests"
  ]
}
```

These three completion activities ensure that the architecture process delivers a clean, organized, and actionable set of artifacts ready for the development and implementation phase, with comprehensive testing strategy to validate both individual services and the integrated system.

---

# ...existing code...
