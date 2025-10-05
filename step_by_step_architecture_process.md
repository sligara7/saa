


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


---

## LLM Self-Validation Framework for Generated Artifacts

### Critical Trust and Quality Assurance Challenge

**The Challenge**: With expanded artifact generation in Step 8, there's an inherent "trust gap" where humans may lack domain expertise to validate complex technical specifications (API contracts, infrastructure requirements, security configurations, etc.). **How can we ensure LLM-generated artifacts are not just syntactically correct, but functionally viable for real-world integrated systems?**

### Multi-Layer Validation Strategy

#### 1. **Semantic Consistency Validation** (Automated)
```python
class SemanticValidator:
    """Validates that generated artifacts make logical sense together"""
    
    def validate_api_contract_coherence(self, service_spec, api_contracts):
        """Ensure API contracts align with service capabilities"""
        issues = []
        
        # Check that all service interfaces have corresponding API definitions
        declared_interfaces = service_spec.get("interfaces", [])
        api_endpoints = api_contracts.get("endpoints", [])
        
        for interface in declared_interfaces:
            if not self.has_matching_api_endpoint(interface, api_endpoints):
                issues.append(f"Interface '{interface['name']}' has no API implementation")
        
        # Validate data flow consistency
        for endpoint in api_endpoints:
            if not self.validate_data_flow(endpoint, service_spec):
                issues.append(f"Endpoint '{endpoint['path']}' data flow inconsistent with service model")
        
        return issues
    
    def validate_infrastructure_resource_alignment(self, service_spec, infrastructure_spec):
        """Ensure infrastructure specs match service requirements"""
        issues = []
        
        # Check CPU/Memory requirements against service complexity
        service_complexity = self.calculate_service_complexity(service_spec)
        resource_allocation = infrastructure_spec.get("resources", {})
        
        if self.resources_insufficient_for_complexity(service_complexity, resource_allocation):
            issues.append("Infrastructure resources may be insufficient for service complexity")
        
        # Validate network requirements
        service_interfaces = len(service_spec.get("interfaces", []))
        network_config = infrastructure_spec.get("networking", {})
        
        if not self.network_supports_interfaces(service_interfaces, network_config):
            issues.append("Network configuration doesn't support all service interfaces")
        
        return issues
    
    def validate_cross_service_integration(self, service_a_spec, service_b_spec):
        """Ensure two services can actually integrate as specified"""
        issues = []
        
        # Find interfaces between services
        a_to_b_interfaces = self.find_interfaces_between(service_a_spec, service_b_spec)
        
        for interface in a_to_b_interfaces:
            # Check protocol compatibility
            if not self.protocols_compatible(interface["source_protocol"], interface["target_protocol"]):
                issues.append(f"Protocol mismatch: {interface['name']}")
            
            # Check data format compatibility  
            if not self.data_formats_compatible(interface["source_format"], interface["target_format"]):
                issues.append(f"Data format incompatibility: {interface['name']}")
            
            # Check authentication compatibility
            if not self.auth_mechanisms_compatible(interface["source_auth"], interface["target_auth"]):
                issues.append(f"Authentication mismatch: {interface['name']}")
        
        return issues
```

#### 2. **Functional Completeness Verification** (Automated)
```python
class CompletenessValidator:
    """Ensures generated artifacts provide complete implementation guidance"""
    
    def validate_api_completeness(self, api_contracts):
        """Check that API specifications are implementation-ready"""
        completeness_issues = []
        
        for endpoint in api_contracts.get("endpoints", []):
            # Check request/response schema completeness
            if not self.has_complete_request_schema(endpoint):
                completeness_issues.append(f"Incomplete request schema: {endpoint['path']}")
            
            if not self.has_complete_response_schema(endpoint):
                completeness_issues.append(f"Incomplete response schema: {endpoint['path']}")
            
            # Check error handling completeness
            if not self.has_comprehensive_error_handling(endpoint):
                completeness_issues.append(f"Incomplete error handling: {endpoint['path']}")
            
            # Check authentication/authorization specification
            if not self.has_clear_auth_requirements(endpoint):
                completeness_issues.append(f"Unclear auth requirements: {endpoint['path']}")
        
        return completeness_issues
    
    def validate_data_model_completeness(self, data_models):
        """Ensure data models support all required operations"""
        issues = []
        
        for model in data_models.get("models", []):
            # Check for CRUD operation support
            if not self.supports_required_operations(model):
                issues.append(f"Model '{model['name']}' missing required operations")
            
            # Check for relationship consistency
            if not self.relationships_are_bidirectional(model, data_models):
                issues.append(f"Model '{model['name']}' has incomplete relationships")
            
            # Check for validation rules
            if not self.has_adequate_validation(model):
                issues.append(f"Model '{model['name']}' lacks validation rules")
        
        return issues
    
    def validate_infrastructure_completeness(self, infrastructure_spec):
        """Ensure infrastructure specs cover all deployment needs"""
        issues = []
        
        required_components = [
            "compute_resources", "storage_requirements", "network_configuration",
            "security_policies", "monitoring_setup", "backup_strategy"
        ]
        
        for component in required_components:
            if component not in infrastructure_spec:
                issues.append(f"Missing infrastructure component: {component}")
            elif not self.component_adequately_specified(infrastructure_spec[component]):
                issues.append(f"Inadequate specification for: {component}")
        
        return issues
```

