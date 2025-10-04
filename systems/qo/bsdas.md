# Bluesky Scientific Data Acquisition System-of-Systems

## Overview

We are applying the LLM-driven, graph-based architecture process to design a comprehensive scientific data acquisition and control system based on the Bluesky ecosystem. The goal is to create water-tight service specifications that enable independent development while guaranteeing seamless integration.

## System Description

The Bluesky system-of-systems enables remote scientific instrument control and data acquisition through a distributed architecture of interconnected services. Users can queue experiments, monitor device status, and coordinate beamline operations through web interfaces while maintaining safety and preventing conflicts.

## Core Services


### Service 1: Queue Server Service (Experiment Execution)
**Purpose:**  
Manages the experiment queue, execution pipeline, and provides secure, remote access for experiment control.

**Deployed Components:**
- `bluesky-queueserver`: Core queue management and plan execution engine.
- `bluesky-httpserver`: HTTP/React web interface and API gateway for queue management.
- `nginx`: Reverse proxy providing HTTPS termination, API routing, and load balancing for `bluesky-httpserver`.
- `redis`: Persistent storage backend for queue state, plans, and metadata.
- Systemd-managed services for all major components.
- Secure API key authentication and SSL/TLS for all external interfaces.

**Directory and Environment Setup:**
- Automated creation of service directories (`environment`, `profile_collection`).
- Git-based deployment of experiment profiles and plans.
- Templated configuration and service files for reproducibility and maintainability.
- Log and config file management for traceability.

**Interfaces:**
- **External:**  
  - HTTPS API (via nginx and `bluesky-httpserver`) for queue management, status, and control.
  - Python client library (`bluesky-queueserver-api`) for programmatic access.
- **Internal:**  
  - ZMQ between `bluesky-httpserver` and `bluesky-queueserver`.
  - Redis for persistent state and inter-process communication.
  - Systemd for service lifecycle management.

**Security:**
- API key authentication for all remote access.
- SSL/TLS encryption for all HTTP(S) endpoints.
- Principle of least privilege for service accounts and file permissions.

**Deployment/Management:**
- Fully automated via Ansible playbooks and roles.
- Supports both installation and clean removal.
- Configurable via Ansible variables for site-specific customization.

**Usage Examples:**
- Python API and HTTP request examples provided for queue management and status monitoring.

**Communication Flow:**
```
Unified Web Client ↔ nginx reverse proxy ↔ [bluesky-httpserver (Queue Server Service) | ophyd-websocket (Device Monitoring Service) | Coordination Service]
  - nginx routes HTTP(S) requests to bluesky-httpserver for queue management
  - nginx routes WebSocket connections to ophyd-websocket for device monitoring/control
  - nginx routes coordination requests to Coordination Service for safety management
bluesky-queueserver (via bluesky-httpserver) ↔ redis (queue state)
ophyd-websocket ↔ EPICS/CA ↔ IOCs (with Queue Server coordination)
bluesky-queueserver ↔ EPICS/CA ↔ IOCs (with coordination safety checks)
Coordination Service ↔ [Queue Server Service, Device Monitoring Service]
  - Coordination Service enforces locking: when one service is actively controlling an IOC, the other is blocked from issuing commands to that IOC
  - Enhanced safety mechanisms prevent conflicts during plan execution
Device Registry ↔ [Queue Server Service, Device Monitoring Service]
  - Shared device configuration and metadata across services
```

**Status:**  
Already developed and deployed via Ansible; supports reproducible, secure, and maintainable operation.

### Service 2: Device Monitoring Service (Real-time Status)

**Purpose:**  
Provides real-time monitoring and control of EPICS/ophyd device status and process variables (PVs) to web and Python clients through enhanced websocket infrastructure with comprehensive safety mechanisms.

**Deployed Components:**
- `ophyd-websocket`: FastAPI-based WebSocket service for live device monitoring and control with enhanced capabilities
- React client hooks (`useOphydSocket.ts`) and supporting types for seamless integration into web UIs
- Python client support for direct WebSocket interaction
- Device registry integration with centralized configuration management
- Queue Server coordination service for conflict prevention

**Key Features:**
- **Enhanced Device Registry Integration**: Centralized device registry populated from startup files enabling:
  - Dynamic device discovery through GET endpoints
  - Subscription to devices by intuitive names (not just PV names)
  - Rich metadata about device capabilities and signal hierarchies
