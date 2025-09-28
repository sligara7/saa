


# Step-by-Step: LLM-Driven Translation of System Descriptions to Service JSON Objects (System-Agnostic)



## Overview: System-Agnostic, LLM-Driven Decomposition and JSON Representation

This process is designed to be agnostic to the domain, language, or granularity of the system being analyzed. It can be applied to:
- Software codebases (from individual functions/packages to high-level services)
- Systems-of-systems (e.g., distributed architectures, warfighting systems, biological systems)
- Any complex system where components ("nodes") and their interfaces ("edges") can be described

The only requirement is that the system can be described in text (free-form, markdown, structured docs, etc.). The LLM agent is responsible for decomposing, structuring, and serializing the system into a set of JSON objects representing each component and its interfaces, ready for further analysis (e.g., with NetworkX or other tools).




### LLM-Driven, Format-Agnostic Process
This process leverages an LLM agent to:
- Accept any human-provided input, including:
   - Individual SRDs/ICDs for each component, service, or package (in any format)
   - A high-level system description, architectural goal, or system-of-systems overview (free-form text, markdown, etc.)
- Decompose the system into individual components/services (nodes) and their interfaces (edges) if not already done
- Draft or parse SRDs (system requirements) and ICDs (interface control) for each component/service
- **Process each component/service independently and in alphabetical order.**
- **Translate each SRD and ICD as-is, with no deconfliction or cross-component validation at this stage.**
- Use a domain-appropriate template (e.g., SAA `base_models.py` for software) to build structured objects (e.g., `BaseSRD`, `BaseICD`, `ServiceArchitecture`)
- Serialize each component/service as a JSON file (with versioning) in its folder, ready for analysis
- Support both bottom-up (component-by-component) and top-down (system goal) engineering workflows
- Optionally, allow for a high-level architecture object (e.g., `ARCHITECTURE.json`) to capture system-wide goals, constraints, or integration intent





### Detailed Steps (as performed in this project)

1. **Human Input**
   - The human provides either:
     - A high-level system description (text, markdown, etc.)
     - Or, a set of individual SRDs/ICDs for each component/service (in any format)

2. **LLM Agent Decomposition and Structuring**
   - If only a high-level description is provided, the LLM agent:
     - Decomposes the system into individual components/services (nodes) and their interfaces (edges)
     - Drafts SRD and ICD content for each component/service
   - If individual SRDs/ICDs are provided, the LLM agent parses and structures them
   - **No deconfliction or cross-component validation is performed at this stage.**

3. **Parse High-Level Architecture Constraints (Optional)**
   - Read and parse `ARCHITECTURE.json` (or equivalent) for global system constraints and requirements
   - Represent high-level architecture goals as a structured object/JSON if provided

4. **Translate to Structured Objects**
   - Use a domain-appropriate template (e.g., SAA's `base_models.py` for software)
   - For each component/service, create a structured object (e.g., `ServiceArchitecture` for software, or a domain-appropriate equivalent)

5. **Persist as JSON and Update Index**
   - Serialize each structured object to a JSON file (e.g., `service_architecture.json`) in the component/service's folder
   - Include a `version` field using semver-date versioning (e.g., `1.0+2025-09-28`)
   - **Automatically update a central JSON index file (e.g., `service_architecture_index.json`) with the absolute path to each `service_architecture.json` as it is created.**
   - The index must store the correct, directly usable absolute path for each file, so that downstream scripts can reliably access the artifacts without ambiguity or path errors.
   - If working with an existing codebase, retroactively scan and populate this index file to ensure all service JSONs are tracked with their absolute paths.

6. **Artifacts**
   - JSON files for each component/service's combined SRD/ICD object (with versioning)
   - In-memory structured objects for each component/service
   - A list of all components/services and their interfaces
   - **A central `service_architecture_index.json` file mapping each service to the absolute path of its JSON artifact (must be correct and directly usable by all scripts)**
   - Parsed system constraints from `ARCHITECTURE.json` or equivalent (if provided)

---


## Sample LLM Prompt Template (System-Agnostic)


> **Prompt:**
> "You are a systems architect assistant. Given the following system description or a set of SRDs/ICDs, process each component/service **independently and in alphabetical order**. For each, translate the provided SRD and ICD as-is (do not attempt to deconflict or cross-check with other components/services at this stage). Using a domain-appropriate template (e.g., SAA base_models.py for software), create a structured object for each (e.g., ServiceArchitecture, BaseSRD, BaseICD). Serialize each as a JSON file with a version field in semver-date format (e.g., 1.0+2025-09-28). Place each JSON in the appropriate folder. If any information is missing, make reasonable assumptions and document them in the output. This process is system-agnostic and can be applied to software, hardware, biological, or other complex systems."

---


---

## What We've Done So Far (Project-Specific)

1. **Collected all SRDs and ICDs** for each service in `/examples/xrpl_example/`.
2. **Used the LLM agent to parse and structure** each SRD and ICD independently, with no cross-service deconfliction.
3. **Created a `ServiceArchitecture` object** (using SAA's `base_models.py`) for each service, combining its SRD and ICD.
4. **Serialized each object as `service_architecture.json`** in the corresponding service folder, using semver-date versioning.
5. **Ensured the process is system-agnostic** and could be applied to any domain, not just Python or software.
6. **Ready for next steps:** network analysis, constraint checking, or system-wide integration using the generated JSON artifacts.

---

**Next Step:**
1. Use the LLM agent to perform the transformation from human input (system description or SRDs/ICDs) into structured JSON objects for each component/service, using a domain-appropriate template. **Process each independently and in alphabetical order, and do not attempt to deconflict ICDs/SRDs at this stage.**


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

3. **(Optional) Apply System-Level Constraints and Future-State Goals:**
    - If a system-level architecture file (e.g., `ARCHITECTURE.json` or equivalent) is present:
       - Parse and extract global constraints, rules, and requirements.
       - (In a future step) Iterate through each `service_architecture.json` and annotate or update them to reflect these constraints, flagging incompatibilities or integration issues.
    - **Note:**
       - The `service_architecture.json` files represent the current state, not necessarily the desired future integrated state.
       - Applying system-level constraints may reveal incompatibilities or objectives for a future integrated architecture.

4. **(Future Step) Deconfliction and Integration:**
    - After visualizing and analyzing the current state, proceed to:
       - Deconflict any issues in the current system-of-systems architecture.
       - Apply additional constraints, requirements, or integration goals from the system-level architecture file.
       - Update the graph and service JSONs to reflect the desired future state.