#### 3. **Industry Standards Compliance** (RAG-Enhanced)
```python
class StandardsComplianceValidator:
    """Validates against industry best practices and standards"""
    
    def __init__(self, rag_system):
        self.rag_system = rag_system
        
    def validate_api_standards_compliance(self, api_contracts):
        """Check compliance with REST/OpenAPI best practices"""
        
        # Query RAG for current API standards
        current_standards = self.rag_system.query(
            "REST API design best practices OpenAPI specification standards 2024"
        )
        
        compliance_issues = []
        
        for endpoint in api_contracts.get("endpoints", []):
            # Check HTTP method usage
            if not self.follows_rest_conventions(endpoint, current_standards):
                compliance_issues.append(f"REST convention violation: {endpoint['path']}")
            
            # Check status code usage
            if not self.uses_appropriate_status_codes(endpoint, current_standards):
                compliance_issues.append(f"Inappropriate status codes: {endpoint['path']}")
            
            # Check security headers
            if not self.includes_security_headers(endpoint, current_standards):
                compliance_issues.append(f"Missing security headers: {endpoint['path']}")
        
        return compliance_issues
    
    def validate_security_standards(self, all_service_specs):
        """Validate against current security frameworks"""
        
        security_standards = self.rag_system.query(
            "cybersecurity best practices API security OWASP top 10 2024"
        )
        
        security_issues = []
        
        for service_spec in all_service_specs:
            # Check authentication mechanisms
            if not self.uses_modern_auth(service_spec, security_standards):
                security_issues.append(f"Outdated auth mechanism: {service_spec['name']}")
            
            # Check for encryption requirements
            if not self.adequate_encryption(service_spec, security_standards):
                security_issues.append(f"Insufficient encryption: {service_spec['name']}")
            
            # Check for input validation
            if not self.comprehensive_input_validation(service_spec, security_standards):
                security_issues.append(f"Inadequate input validation: {service_spec['name']}")
        
        return security_issues
```

#### 4. **System Integration Simulation** (Advanced)
```python
class IntegrationSimulator:
    """Simulates system behavior to detect integration issues"""
    
    def simulate_end_to_end_workflows(self, system_specs, test_scenarios):
        """Simulate complete workflows to find integration gaps"""
        
        simulation_results = []
        
        for scenario in test_scenarios:
            try:
                # Trace through the workflow
                execution_path = self.trace_workflow_execution(scenario, system_specs)
                
                # Check for bottlenecks
                bottlenecks = self.identify_bottlenecks(execution_path)
                
                # Check for failure points
                failure_points = self.identify_failure_points(execution_path)
                
                # Check for data inconsistencies
                data_issues = self.check_data_consistency(execution_path)
                
                simulation_results.append({
                    "scenario": scenario["name"],
                    "execution_path": execution_path,
                    "bottlenecks": bottlenecks,
                    "failure_points": failure_points,
                    "data_issues": data_issues,
                    "success": len(bottlenecks) == 0 and len(failure_points) == 0 and len(data_issues) == 0
                })
                
            except Exception as e:
                simulation_results.append({
                    "scenario": scenario["name"],
                    "error": str(e),
                    "success": False
                })
        
        return simulation_results
    
    def validate_performance_characteristics(self, system_specs):
        """Predict system performance based on specifications"""
        
        performance_analysis = {}
        
        for service_name, service_spec in system_specs.items():
            # Estimate response times
            estimated_latency = self.estimate_service_latency(service_spec)
            
            # Estimate throughput
            estimated_throughput = self.estimate_service_throughput(service_spec)
            
            # Identify potential scaling issues
            scaling_concerns = self.identify_scaling_concerns(service_spec)
            
            performance_analysis[service_name] = {
                "estimated_latency_ms": estimated_latency,
                "estimated_throughput_rps": estimated_throughput,
                "scaling_concerns": scaling_concerns
            }
        
        return performance_analysis
```