- **Unified WebSocket Interface**: Single websocket endpoint handling both Process Variables (PVs) and complex Ophyd devices
- **Advanced Safety Mechanisms**: Critical coordination with Queue Server to prevent conflicts:
  - All write operations check Queue Server status before execution
  - Commands rejected if RunEngine is active in Queue Server
  - Real-time coordination through Queue Server REST API
  - Protection for both REST API and WebSocket operations
- **Enhanced Subscription Model**: 
  - Subscribe to devices using intuitive names: `"IOC:m1"`, `"myDevice"`
  - Support for individual signals within complex Ophyd devices
  - Proper TypeScript typing for device objects and nested signals
  - Automatic metadata handling and signal hierarchy management
- **Multi-Protocol Support**: Receives live updates on value changes, device connection/disconnection events
- **Comprehensive Command Support**: Both monitoring and control operations with safety validation
- **Rich Message Format**: Structured JSON messaging with full device context and metadata

**Technical Implementation:**
- **Tested and Validated**: WebSocket service has been thoroughly tested with multiple concurrent connections
- **Multiple WebSocket Endpoints**: 
  - Primary device control websocket with enhanced safety
  - Queue Server console output streaming
  - Area detector array streaming for cameras
  - Real-time device state monitoring across all connected systems
- **Modern Frontend Integration**: Designed for seamless React component integration with structured data consumption

**Communication Flow:**
```
Unified Web Client ↔ Enhanced ophyd-websocket (FastAPI WebSocket) ↔ EPICS/CA ↔ IOCs
                                    ↕ (Safety Coordination)
                              Queue Server REST API
                                    ↕ (Device Registry)
                              Centralized Device Registry
                                    ↕ (Coordination)
                              Coordination Service
```

**Deployment/Management:**
- Can be started with Python or Uvicorn with enhanced configuration options
- Requirements: `ophyd`, `pyepics`, `fastapi`, `uvicorn`, `numpy`, plus coordination dependencies
- Designed for seamless deployment alongside Queue Server and coordination services
- Centralized configuration management through device registry

**Security:**
- Integrated with Queue Server authentication mechanisms
- Safety-first approach with comprehensive conflict prevention
- Configurable access controls for device operations

**Current Status & Integration:**
- **Active Development**: Enhanced coordination with Queue Server implemented and tested
- **Device Registry**: Centralized device management operational
- **Safety Mechanisms**: Queue Server coordination active and validated
- **Ready for Production**: Enhanced websocket infrastructure supporting modern beamline operations

### Service 3: Coordination Service (Beamline Control)
**Purpose:** Prevents conflicts between remote users and ensures safe beamline operation
**Requirements:**
- Lock beamline for exclusive scan/bluesky plan execution
- Prevent simultaneous manual device control during automated scans
- Coordinate access between queue operations and manual interventions
- Replace traditional "physical presence" control with remote coordination

**Communication Flow:**
```
Unified Web Client ↔ Coordination Service ↔ [Queue Server Service, Device Monitoring Service]
                                          ↔ Device Registry
                                          ↔ Authentication Service
```
*Enhanced coordination prevents ophyd-websocket from executing IOC commands while Queue Server is running plans, with comprehensive safety mechanisms and real-time status monitoring*

**Key Problem:** In traditional setups, beamline control is enforced by physical presence. With remote operation, we need a coordination mechanism to prevent conflicts (e.g., one user running a scan while another manually closes a shutter).

**Design Decision:** The coordination service will be its own independent service, not integrated into the Queue Server Service or Device Monitoring Service, to maintain separation of concerns and avoid coupling beamline control logic with experiment execution or device monitoring.

**Design Question:** Should this service be:
- Integrated into the Queue Server Service?
- Integrated into the Device Monitoring Service?
- ✅ A standalone coordination service? (SELECTED)

### Service 4: Unified Web Client (User Interface)

**Purpose:**  
Provides a comprehensive React-based web interface that combines beamline device control capabilities with experiment queue management functionality, creating a unified user experience for scientists and beamline operators.

