# Bluesky Scientific Data Acquisition System-of-Systems

## Overview

We are applying the LLM-driven, graph-based architecture process to design a comprehensive scientific data acquisition and control system based on the Bluesky ecosystem. The goal is to create water-tight service specifications that enable independent development while guaranteeing seamless integration.

## System Description

The Bluesky system-of-systems enables remote scientific instrument control and data acquisition through a distributed architecture of interconnected services. Users can queue experiments, monitor device status, and coordinate beamline operations through web interfaces while maintaining safety and preventing conflicts.

## Core Services

### Service 1: Queue Server Service (Experiment Execution)
**Purpose:** Manages experiment queue and execution pipeline
**Components:**
- `bluesky-queueserver` - Core queue management and plan execution
- `bluesky-queueserver-api` - Python API for queue interaction  
- `bluesky-httpserver` - HTTP/React web interface for queue management
- `nginx` - Reverse proxy providing HTTPS termination and load balancing for bluesky-httpserver
- `redis` - Persistent storage backend for queue state (plans, queue operations, and metadata)

**Communication Flow:**
```
Client → HTTP → bluesky-httpserver → ZMQ → bluesky-queueserver → bluesky/ophyd → EPICS → IOCs
```

**Status:** Already developed and deployed via Ansible

### Service 2: Device Monitoring Service (Real-time Status)
**Purpose:** Provides real-time monitoring of device status and PV traffic
**Components:**
- `ophyd-websocket` - WebSocket service for real-time device monitoring
- Client interfaces (Python/React/web)

**Communication Flow:**
```
IOCs → EPICS/CA → ophyd-websocket-service → HTTP/WebSocket → Client
```

**Status:** New addition to the ecosystem

### Service 3: Coordination Service (Beamline Control)
**Purpose:** Prevents conflicts between remote users and ensures safe beamline operation
**Requirements:**
- Lock beamline for exclusive scan execution
- Prevent simultaneous manual device control during automated scans
- Coordinate access between queue operations and manual interventions
- Replace traditional "physical presence" control with remote coordination

**Key Problem:** In traditional setups, beamline control is enforced by physical presence. With remote operation, we need a coordination mechanism to prevent conflicts (e.g., one user running a scan while another manually closes a shutter).

**Design Question:** Should this service be:
- Integrated into the Queue Server Service?
- Integrated into the Device Monitoring Service?
- A standalone coordination service?

## Cross-Service Requirements

### Shared Device Configuration
**Challenge:** Both Queue Server and Device Monitoring services need access to the same:
- Ophyd object definitions
- IOC configurations  
- Device registry information

**Solution Needed:** Determine how to share `bluesky-queueserver/blob/main/bluesky_queueserver/manager/profile_ops.py` functionality across services.

### Critical Constraint
**Avoid EPICS/CA Traffic Through RE Worker:** Prevent EPICS Channel Access traffic from routing through the RunEngine worker to avoid denial-of-service scenarios.

### Architectural Constraints
**Maintain Separation of Concerns:** Keep Bluesky packages focused on their core functions without adding unrelated functionality that violates their design purpose.

**Preserve Client/Server Boundaries:** Do not add server functionality to client packages or vice versa:
- `bluesky-queueserver-api` is a Python client library and should remain focused on client-side queue interaction
- `bluesky-httpserver` is primarily a proxy service providing HTTP interface to `bluesky-queueserver` and should not become a comprehensive server platform
- Each package should maintain its intended role in the ecosystem

## Design Principles

### Minimal Modification Strategy
**Goal:** Change existing Python packages as little as possible while enabling service-oriented architecture
**Requirements:**
- Preserve existing functionality and APIs
- Add new interfaces only where absolutely necessary
- Maintain backward compatibility
- Avoid architectural changes that require major refactoring

### Specific Interface Placement
**Critical Decision:** Determine exactly where to add new interfaces for:
- Coordination service integration points
- Shared configuration access points
- Cross-service communication endpoints
- Service discovery and registration mechanisms

**Constraint:** Interface additions must respect package boundaries and not violate separation of concerns

## Architecture Goals

Using our LLM-driven process, we will:

1. **Decompose** each service into complete SRDs (functional requirements) and ICDs (interface contracts)
2. **Build a global system graph** to identify all communication paths and dependencies
3. **Infer and validate all interfaces** between services, ensuring message format consistency
4. **Identify and resolve** architectural issues like the coordination service placement and shared configuration management
5. **Generate water-tight specifications** that enable independent development of each service with guaranteed integration success

## Expected Outcomes

- Complete `service_architecture.json` files for each service
- Validated interface contracts for all inter-service communication
- Resolution of coordination service architecture question
- Shared configuration management strategy
- Performance and safety validation ensuring EPICS traffic optimization
- **Minimal modification strategy** for existing Bluesky packages while enabling service-oriented architecture
- **Specific interface placement recommendations** - exactly where to add new interfaces without violating package boundaries
- Ready-to-develop specifications for distributed beamline control system

### Stretch Goal
- **Combined web client architecture** using `bluesky-webclient` as the foundation
- Integration strategy for React components supporting both:
  - Queue Server Service (experiment execution and management)
  - Device Monitoring Service (real-time status and PV monitoring)
- Unified user experience while maintaining service separation