#### 5. **Deployment Feasibility Analysis** (Automated)
```python
class DeploymentValidator:
    """Validates that generated specs can actually be deployed"""
    
    def validate_resource_requirements(self, infrastructure_specs):
        """Check if resource requirements are realistic"""
        
        feasibility_issues = []
        
        total_cpu = sum(spec.get("cpu_cores", 0) for spec in infrastructure_specs.values())
        total_memory = sum(spec.get("memory_gb", 0) for spec in infrastructure_specs.values())
        total_storage = sum(spec.get("storage_gb", 0) for spec in infrastructure_specs.values())
        
        # Check against reasonable limits
        if total_cpu > 100:  # Example threshold
            feasibility_issues.append(f"Total CPU requirement ({total_cpu} cores) may be excessive")
        
        if total_memory > 500:  # Example threshold  
            feasibility_issues.append(f"Total memory requirement ({total_memory} GB) may be excessive")
        
        # Check for resource conflicts
        port_conflicts = self.check_port_conflicts(infrastructure_specs)
        if port_conflicts:
            feasibility_issues.extend(port_conflicts)
        
        return feasibility_issues
    
    def validate_dependency_availability(self, all_service_specs):
        """Check that all dependencies can be satisfied"""
        
        dependency_issues = []
        
        # Build dependency graph
        dependency_graph = self.build_dependency_graph(all_service_specs)
        
        # Check for circular dependencies
        cycles = self.find_cycles(dependency_graph)
        if cycles:
            dependency_issues.extend([f"Circular dependency: {' -> '.join(cycle)}" for cycle in cycles])
        
        # Check for missing dependencies
        missing_deps = self.find_missing_dependencies(dependency_graph, all_service_specs)
        if missing_deps:
            dependency_issues.extend([f"Missing dependency: {dep}" for dep in missing_deps])
        
        return dependency_issues
```

### Integrated Self-Validation Protocol

#### Mandatory Validation Sequence for Step 8 Artifacts
```python
class ArtifactValidationOrchestrator:
    """Orchestrates comprehensive validation of all generated artifacts"""
    
    def __init__(self, rag_system):
        self.semantic_validator = SemanticValidator()
        self.completeness_validator = CompletenessValidator()
        self.standards_validator = StandardsComplianceValidator(rag_system)
        self.integration_simulator = IntegrationSimulator()
        self.deployment_validator = DeploymentValidator()
    
    def validate_all_artifacts(self, system_path):
        """Run comprehensive validation on all generated artifacts"""
        
        print("🔍 STARTING COMPREHENSIVE ARTIFACT VALIDATION")
        
        # Load all artifacts
        artifacts = self.load_all_artifacts(system_path)
        
        validation_report = {
            "timestamp": datetime.now().isoformat(),
            "system_name": artifacts["system_name"],
            "validation_results": {},
            "overall_status": "UNKNOWN",
            "critical_issues": [],
            "warnings": [],
            "recommendations": []
        }
        
        # 1. Semantic Consistency Validation
        print("1️⃣ Validating semantic consistency...")
        semantic_issues = self.validate_semantic_consistency(artifacts)
        validation_report["validation_results"]["semantic_consistency"] = semantic_issues
        
        # 2. Functional Completeness
        print("2️⃣ Validating functional completeness...")
        completeness_issues = self.validate_completeness(artifacts)
        validation_report["validation_results"]["completeness"] = completeness_issues
        
        # 3. Standards Compliance
        print("3️⃣ Validating standards compliance...")
        standards_issues = self.validate_standards_compliance(artifacts)
        validation_report["validation_results"]["standards_compliance"] = standards_issues
        
        # 4. Integration Simulation
        print("4️⃣ Running integration simulation...")
        integration_results = self.simulate_integration(artifacts)
        validation_report["validation_results"]["integration_simulation"] = integration_results
        
        # 5. Deployment Feasibility
        print("5️⃣ Validating deployment feasibility...")
        deployment_issues = self.validate_deployment_feasibility(artifacts)
        validation_report["validation_results"]["deployment_feasibility"] = deployment_issues
        
        # Analyze overall status
        validation_report["overall_status"] = self.determine_overall_status(validation_report)
        validation_report["critical_issues"] = self.extract_critical_issues(validation_report)
        validation_report["recommendations"] = self.generate_improvement_recommendations(validation_report)
        
        # Save validation report
        self.save_validation_report(validation_report, system_path)
        
        return validation_report
    
    def determine_overall_status(self, validation_report):
        """Determine if artifacts are ready for implementation"""
        
        results = validation_report["validation_results"]
        
        # Count critical issues
        critical_count = 0
        warning_count = 0
        
        for category, issues in results.items():
            if isinstance(issues, list):
                critical_count += len([i for i in issues if i.get("severity") == "critical"])
                warning_count += len([i for i in issues if i.get("severity") == "warning"])
        
        if critical_count == 0:
            return "READY_FOR_IMPLEMENTATION"
        elif critical_count <= 3:
            return "NEEDS_MINOR_FIXES"
        else:
            return "NEEDS_MAJOR_REVISION"
```