**Core Architecture:**
The Unified Web Client integrates the best features of the [Finch UI library](https://github.com/bluesky/finch) for device interaction with [queue-monitor](https://github.com/bluesky/bluesky-widgets/tree/master/bluesky_widgets/apps/queue_monitor) capabilities for experiment queue management, delivered as a modern React application.

**Key Components:**
- **Finch Integration**: 
  - Device control widgets for motors, detectors, and beamline instruments
  - MEDM screen replication using modern React components
  - Real-time device status monitoring and control interfaces
  - Area detector integration for imaging systems
  - Customizable layouts for different beamline configurations

- **Queue Monitor Integration**:
  - Visual queue management interface for experiment planning
  - Real-time queue status monitoring and control
  - Plan editing and parameter adjustment capabilities
  - Queue history and experiment tracking
  - Direct integration with Queue Server REST API and websocket feeds

- **Unified Data Management**:
  - Single data store combining device states and queue information
  - Real-time updates through websocket connections to both ophyd-websocket and Queue Server
  - TypeScript interfaces ensuring type safety across all components
  - Reactive state management for seamless UI updates

**Technical Implementation:**

**React Component Architecture**:
```typescript
// Core application structure
interface UnifiedClientProps {
  queueServerUrl: string;
  ophydWebsocketUrl: string;
  coordinationServiceUrl: string;
}

// Integrated data context
interface BlueskySystemContext {
  devices: DeviceRegistry;
  queue: QueueState;
  plans: PlanRegistry;
  coordinationStatus: CoordinationState;
  activeConnections: WebSocketConnections;
}
```

**Component Hierarchy**:
- `<UnifiedClient />` - Root application component
  - `<DeviceControlPanel />` - Finch-based device interfaces
  - `<QueueManagementPanel />` - Queue monitor interface  
  - `<LiveDataViewer />` - Real-time data visualization
  - `<CoordinationStatusBar />` - System coordination and health monitoring
  - `<SecurityManager />` - Authentication and access control

**Multi-Service Integration**:
- **Queue Server Service**: Plan submission, queue manipulation, execution monitoring
- **Device Monitoring Service**: Real-time device subscription, control with safety checks
- **Coordination Service**: Lock status, conflict prevention, beamline state coordination
- **Authentication Service**: Single sign-on, role-based access control

**Communication Patterns**:
```
Unified Web Client ↔ nginx reverse proxy ↔ Queue Server Service (experiment management)
                   ↔ nginx reverse proxy ↔ Device Monitoring Service (real-time control)  
                   ↔ Coordination Service (safety & conflict prevention)
                   ↔ Authentication Service (security & access control)
```

**State Management Strategy**:
- Redux Toolkit for complex application state
- React Query for server state synchronization and caching
- Context providers for component-level shared state
- Optimistic updates with automatic rollback on conflicts

**Development & Deployment**:
```bash
# Development setup
npm create react-app@latest unified-bluesky-client --template typescript
npm install @blueskyproject/finch @reduxjs/toolkit react-query
npm install @types/ws socket.io-client react-router-dom
```

**Production Features**:
- Static build deployment optimized for CDN distribution
- Environment-specific configuration injection
- Service discovery integration for dynamic endpoint resolution
- Container-based deployment with Docker and Kubernetes support
- Progressive Web App (PWA) capabilities for offline resilience

**User Experience Design**:
- **Responsive Interface**: Optimized for desktop, tablet, and mobile access
- **Real-time Feedback**: Immediate visual feedback for all user interactions
- **Contextual Safety**: UI elements reflect coordination service state and safety constraints
- **Customizable Dashboards**: User-configurable layouts and widget arrangements
- **Accessibility**: WCAG 2.1 compliant design for universal access

**Security Integration**:
- Single Sign-On (SSO) integration across all Bluesky services
- Role-based access control with service-specific permissions
- Secure websocket connections with authentication tokens
- Audit logging for all user actions and system interactions

**Status:**  
New comprehensive integration combining proven Finch components with queue-monitor functionality, designed for immediate deployment in production beamline environments.

## Deployment Architecture

### Per-Endstation VM Deployment Strategy

**Deployment Philosophy:**  
Each beamline endstation receives a dedicated virtual machine (VM) that hosts a complete, integrated set of backend services. This approach provides isolation, scalability, and simplified management while maintaining the flexibility for beamlines with multiple endstations.

**Services Deployed Per VM:**
- **Queue Server Service** - Experiment execution and management
- **Device Monitoring Service (ophyd-websocket)** - Real-time device control with safety coordination
- **Coordination Service** - Conflict prevention and beamline safety management
- **nginx Reverse Proxy** - Gateway and routing for all services
- **redis** - Persistent storage backend for queue state and coordination
- **Shared Device Registry** - Centralized device configuration and metadata

**Ansible-Based Deployment:**
Building on the existing Queue Server Service Ansible automation, the deployment strategy extends to include all integrated services:

```yaml
# Example Ansible inventory per endstation
[endstation_vm_alpha]
beamline-alpha-vm ansible_host=192.168.1.100

[endstation_vm_beta]  
beamline-beta-vm ansible_host=192.168.1.101

[bluesky_endstations:children]
endstation_vm_alpha
endstation_vm_beta
```

**Integrated Service Stack per VM:**
```
┌─────────────────────────────────────────────────────────────┐
│                    Endstation VM                            │
├─────────────────────────────────────────────────────────────┤
│  nginx Reverse Proxy (HTTPS Gateway)                       │
│  ├─ /api/queue/* → Queue Server Service                    │
│  ├─ /api/devices/* → Device Monitoring Service             │
│  ├─ /api/coordination/* → Coordination Service             │
│  └─ SSL/TLS termination & load balancing                   │
├─────────────────────────────────────────────────────────────┤
│  Queue Server Service                                       │
│  ├─ bluesky-queueserver (queue management & execution)     │
│  ├─ bluesky-httpserver (HTTP API interface)                │
│  └─ Environment & profile collection management            │
├─────────────────────────────────────────────────────────────┤
│  Device Monitoring Service                                  │
│  ├─ ophyd-websocket (FastAPI WebSocket service)            │
│  ├─ Device registry integration                            │
│  └─ Queue Server coordination interfaces                   │
├─────────────────────────────────────────────────────────────┤
│  Coordination Service                                       │
│  ├─ Conflict prevention logic                              │
│  ├─ Safety mechanism enforcement                           │
│  └─ Inter-service communication management                 │
├─────────────────────────────────────────────────────────────┤
│  redis (Shared State Backend)                              │
│  ├─ Queue state persistence                                │
│  ├─ Coordination state management                          │
│  └─ Device registry caching                                │
├─────────────────────────────────────────────────────────────┤
│  Shared Device Registry                                     │
│  ├─ Ophyd object definitions                               │
│  ├─ IOC configurations                                     │
│  └─ Device metadata and capabilities                       │
└─────────────────────────────────────────────────────────────┘
           ↑ EPICS/CA Connections to IOCs ↑
```

**nginx Reverse Proxy Configuration:**
The nginx reverse proxy serves as the single entry point for all client connections:

```nginx
# Example nginx configuration per endstation VM
upstream queue_server {
    server localhost:8080;
}

upstream ophyd_websocket {
    server localhost:8081;  
}

upstream coordination_service {
    server localhost:8082;
}

server {
    listen 443 ssl;
    server_name beamline-alpha.facility.org;
    
    # Queue Server routing
    location /api/queue/ {
        proxy_pass http://queue_server/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Device Monitoring WebSocket routing
    location /api/devices/ {
        proxy_pass http://ophyd_websocket/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # Coordination Service routing
    location /api/coordination/ {
        proxy_pass http://coordination_service/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Ansible Deployment Extension:**
The existing Queue Server Ansible automation extends to support the integrated service stack:

```yaml
# Ansible playbook structure
- name: Deploy Integrated Bluesky Services per Endstation
  hosts: bluesky_endstations
  roles:
    - role: bluesky_queue_server      # Existing role
    - role: bluesky_device_monitoring # New role
    - role: bluesky_coordination      # New role  
    - role: nginx_reverse_proxy       # Enhanced role
    - role: shared_device_registry    # New role
    
  vars:
    endstation_name: "{{ inventory_hostname.split('-')[1] }}"
    service_domain: "{{ endstation_name }}.facility.org"
    nginx_ssl_cert: "/etc/ssl/certs/{{ service_domain }}.crt"
```

**External Web Client Deployment:**
The Unified Web Client is deployed separately from the endstation VMs, providing flexibility for:
- **Central Web Hosting**: Single web application serving multiple endstations
- **CDN Distribution**: Static asset optimization and global availability  
- **Development/Staging**: Independent deployment cycles for UI updates
- **Multi-Endstation Access**: Single interface for users managing multiple endstations

**Web Client to VM Communication:**
```
┌─────────────────────────────────────────────────────────────┐
│                 Unified Web Client                          │
│              (Separate Deployment)                          │
│  ├─ React Application (Static Assets)                      │
│  ├─ Environment-specific configuration                     │
│  └─ Service discovery for endstation VMs                   │
└─────────────────────────────────────────────────────────────┘
                            │ HTTPS
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              nginx Reverse Proxy                            │
│          (Per Endstation VM Gateway)                       │
│  ├─ SSL/TLS termination                                    │
│  ├─ Authentication & authorization                         │
│  ├─ API routing to backend services                       │
│  └─ WebSocket proxy for real-time connections             │
└─────────────────────────────────────────────────────────────┘
```

**Benefits of This Architecture:**
- **Isolation**: Each endstation operates independently with dedicated resources
- **Scalability**: New endstations can be deployed by provisioning additional VMs
- **Maintainability**: Consistent deployment automation across all endstations
- **Security**: Network isolation and controlled access through nginx gateways
- **Flexibility**: Web client can connect to any endstation VM through service discovery
- **Reliability**: Service failures are contained to individual endstations
- **Development**: Independent update cycles for backend services and web client

**Deployment Workflow:**
1. **Provision VM**: Create dedicated VM for new endstation
2. **Run Ansible**: Execute integrated playbook to deploy all services
3. **Configure nginx**: Set up reverse proxy with endstation-specific routing
4. **Deploy Web Client**: Update client configuration to include new endstation
5. **Test Integration**: Validate all services communicate correctly through nginx
6. **Production Handover**: Endstation ready for scientific operations

This deployment strategy ensures that beamlines can scale efficiently while maintaining service isolation and providing a unified user experience across multiple endstations.

## Cross-Service Requirements

### Shared Device Configuration
**Challenge:** Both Queue Server and Device Monitoring services need access to the same:
- Ophyd object definitions
- IOC configurations  
- Device registry information

**Coordination Integration:** While device configuration is shared between ophyd-websocket and Queue Server services, the Coordination Service manages access control to prevent conflicts during plan execution. The coordination service does not directly handle device configuration but coordinates when each service can execute commands.

**Solution Needed:** Determine how to share `bluesky-queueserver/blob/main/bluesky_queueserver/manager/profile_ops.py` functionality across services while maintaining coordination service oversight of device access.

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

### Ophyd Verb Exposure Design Consideration
**Critical Architectural Question:** Should Ophyd device verbs be directly exposed as REST/WebSocket endpoints?

**Ophyd Verbs in Question:**
Ophyd devices provide standardized interaction methods (verbs) that could potentially be exposed as service endpoints:
- **Traditional Ophyd** ([ophyd/device.py](https://github.com/bluesky/ophyd/blob/main/ophyd/device.py)):
  - `set()` - Set device to a target value
  - `trigger()` - Trigger device acquisition/measurement
  - `read()` - Read current device values
  - `describe()` - Get device metadata and signal descriptions
  - `stage()` / `unstage()` - Prepare/cleanup device for acquisition
  - `pause()` / `resume()` - Pause/resume device operations
  - `stop()` - Stop current device operations
- **Ophyd-Async** ([ophyd-async](https://github.com/bluesky/ophyd-async)): 
  - Similar verb patterns but with async/await implementations
  - Enhanced type safety and modern Python patterns

**Design Options:**

**Option 1: Direct Verb Exposure**
```json
POST /api/devices/{device_name}/set
{
  "value": 10.5,
  "timeout": 30
}

POST /api/devices/{device_name}/trigger
{
  "wait": true
}

GET /api/devices/{device_name}/read
GET /api/devices/{device_name}/describe
```

**Option 2: Abstracted Command Interface**
```json
POST /api/devices/{device_name}/command
{
  "action": "set",
  "parameters": {"value": 10.5, "timeout": 30}
}

POST /api/devices/{device_name}/command  
{
  "action": "trigger",
  "parameters": {"wait": true}
}
```

**Option 3: Hybrid Approach**
```json
// Common operations as direct endpoints
PUT /api/devices/{device_name}/value
GET /api/devices/{device_name}/value
GET /api/devices/{device_name}/metadata

// Complex operations through command interface
POST /api/devices/{device_name}/actions
{
  "verb": "stage",
  "parameters": {...}
}
```

**Key Considerations:**

**Advantages of Direct Verb Exposure:**
- **Semantic Clarity**: RESTful URLs directly map to device operations
- **Ophyd Compatibility**: Natural translation from Python API to HTTP API
- **Developer Experience**: Intuitive endpoint design for client developers
- **Type Safety**: Each verb can have specific parameter validation
- **Documentation**: Clear OpenAPI specs for each device operation

**Disadvantages of Direct Verb Exposure:**
- **API Proliferation**: Many endpoints per device type
- **Coupling**: HTTP API tightly coupled to Ophyd implementation details
- **Versioning Complexity**: Changes to Ophyd verbs require API versioning
- **Security Granularity**: Need fine-grained permissions per verb
- **Coordination Complexity**: Each verb needs Queue Server coordination checks

**Impact on Service Architecture:**

**Device Monitoring Service Implications:**
- WebSocket message format needs to support all Ophyd verbs
- Safety coordination required for each verb type
- TypeScript interfaces must reflect full Ophyd verb signatures

**Coordination Service Implications:**
- Must understand semantics of each Ophyd verb for conflict resolution
- Different verbs have different safety requirements (read vs. set vs. trigger)
- Coordination policies may vary per verb type

**Unified Web Client Implications:**
- React components need to support all exposed verbs
- Finch component integration must map to available endpoints
- Error handling varies significantly per verb type

**Recommendation Framework:**
This design decision should be evaluated based on:
1. **Client Development Complexity**: How do different approaches affect Finch and queue-monitor integration?
2. **Safety Implementation**: Which approach best supports Queue Server coordination?
3. **Maintenance Burden**: How do Ophyd updates impact the HTTP API?
4. **Performance Characteristics**: Network overhead and response time implications
5. **Security Model**: Authentication and authorization granularity requirements

**Decision Impact:**
This choice fundamentally affects:
- Device Monitoring Service API design
- Unified Web Client component architecture  
- Coordination Service safety mechanism implementation
- Overall system complexity and maintainability

**Resolution Required:** This design decision must be resolved before finalizing service specifications, as it impacts interface contracts across all four services.

## Architecture Goals

Using our LLM-driven process, we will:

1. **Decompose** each service into complete SRDs (functional requirements) and ICDs (interface contracts)
2. **Build a global system graph** to identify all communication paths and dependencies
3. **Infer and validate all interfaces** between services, ensuring message format consistency
4. **Identify and resolve** architectural issues like the coordination service placement and shared configuration management
5. **Resolve the Ophyd verb exposure design question** and determine the optimal approach for device operation APIs
6. **Design and implement a unified web client** that combines Finch React components with queue-monitor functionality, providing comprehensive access to all four core services while maintaining their independence
7. **Establish enhanced safety mechanisms** through Queue Server coordination and device registry integration
8. **Generate water-tight specifications** that enable independent development of each service with guaranteed integration success

## Expected Outcomes

- Complete `service_architecture.json` files for each of the four core services
- Validated interface contracts for all inter-service communication
- Resolution of coordination service architecture with enhanced safety mechanisms
- Centralized device registry and shared configuration management strategy
- Performance and safety validation ensuring EPICS traffic optimization with coordination safeguards
- **Production-ready Unified Web Client** combining:
  - **Finch React Components**: Modern device control interfaces, MEDM screen replication, real-time monitoring
  - **Queue Monitor Functionality**: Visual queue management, plan editing, experiment tracking
  - **Enhanced Integration**: Single application providing access to all four services
  - **Comprehensive Safety**: UI elements reflecting coordination service state and safety constraints
- **Enhanced Device Monitoring Service** with:
  - Queue Server coordination and conflict prevention
  - Device registry integration and centralized configuration
  - Advanced WebSocket infrastructure supporting multiple concurrent connections
  - TypeScript interfaces and rich metadata support
- **Minimal modification strategy** for existing Bluesky packages while enabling service-oriented architecture
- **Specific interface placement recommendations** - exactly where to add new interfaces without violating package boundaries
- Ready-to-deploy specifications for distributed beamline control system with:
  - Four-service architecture: Queue Server, Device Monitoring, Coordination, and Unified Web Client
  - Enhanced safety mechanisms and conflict prevention
  - Modern React-based user interface combining proven Finch and queue-monitor capabilities
  - Production-grade security, authentication, and access control
  - Comprehensive real-time monitoring and control capabilities
- **Per-Endstation Deployment Architecture** featuring:
  - Dedicated VM per endstation with complete integrated service stack
  - Extended Ansible automation for deployment of all four backend services
  - nginx reverse proxy as single gateway entry point per endstation
  - Separate Unified Web Client deployment with multi-endstation support
  - Service isolation, scalability, and maintainability across beamline facilities
  - Production-ready deployment workflow and operational procedures
- **Complete integration strategy** supporting:
  - Queue Server Service (experiment execution and management)
  - Enhanced Device Monitoring Service (real-time status, device control, and safety coordination)
  - Coordination Service (conflict prevention and beamline safety)
  - Unified Web Client (comprehensive user interface combining Finch and queue-monitor)
- Unified, safe, and efficient user experience while maintaining strict service separation and safety guarantees

