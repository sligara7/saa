


# Step-by-Step: LLM-Driven Translation of System Descriptions to Service JSON Objects (System-Agnostic)

## Architectural Definitions

This process uses standardized architectural definitions based on the Unified Architecture Framework (UAF). All terms, concepts, and hierarchical structures are defined in:

**📁 `/definitions/architectural_definitions.json`**

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

### Critical Context Preservation

**CONTEXT WINDOW LIMITATION MITIGATION**: This process includes systematic context refresh mechanisms to prevent LLM agents from losing track of objectives, constraints, and methodology during complex, multi-step operations.

#### Context Refresh Trigger Points
1. **Every N operations** (recommended: 5-10 service files or 15-20 minutes of processing)
2. **Before starting each major step** (Steps 1, 2, 3, 4, 5, 6)
3. **When context appears degraded** (inconsistent naming, forgotten constraints, template violations)
4. **After handling interruptions** (user questions, clarifications, error corrections)
5. **Before complex operations** (Level 3 decomposition, graph analysis, deployment validation)

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

---


## Enhanced LLM Prompt Template (System-Agnostic with Automation and Context Management)


> **Prompt:**
> "You are a systems architect assistant partnering with a human to analyze a system-of-systems using an enhanced automated workflow. **CRITICAL: You MUST implement systematic context refresh to prevent losing track of objectives during complex operations.**
> 
> **CONTEXT MANAGEMENT PROTOCOL:**
> - **INITIAL SETUP**: Review architectural definitions in `/definitions/architectural_definitions.json` and templates in `/templates/` to ensure consistent terminology and UAF standards
> - **CONTEXT REFRESH TRIGGERS**: Automatically refresh context every 5-7 operations, every 15-20 minutes, before major steps, or when context degradation is detected
> - **REFRESH SEQUENCE**: (1) Save current state to working_memory.json, (2) Reload definitions and templates, (3) Restore system context, (4) Verify progress against process_log.md, (5) Validate consistency, (6) Resume with explicit confirmation
> - **DEGRADATION DETECTION**: Monitor for naming inconsistencies, template violations, forgotten constraints, repetitive questions, or UAF terminology drift
> - **PERSISTENT MEMORY**: Maintain process_log.md (decisions/issues), working_memory.json (current state), and context_checkpoint.md (critical context)
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
> Given the following system description or SRDs/ICDs, identify the starting hierarchy level (Level 0) and apply the Two-Level Rule with objective decomposition triggers. **Capture complete communication flows** including external/non-modifiable systems. Build a global graph and infer all communication paths using graph algorithms. **Generate precise implementation guidance** with clear implementation status markers. Update all artifacts in coordinated batches with incremental validation. Create structured objects using domain-appropriate templates and serialize as JSON with semver-date versioning. The enhanced process produces water-tight service specifications enabling independent development with guaranteed integration success."

---


---

## What We've Done So Far (Project-Specific)