### Confidence Scoring and Uncertainty Tracking

#### LLM Self-Assessment Framework
```python
class LLMSelfAssessment:
    """Framework for LLMs to assess their own artifact quality"""
    
    def assess_artifact_confidence(self, artifact_type, generated_content, source_context):
        """LLM assesses its own confidence in generated artifacts"""
        
        confidence_factors = {
            "source_code_evidence": self.has_source_code_backing(generated_content, source_context),
            "industry_standard_alignment": self.aligns_with_standards(generated_content),
            "internal_consistency": self.is_internally_consistent(generated_content),
            "completeness": self.is_complete(generated_content),
            "complexity_appropriateness": self.matches_problem_complexity(generated_content, source_context)
        }
        
        # Calculate weighted confidence score
        weights = {
            "source_code_evidence": 0.3,
            "industry_standard_alignment": 0.25,
            "internal_consistency": 0.2,
            "completeness": 0.15,
            "complexity_appropriateness": 0.1
        }
        
        confidence_score = sum(
            confidence_factors[factor] * weights[factor] 
            for factor in confidence_factors
        )
        
        # Generate uncertainty notes
        uncertainty_notes = []
        for factor, confident in confidence_factors.items():
            if not confident:
                uncertainty_notes.append(f"Low confidence in {factor}")
        
        return {
            "confidence_score": confidence_score,
            "confidence_level": self.categorize_confidence(confidence_score),
            "uncertainty_notes": uncertainty_notes,
            "recommended_validation": self.recommend_validation_approach(confidence_score, uncertainty_notes)
        }
    
    def categorize_confidence(self, score):
        """Categorize confidence score into levels"""
        if score >= 0.8:
            return "HIGH"
        elif score >= 0.6:
            return "MEDIUM"
        elif score >= 0.4:
            return "LOW"
        else:
            return "VERY_LOW"
    
    def recommend_validation_approach(self, confidence_score, uncertainty_notes):
        """Recommend specific validation approaches based on confidence"""
        
        recommendations = []
        
        if confidence_score < 0.6:
            recommendations.append("REQUIRES_HUMAN_REVIEW")
        
        if "source_code_evidence" in uncertainty_notes:
            recommendations.append("NEEDS_SOURCE_CODE_VERIFICATION")
        
        if "industry_standard_alignment" in uncertainty_notes:
            recommendations.append("REQUIRES_STANDARDS_COMPLIANCE_CHECK")
        
        if "internal_consistency" in uncertainty_notes:
            recommendations.append("NEEDS_CONSISTENCY_VALIDATION")
        
        return recommendations
```

### Integration with Step 8 Artifact Generation

#### Enhanced Step 8 with Built-in Validation
```markdown
## Enhanced Step 8: Generate Implementation-Ready Development Artifacts (With Self-Validation)

**MANDATORY VALIDATION PROTOCOL**: After generating each artifact type, the LLM agent MUST:

1. **Self-Assessment**: Evaluate confidence in generated artifacts using LLMSelfAssessment framework
2. **Automated Validation**: Run appropriate validators (semantic, completeness, standards)
3. **Integration Check**: Verify artifacts work together coherently
4. **Confidence Reporting**: Document confidence levels and uncertainty areas
5. **Validation Results**: Save validation report with recommendations for human review

### Step 8.1: API Contract Definitions (with Validation)
For each service, generate OpenAPI specifications, then IMMEDIATELY validate:

```bash
# Generate API contracts
python3 /tools/generate_api_contracts.py /systems/<system_name>/<service>

# MANDATORY: Self-validate generated contracts
python3 /tools/validate_api_contracts.py /systems/<system_name>/<service>/api_contracts.json

# Check semantic consistency with service architecture
python3 /tools/validate_semantic_consistency.py /systems/<system_name>/<service>