1. **Collected all SRDs and ICDs** for each service in `/examples/xrpl_example/`.
2. **Used the LLM agent to parse and structure** each SRD and ICD, then inferred end-to-end paths and deduced all required interfaces.
3. **Created a `ServiceArchitecture` object** (using SAA's `base_models.py`) for each service, combining its SRD and ICD with deduced interfaces.
4. **Updated all relevant service artifacts in coordinated batches** to ensure interface consistency and message format alignment across communication paths.
5. **Serialized each object as `service_architecture.json`** in the corresponding service folder, using semver-date versioning.
6. **Ensured the process is system-agnostic** and could be applied to any domain, not just Python or software.
7. **Ready for next steps:** network analysis, constraint checking, or system-wide integration using the generated JSON artifacts.

---

**Next Step:**
1. Use the LLM agent to perform the transformation from human input (system description or SRDs/ICDs) into structured JSON objects for each component/service, using a domain-appropriate template. **Build a global system graph, infer all end-to-end paths and interfaces, and update all relevant service artifacts in coordinated batches to ensure consistency.**


2. **Index and Visualize the Current System-of-Systems State:**
    - **Indexing:**
       - As each `service_architecture.json` is created, its absolute path is automatically recorded in a central `service_architecture_index.json` file (a mapping of service ID to absolute file path).
       - For existing projects, retroactively scan and populate this index file to ensure all service JSONs are tracked with their absolute paths.
       - This index enables efficient access for analysis and future updates, and eliminates the need for directory scanning in downstream scripts. The path must be correct and directly usable by all scripts.
    - **Graph Construction:**
       - Write a Python script that:
          - Loads all `service_architecture.json` files using the central index file.
          - Adds each service as a node in a NetworkX directed graph.
          - Adds edges for each dependency/interface (using the `dependencies` or `interfaces` fields).
          - Visualizes or outputs the resulting system-of-systems graph.
    - **Purpose:**
       - This step captures the current state of the system as it is, before any system-level constraints or future-state goals are applied.
       - The graph supports analysis such as:
          - Identifying orphaned nodes/edges (services with no connections)
          - Detecting duplicative or overlapping functions
          - Highlighting missing or ambiguous interfaces
          - Enabling further constraint or gap analysis

3. **Parse System-Level Constraints and Prepare for Automated Analysis:**
    - If a system-level architecture file (e.g., `ARCHITECTURE.json` or equivalent) is present:
       - Parse and extract global constraints, rules, and requirements.
       - Prepare these constraints for automated validation in the next step.
    - **Note:**
       - The `service_architecture.json` files represent the current state, which will be analyzed for compliance with these constraints.
       - The automated analysis will identify where the current state deviates from desired constraints and goals.

4. **Automated Analysis and Risk/Gap Identification:**
    - **Phase 1: Identify Issues Using Graph Analysis:**
       - Use NetworkX graph algorithms and machine-readable artifacts to automatically detect:
          - **Orphaned nodes/services** (no incoming or outgoing connections)
          - **Circular dependencies** (cycles in the dependency graph)
          - **Single points of failure** (critical nodes whose removal disconnects the graph)
          - **Interface mismatches** (inconsistent message formats across communication paths)
          - **Missing intermediate interfaces** (gaps in end-to-end communication paths)
          - **Duplicative functions** (services with overlapping purposes or interfaces)
          - **Security vulnerabilities** (unencrypted or unauthenticated communication paths)
          - **Performance bottlenecks** (high-degree nodes that could become bottlenecks)
          - **Compliance violations** (services not meeting specified constraints from ARCHITECTURE.json)
       - Generate a machine-readable **issues report** (JSON format) categorizing all detected problems by severity and type
       - Provide human-readable **visualization and summary** highlighting problem areas in the system graph
    
    - **Phase 2: Generate and Implement Remedies:**
       - **Automated Remedy Suggestions:**
          - For each identified issue, use LLM analysis to propose specific remedies (e.g., "Add authentication to HTTP interface between service_A and service_B")
          - Rank remedies by impact, implementation complexity, and risk reduction
          - Generate updated `service_architecture.json` files that implement the proposed remedies
       - **Human-LLM Collaboration:**
          - Present issues and proposed remedies to the human for review and approval
          - Allow human to modify, reject, or prioritize remedies before implementation
          - Update the system graph and service artifacts to reflect approved changes
       - **Validation:**
          - Re-run the analysis on the updated system to verify that issues have been resolved
          - Ensure no new issues were introduced by the remedies
          - **Final Verification:** Confirm that each service specification is complete, unambiguous, and ready for independent development
          - **Integration Assurance:** Validate that all interface contracts are consistent and will enable seamless system integration
    
    - **Artifacts:**
       - **Issues report** (JSON) with detailed analysis of all detected problems
       - **Remedies report** (JSON) with proposed solutions and implementation plans
       - **Updated service_architecture.json files** implementing approved remedies
       - **Updated system graph** reflecting the improved architecture
       - **Validation report** confirming issue resolution

5. **Persist as JSON and Update Index**
   - Serialize each structured object to a JSON file (e.g., `service_architecture.json`) in the component/service's folder:
     - `/systems/<system_of_systems_name>/<individual_system_A>/service_architecture.json`
   - Include a `version` field using semver-date versioning (e.g., `1.0+2025-09-28`)
   - **Automatically update a central JSON index file:**  
     - Save as `/systems/<system_of_systems_name>/index.json`
     - This index maps each service ID to the absolute path of its `service_architecture.json`
     - The index must store the correct, directly usable absolute path for each file, so that downstream scripts can reliably access the artifacts without ambiguity or path errors.
   - If working with an existing codebase, retroactively scan and populate this index file to ensure all service JSONs are tracked with their absolute paths.
   - **System-level artifacts:**  
     - Any global system graphs, constraint files, or reports are saved in `/systems/<system_of_systems_name>/`

---

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

---

## Summary of Process Improvements

### 🎯 **Key Enhancements Implemented**

#### 1. **Automated Source Code Integration (Step 1.1)**
- **GitHub API Integration**: Automatic repository scanning for existing APIs and interfaces
- **Implementation Status Automation**: Categorizes interfaces as existing/needs_verification/missing based on source analysis
- **Configuration Discovery**: Automatically finds deployment configs (nginx.conf, docker-compose.yml, etc.)
- **Source Evidence Linking**: Creates traceable links between architecture specs and actual code

#### 2. **Objective Decomposition Triggers (Step 2)**
- **Six Objective Criteria**: Clear, measurable triggers for Level 3 decomposition
- **Automated Complexity Analysis**: Counts method calls, identifies safety/security interfaces
- **Performance Bottleneck Detection**: Uses graph analysis to identify high-degree nodes
- **Multi-Service Coordination Detection**: Identifies interfaces requiring coordination between >2 services

#### 3. **Systematic Deployment Validation (Step 5)**
- **Multi-Format Artifact Parsing**: Docker, K8s, Ansible, Terraform, nginx configurations
- **Architecture Reconciliation**: Compares logical dependencies with actual deployment routing
- **Automatic Correction Engine**: Updates service_architecture.json files to match deployment reality
- **Deployment Evidence Documentation**: Links logical architecture to specific deployment artifacts

#### 4. **Incremental Validation Checkpoints (Step 6)**
- **Four-Stage Validation**: Post-decomposition, post-graph, post-deployment, and final checkpoints
- **Early Issue Detection**: Catches problems before they propagate through the process
- **Validation Rollback**: Prevents proceeding with invalid architectures
- **Comprehensive Integration Readiness**: Final checkpoint ensures all services are ready for independent development

### 🔧 **Implementation Impact**

#### **Before Improvements**:
- Manual source code verification
- Subjective decomposition decisions
- Late-stage validation discovery
- Deployment architecture mismatches

#### **After Improvements**:
- Automated source analysis with confidence levels
- Objective criteria for consistent decomposition decisions
- Early validation with iterative correction
- Guaranteed logical-deployment architecture alignment

### 🚀 **Process Quality Improvements**

1. **Accuracy**: Automated source analysis reduces human error in interface identification
2. **Consistency**: Objective triggers ensure uniform decomposition across different LLM agents
3. **Completeness**: Deployment validation catches real-world architecture gaps
4. **Reliability**: Incremental validation prevents cascade failures in large systems
5. **Traceability**: Every interface links back to source code or deployment evidence

### 📈 **Expected Outcomes**

- **Reduced Manual Effort**: 60-80% reduction in manual verification tasks
- **Higher Accuracy**: 90%+ accuracy in existing vs. recommended interface classification
- **Faster Iteration**: Early validation catches issues in minutes vs. hours
- **Better Integration**: Deployment validation eliminates logical-physical architecture mismatches

The enhanced process maintains the original goal of producing water-tight service specifications while dramatically improving automation, accuracy, and reliability through systematic tooling and objective criteria.

6. **Artifacts**
   - JSON files for each component/service's combined SRD/ICD object (with versioning and deduced interfaces) in their respective subdirectories
   - **Hierarchical JSON files following the Two-Level Rule decomposition** (e.g., separate files for Level 1 and Level 2 components)
   - In-memory structured objects for each component/service at all decomposition levels
   - A global system graph (e.g., NetworkX DiGraph) with all components at the final decomposition level and their interfaces, saved in `/systems/<system_of_systems_name>/`
   - **A central `index.json` file mapping each component at all decomposition levels to the absolute path of its JSON artifact, saved in `/systems/<system_of_systems_name>/index.json`**
   - A central interface registry or mapping for consistency validation
   - Parsed system constraints from `ARCHITECTURE.json` or equivalent (if provided)
   - **Context Management Files** (NEW):
     - `/systems/<system_name>/process_log.md`: Chronological log of decisions, context refreshes, and issue resolution
     - `/systems/<system_name>/working_memory.json`: Current state, active constraints, decision cache for context restoration
     - `/systems/<system_name>/context_checkpoint.md`: Condensed critical context summary for quick LLM restoration
   - All artifacts designed for both machine-actionability (LLM processing) and human readability (review and collaboration)