# Generate confidence report
python3 /tools/assess_artifact_confidence.py /systems/<system_name>/<service>/api_contracts.json
```

### Step 8.2: Data Model Specifications (with Validation)
Generate database schemas and data models, then validate:

```bash
# Generate data models
python3 /tools/generate_data_models.py /systems/<system_name>/<service>

# MANDATORY: Validate data model completeness
python3 /tools/validate_data_completeness.py /systems/<system_name>/<service>/data_models.json

# Check for relationship consistency
python3 /tools/validate_data_relationships.py /systems/<system_name>

# Assess LLM confidence
python3 /tools/assess_artifact_confidence.py /systems/<system_name>/<service>/data_models.json
```

### System-Wide Integration Validation
After completing all services for each artifact type:

```bash
# Run comprehensive system validation
python3 /tools/validate_system_integration.py /systems/<system_name>

# Generate deployment feasibility report
python3 /tools/validate_deployment_feasibility.py /systems/<system_name>

# Create comprehensive validation report
python3 /tools/generate_validation_report.py /systems/<system_name>
```

### Validation Report Format
```json
{
  "validation_report": {
    "system_name": "example_system",
    "validation_timestamp": "2025-10-04T15:30:00Z",
    "overall_status": "READY_FOR_IMPLEMENTATION",
    "confidence_summary": {
      "high_confidence_artifacts": ["api_contracts", "data_models"],
      "medium_confidence_artifacts": ["infrastructure"],
      "low_confidence_artifacts": ["security_configurations"],
      "requires_human_review": ["complex_integration_scenarios"]
    },
    "critical_issues": [
      {
        "issue": "Circular dependency between service_a and service_b",
        "severity": "critical",
        "recommendation": "Introduce message queue for async communication"
      }
    ],
    "integration_simulation_results": {
      "successful_scenarios": 8,
      "failed_scenarios": 2,
      "performance_concerns": ["service_c response time > 500ms"]
    },
    "deployment_feasibility": {
      "resource_requirements": "within reasonable limits",
      "dependency_satisfaction": "all dependencies resolvable",
      "scaling_projections": "linear scaling expected up to 1000 users"
    }
  }
}
```
```

### Trust Through Transparency and Verification

This self-validation framework addresses the "trust gap" by:

1. **🔍 Multi-Layer Verification**: Semantic, functional, standards, integration, and deployment validation
2. **📊 Confidence Scoring**: LLM explicitly assesses its own confidence and identifies uncertainty areas  
3. **🤖 Automated Cross-Checking**: Generated artifacts validate each other for consistency
4. **📈 Performance Simulation**: Predicts system behavior before implementation
5. **📋 Standards Compliance**: Validates against current industry best practices via RAG
6. **🎯 Targeted Human Review**: Identifies specific areas that need human expertise
7. **📝 Transparent Reporting**: Comprehensive validation reports with actionable recommendations

**Result**: Instead of blind trust, you get validated artifacts with explicit confidence levels, identified uncertainties, and clear guidance on what requires human verification.

## Enhanced Automation Tools and Implementation Guidance

### 1. Source Code Integration Automation

#### Automated GitHub Repository Analysis
```python
# Example implementation for GitHub API integration
import requests
import json
from pathlib import Path

class GitHubAnalyzer:
    def __init__(self, api_token):
        self.api_token = api_token
        self.headers = {"Authorization": f"token {api_token}"}
    
    def analyze_repository(self, repo_url):
        """Analyze GitHub repository for existing interfaces and APIs"""
        repo_info = self.extract_repo_info(repo_url)
        
        analysis = {
            "existing_apis": self.scan_for_apis(repo_info),
            "configuration_files": self.find_config_files(repo_info),
            "dependencies": self.extract_dependencies(repo_info),
            "interface_implementations": self.find_interface_patterns(repo_info)
        }
        
        return analysis
    
    def generate_implementation_status(self, interface_spec, repo_analysis):
        """Automatically determine implementation status"""
        if self.interface_exists_in_code(interface_spec, repo_analysis):
            return "existing"
        elif self.interface_mentioned_in_docs(interface_spec, repo_analysis):
            return "needs_verification" 
        else:
            return "missing"
```

#### Deployment Artifact Scanner
```python
# Example implementation for deployment validation
class DeploymentValidator:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
    
    def scan_deployment_artifacts(self):
        """Scan for all deployment configuration files"""
        artifacts = {
            "nginx_configs": list(self.project_path.rglob("nginx.conf")),
            "docker_compose": list(self.project_path.rglob("docker-compose*.yml")),
            "kubernetes_manifests": list(self.project_path.rglob("*.k8s.yaml")),
            "ansible_playbooks": list(self.project_path.rglob("*.ansible.yml")),
            "terraform_configs": list(self.project_path.rglob("*.tf"))
        }
        return artifacts
    
    def validate_routing_consistency(self, logical_architecture, deployment_artifacts):
        """Compare logical vs deployment architecture"""
        warnings = []
        
        # Parse nginx upstream definitions
        nginx_upstreams = self.parse_nginx_upstreams(deployment_artifacts["nginx_configs"])
        
        # Compare with logical dependencies
        for service, dependencies in logical_architecture.items():
            for dep in dependencies:
                if not self.routing_exists(service, dep, nginx_upstreams):
                    warnings.append(f"Missing routing: {service} -> {dep}")
        
        return warnings
```

### 2. Objective Decomposition Triggers Implementation

#### Automated Complexity Analysis
```python
class ComplexityAnalyzer:
    def __init__(self):
        self.decomposition_triggers = {
            "recommended_interface": self.check_recommended_interface,
            "complexity_threshold": self.check_complexity_threshold,
            "safety_critical": self.check_safety_critical,
            "multi_service": self.check_multi_service_coordination,
            "external_bridge": self.check_external_bridge,
            "bottleneck": self.check_performance_bottleneck
        }
    
    def should_decompose_to_level3(self, interface_spec, system_graph):
        """Determine if Level 3 decomposition is needed"""
        for trigger_name, trigger_func in self.decomposition_triggers.items():
            if trigger_func(interface_spec, system_graph):
                return True, trigger_name
        return False, None
    
    def check_complexity_threshold(self, interface_spec, system_graph):
        """Check if interface requires >3 method calls"""
        method_count = self.count_required_methods(interface_spec)
        return method_count > 3
    
    def check_safety_critical(self, interface_spec, system_graph):
        """Check if interface involves coordination or security"""
        critical_keywords = ["coordination", "lock", "auth", "security", "safety"]
        description = interface_spec.get("description", "").lower()
        return any(keyword in description for keyword in critical_keywords)
```

### 3. Incremental Validation System

#### Validation Checkpoint Manager
```python
class ValidationCheckpointManager:
    def __init__(self, project_path):
        self.project_path = project_path
        self.checkpoints = {
            "post_decomposition": self.validate_template_conformance,
            "post_graph": self.validate_graph_consistency, 
            "post_deployment": self.validate_deployment_alignment,
            "final": self.validate_integration_readiness
        }
    
    def run_checkpoint(self, checkpoint_name, artifacts):
        """Run specific validation checkpoint"""
        if checkpoint_name not in self.checkpoints:
            raise ValueError(f"Unknown checkpoint: {checkpoint_name}")
        
        validator = self.checkpoints[checkpoint_name]
        result = validator(artifacts)
        
        if not result.is_valid:
            raise ValidationError(f"Checkpoint {checkpoint_name} failed: {result.errors}")
        
        return result
    
    def validate_template_conformance(self, artifacts):
        """Validate all files conform to templates"""
        # Run validate_templates.py equivalent
        return self.run_template_validation()
    
    def validate_graph_consistency(self, artifacts):
        """Validate system graph for cycles and completeness"""
        graph = self.build_system_graph(artifacts)
        cycles = self.detect_cycles(graph)
        if cycles:
            return ValidationResult(False, f"Circular dependencies: {cycles}")
        return ValidationResult(True, "Graph is consistent")
```

### 4. Enhanced Interface Implementation Analysis

#### Automated Interface Generator
```python
class InterfaceImplementationGenerator:
    def __init__(self, source_analyzer, deployment_validator):
        self.source_analyzer = source_analyzer
        self.deployment_validator = deployment_validator
    
    def generate_precise_interface_spec(self, interface_description, source_repos):
        """Generate exact implementation specifications"""
        
        # Analyze source code for existing patterns
        existing_patterns = self.source_analyzer.find_similar_interfaces(
            interface_description, source_repos
        )
        
        # Generate implementation guidance
        spec = {
            "method_signatures": self.generate_method_signatures(existing_patterns),
            "data_structures": self.infer_data_structures(existing_patterns),
            "error_handling": self.suggest_error_patterns(existing_patterns),
            "integration_tests": self.generate_test_requirements(interface_description),
            "implementation_status": self.determine_status(existing_patterns),
            "source_evidence": self.link_to_source_examples(existing_patterns)
        }
        
        return spec
    
    def generate_method_signatures(self, patterns):
        """Generate specific method signatures based on existing code"""
        signatures = []
        for pattern in patterns:
            if pattern["confidence"] > 0.8:
                signatures.append({
                    "signature": pattern["method_signature"],
                    "source_file": pattern["file_path"],
                    "status": "existing"
                })
            else:
                signatures.append({
                    "signature": self.synthesize_signature(pattern),
                    "rationale": pattern["reasoning"],
                    "status": "recommended"
                })
        return signatures
```

### 5. Integration with Existing Validation Tools

#### Enhanced validate_templates.py Integration
```python
# Enhanced version of validate_templates.py with checkpoint support
def validate_with_checkpoints(system_path, checkpoint_stage=None):
    """Run validation appropriate for specific checkpoint"""
    
    if checkpoint_stage == "post_decomposition":
        # Validate basic template conformance
        return validate_basic_templates(system_path)
    
    elif checkpoint_stage == "post_graph":
        # Validate templates + graph consistency
        basic_result = validate_basic_templates(system_path) 
        graph_result = validate_graph_structure(system_path)
        return combine_results(basic_result, graph_result)
    
    elif checkpoint_stage == "post_deployment":
        # Validate templates + graph + deployment alignment
        return validate_full_architecture(system_path)
    
    elif checkpoint_stage == "final":
        # Comprehensive validation for integration readiness
        return validate_integration_readiness(system_path)
    
    else:
        # Default: run all validations
        return validate_comprehensive(system_path)
```

### 6. LLM Context Management and Memory Tools

#### Context Manager for Long Operations
```python
import json
import time
from datetime import datetime
from pathlib import Path

class LLMContextManager:
    def __init__(self, system_path):
        self.system_path = Path(system_path)
        self.process_log_path = self.system_path / "process_log.md"
        self.working_memory_path = self.system_path / "working_memory.json"
        self.context_checkpoint_path = self.system_path / "context_checkpoint.md"
        self.operation_count = 0
        self.last_refresh = time.time()
        
    def should_refresh_context(self):
        """Determine if context refresh is needed"""
        return (
            self.operation_count >= 7 or  # Every 7 operations
            (time.time() - self.last_refresh) > 1200 or  # Every 20 minutes
            self.detect_context_degradation()
        )
    
    def detect_context_degradation(self):
        """Detect signs of context loss"""
        degradation_indicators = [
            "template_violations_detected",
            "naming_inconsistencies_found", 
            "forgotten_constraints_detected",
            "repetitive_questions_asked"
        ]
        # Implementation would check for these indicators
        return False
    
    def save_current_state(self, current_operation, progress_data):
        """Save current state to working memory"""
        state = {
            "timestamp": datetime.now().isoformat(),
            "current_operation": current_operation,
            "operation_count": self.operation_count,
            "progress_data": progress_data,
            "system_context": self.get_system_context()
        }
        
        with open(self.working_memory_path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def create_context_checkpoint(self):
        """Create condensed context checkpoint for quick restoration"""
        checkpoint_content = f"""# Context Checkpoint - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## System Overview
- **System Name**: {self.get_system_name()}
- **Current Step**: {self.get_current_step()}
- **Operations Completed**: {self.operation_count}

## Critical Constraints
{self.get_critical_constraints()}

## Current Objectives
{self.get_current_objectives()}

## Key Decisions Made
{self.get_key_decisions()}

## Template Requirements
- Use exact format from `/templates/service_architecture_template.json`
- Follow UAF hierarchical structure (tier_0/tier_1/tier_2)
- Mark implementation_status as existing/recommended/hypothetical
- Include source_verification for all interfaces

## Refresh Protocol Completed ✓
- Architectural definitions reloaded
- Template requirements confirmed
- System context verified
- Progress validated against process log
"""
        
        with open(self.context_checkpoint_path, 'w') as f:
            f.write(checkpoint_content)
    
    def log_decision(self, decision_type, description, rationale):
        """Log important decisions to process log"""
        log_entry = f"""
## {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {decision_type}

**Description**: {description}

**Rationale**: {rationale}

**Operation Count**: {self.operation_count}

---
"""
        
        with open(self.process_log_path, 'a') as f:
            f.write(log_entry)
    
    def execute_context_refresh(self):
        """Execute full context refresh protocol"""
        print("🔄 EXECUTING CONTEXT REFRESH PROTOCOL")
        
        # 1. Save current state
        self.save_current_state("context_refresh", {"refresh_reason": "scheduled"})
        
        # 2. Create context checkpoint
        self.create_context_checkpoint()
        
        # 3. Log refresh event
        self.log_decision("CONTEXT_REFRESH", "Scheduled context refresh executed", 
                         f"Operation count: {self.operation_count}, Time since last: {time.time() - self.last_refresh:.1f}s")
        
        # 4. Reset counters
        self.operation_count = 0
        self.last_refresh = time.time()
        
        print("✅ CONTEXT REFRESH COMPLETED - Ready to resume operations")
        
        return {
            "system_name": self.get_system_name(),
            "current_step": self.get_current_step(),
            "critical_constraints": self.get_critical_constraints(),
            "template_requirements": self.get_template_requirements()
        }
    
    def increment_operation(self, operation_description):
        """Track operation and check for refresh need"""
        self.operation_count += 1
        
        if self.should_refresh_context():
            print(f"⚠️  CONTEXT REFRESH TRIGGERED after operation: {operation_description}")
            return self.execute_context_refresh()
        
        return None

# Usage in step-by-step process
def enhanced_step_2_with_context_management(system_description, system_path):
    """Enhanced Step 2 with automatic context management"""
    
    context_manager = LLMContextManager(system_path)
    
    # Initial context setup
    context_manager.log_decision("STEP_START", "Beginning Step 2: Decomposition", 
                                "Starting systematic decomposition with context management")
    
    services_to_process = identify_services(system_description)
    
    for i, service in enumerate(services_to_process):
        # Check for context refresh need before each service
        refresh_data = context_manager.increment_operation(f"Processing service: {service['name']}")
        
        if refresh_data:
            # Context was refreshed - confirm we're still on track
            print(f"📋 CONTEXT RESTORED - Continuing with service {i+1}/{len(services_to_process)}: {service['name']}")
            print(f"🎯 Current objective: {refresh_data['current_step']}")
        
        # Process the service
        service_architecture = create_service_architecture(service, refresh_data)
        
        # Log the completion
        context_manager.log_decision("SERVICE_COMPLETED", f"Completed {service['name']}", 
                                    f"Service {i+1}/{len(services_to_process)} processed successfully")
    
    # Final context checkpoint
    context_manager.create_context_checkpoint()
    context_manager.log_decision("STEP_COMPLETED", "Step 2 completed successfully", 
                                f"All {len(services_to_process)} services processed with {context_manager.operation_count} total operations")
```

#### Context Restoration Utility
```python
def restore_llm_context(system_path):
    """Utility to restore LLM context from checkpoint files"""
    
    system_path = Path(system_path)
    context_checkpoint = system_path / "context_checkpoint.md"
    working_memory = system_path / "working_memory.json"
    
    if not context_checkpoint.exists():
        raise FileNotFoundError("No context checkpoint found - cannot restore context")
    
    # Read checkpoint
    with open(context_checkpoint, 'r') as f:
        checkpoint_content = f.read()
    
    # Read working memory if available
    working_state = {}
    if working_memory.exists():
        with open(working_memory, 'r') as f:
            working_state = json.load(f)
    
    restoration_prompt = f"""
🔄 CONTEXT RESTORATION PROTOCOL

The following critical context must be restored for continuing the step-by-step architecture process:

{checkpoint_content}

**Working Memory State**: {json.dumps(working_state, indent=2)}

**MANDATORY ACTIONS BEFORE PROCEEDING:**
1. ✅ Confirm system name and current objectives
2. ✅ Reload architectural definitions from `/definitions/architectural_definitions.json`
3. ✅ Refresh template requirements from `/templates/`
4. ✅ Verify current step and progress
5. ✅ Resume operations with full context awareness

**RESPONSE REQUIRED**: Please confirm context restoration by stating:
- Current system name
- Current step being executed
- Next specific action to be taken
- Any critical constraints that must be maintained
"""
    
    return restoration_prompt
```

### 6. Implementation Roadmap

#### Phase 1: Core Automation (Immediate)
1. **Template Validation Enhancement**: Add checkpoint-specific validation modes
2. **Graph Analysis Automation**: Enhanced system graph building with cycle detection
3. **Basic Source Code Scanning**: Simple GitHub repository analysis for API discovery

#### Phase 2: Advanced Integration (Short-term)
1. **Deployment Artifact Parsing**: Automated nginx, Docker, K8s configuration analysis
2. **Objective Decomposition Triggers**: Automated complexity analysis and Level 3 triggers
3. **Incremental Validation System**: Checkpoint manager with rollback capabilities

#### Phase 3: Full Automation (Medium-term)
1. **AI-Powered Interface Generation**: ML-based interface implementation suggestion
2. **Continuous Architecture Validation**: CI/CD integration for architecture drift detection
3. **Cross-Repository Analysis**: Multi-repo system architecture validation

This enhanced automation framework transforms the step-by-step process from manual to automated while maintaining the rigor and completeness that ensures water-tight service specifications.
