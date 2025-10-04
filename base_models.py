"""
Base Pydantic Models for Service Architecture
Foundational classes for SRD and ICD objects with type safety and validation

This module implements UAF-based (Unified Architecture Framework) architectural definitions.
For complete terminology and standards, see: /definitions/architectural_definitions.json

Key UAF Enhancements:
- Hierarchical tier classification (Tier 0: SoS, Tier 1: Systems, Tier 2: Components)
- Service vs Function vs Interface distinctions
- External/non-modifiable system support
- Enhanced dependency typing (direct/indirect/external)
- UAF-based communication patterns (synchronous/asynchronous/bidirectional)
"""

from typing import Dict, List, Optional, Set, Union, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator, ConfigDict
import re


class InterfaceType(str, Enum):
    """Supported interface types"""
    HTTP_ENDPOINT = "http_endpoint"
    MESSAGE = "message"  
    DATA_CONTRACT = "data_contract"
    SERVICE_DEPENDENCY = "service_dependency"
    AUTH_REQUIREMENT = "auth_requirement"
    CACHE_REQUIREMENT = "cache_requirement"
    STORAGE_REQUIREMENT = "storage_requirement"
    ARCHITECTURAL_CONSTRAINT = "architectural_constraint"


class ServiceState(str, Enum):
    """Service operational states"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
    STOPPED = "stopped"


class HTTPMethod(str, Enum):
    """HTTP methods"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class ServiceType(str, Enum):
    """Service classification types"""
    CORE = "core"
    INFRASTRUCTURE = "infrastructure"
    ENHANCED = "enhanced"
    GATEWAY = "gateway"


class HierarchicalTier(str, Enum):
    """UAF-based hierarchical tiers for systematic decomposition"""
    TIER_0_SYSTEM_OF_SYSTEMS = "tier_0_system_of_systems"  # Enterprise/SoS level
    TIER_1_SYSTEMS = "tier_1_systems"  # Individual systems/major services
    TIER_2_COMPONENTS = "tier_2_components"  # Components/packages/sub-services
    TIER_3_INTERNAL_MODULES = "tier_3_internal_modules"  # Classes/methods (conditional)


class ComponentClassification(str, Enum):
    """UAF-based component classification"""
    SERVICE = "service"  # Black-box functionality exposed to external consumers
    FUNCTION = "function"  # Internal behavior within a service
    EXTERNAL = "external"  # External/non-modifiable systems
    INTERFACE_PROTOCOL = "interface_protocol"  # Data transport mechanisms


class DependencyType(str, Enum):
    """Types of dependencies between components"""
    DIRECT = "direct"  # Direct communication between components
    INDIRECT = "indirect"  # Communication through intermediary
    EXTERNAL = "external"  # Dependency on external system


class CommunicationPattern(str, Enum):
    """UAF-based communication patterns"""
    SYNCHRONOUS = "synchronous"  # Request-response, caller waits
    ASYNCHRONOUS = "asynchronous"  # Fire-and-forget, pub-sub
    BIDIRECTIONAL = "bidirectional"  # Two-way communication


class Interface(BaseModel):
    """Represents a single interface (endpoint, message, etc.)"""
    model_config = ConfigDict(use_enum_values=True)
    
    interface_type: InterfaceType
    name: str
    description: str = ""
    method: Optional[HTTPMethod] = None
    path: Optional[str] = None
    request_schema: Optional[Dict[str, Any]] = None
    response_schema: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None
    parameters: Optional[Dict[str, Any]] = None
    dependencies: List[str] = Field(default_factory=list)
    dependency_type: DependencyType = DependencyType.DIRECT
    communication_pattern: CommunicationPattern = CommunicationPattern.SYNCHRONOUS
    rate_limit: Optional[int] = None
    auth_required: bool = False
    timeout: Optional[int] = None
    version: str = "1.0"
    
    @property
    def interface_id(self) -> str:
        """Generate unique identifier for the interface"""
        if self.interface_type == InterfaceType.HTTP_ENDPOINT and self.method and self.path:
            return f"{self.method} {self.path}"
        return f"{self.interface_type}_{self.name.lower().replace(' ', '_')}"
    
    @validator('path')
    def validate_path(cls, v):
        """Validate URL path format"""
        if v and not v.startswith('/'):
            return f"/{v}"
        return v
    
    def matches_interface(self, other: 'Interface') -> bool:
        """Check if this interface matches another interface"""
        return (
            self.interface_type == other.interface_type and
            self.method == other.method and
            self.path == other.path
        )


class RuntimeInfo(BaseModel):
    """Runtime information for a service"""
    model_config = ConfigDict(use_enum_values=True, arbitrary_types_allowed=True)
    
    pid: Optional[int] = None
    port: Optional[int] = None
    host: str = "localhost"
    state: ServiceState = ServiceState.UNKNOWN
    start_time: Optional[datetime] = None
    last_health_check: Optional[datetime] = None
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    active_connections: Optional[int] = None
    
    @property
    def endpoint_url(self) -> str:
        """Get the full endpoint URL for the service"""
        if self.port:
            return f"http://{self.host}:{self.port}"
        return f"http://{self.host}"
    
    @property
    def is_running(self) -> bool:
        """Check if service is currently running"""
        return self.pid is not None and self.state in [ServiceState.HEALTHY, ServiceState.DEGRADED]


class VersionInfo(BaseModel):
    """Version information with semantic versioning"""
    version: str
    date: datetime = Field(default_factory=datetime.now)
    note: str = ""
    
    @validator('version')
    def validate_version(cls, v):
        """Validate semantic version format"""
        if not re.match(r'^\d+\.\d+(\+\d{4}-\d{2}-\d{2})?$', v):
            raise ValueError('Version must be in format "X.Y" or "X.Y+YYYY-MM-DD"')
        return v


class BaseSRD(BaseModel):
    """Base Service Requirements Document"""
    model_config = ConfigDict(use_enum_values=True)
    
    # Core identification
    service_name: str
    service_id: str
    service_directory: str
    version_info: VersionInfo
    
    # Requirements sections
    purpose: str = ""
    business_requirements: List[str] = Field(default_factory=list)
    functional_requirements: List[str] = Field(default_factory=list)
    non_functional_requirements: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    
    # Architecture details
    technology_stack: List[str] = Field(default_factory=list)
    deployment_requirements: Dict[str, Any] = Field(default_factory=dict)
    scaling_requirements: Dict[str, Any] = Field(default_factory=dict)
    security_requirements: List[str] = Field(default_factory=list)
    compliance_requirements: List[str] = Field(default_factory=list)
    
    # Runtime information
    runtime: RuntimeInfo = Field(default_factory=RuntimeInfo)
    service_type: ServiceType = ServiceType.CORE
    
    # UAF-based classifications
    hierarchical_tier: HierarchicalTier = HierarchicalTier.TIER_2_COMPONENTS
    component_classification: ComponentClassification = ComponentClassification.SERVICE
    is_external: bool = False  # Mark external/non-modifiable systems
    parent_system: Optional[str] = None  # Reference to parent in hierarchy
    
    # Metadata
    creation_date: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    stakeholders: List[str] = Field(default_factory=list)
    approval_status: str = "draft"
    
    @validator('service_id', pre=True, always=True)
    def generate_service_id(cls, v, values):
        """Generate service_id from service_name if not provided"""
        if not v and 'service_name' in values:
            return values['service_name'].lower().replace(' ', '_').replace('-', '_')
        return v


class BaseICD(BaseModel):
    """Base Interface Control Document"""
    model_config = ConfigDict(use_enum_values=True)
    
    # Core identification
    service_name: str
    service_id: str
    version_info: VersionInfo
    
    # Interface definitions
    interfaces: List[Interface] = Field(default_factory=list)
    
    # Communication specifications
    base_url: str = ""
    api_version: str = "v1"
    supported_versions: List[str] = Field(default_factory=list)
    deprecated_versions: List[str] = Field(default_factory=list)
    
    # Technical specifications
    authentication: Dict[str, Any] = Field(default_factory=dict)
    rate_limits: Dict[str, int] = Field(default_factory=dict)
    timeouts: Dict[str, int] = Field(default_factory=dict)
    error_handling: Dict[str, Any] = Field(default_factory=dict)
    
    # Communication patterns (UAF-based)
    communication_patterns: List[CommunicationPattern] = Field(default_factory=list)
    message_formats: Dict[str, Dict] = Field(default_factory=dict)
    
    # UAF classifications
    component_classification: ComponentClassification = ComponentClassification.SERVICE
    is_external: bool = False  # Mark external/non-modifiable systems
    
    # Runtime information
    runtime: RuntimeInfo = Field(default_factory=RuntimeInfo)
    
    # Metadata
    creation_date: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    
    @validator('service_id', pre=True, always=True)
    def generate_service_id(cls, v, values):
        """Generate service_id from service_name if not provided"""
        if not v and 'service_name' in values:
            return values['service_name'].lower().replace(' ', '_').replace('-', '_')
        return v
    
    @property
    def provides_interfaces(self) -> Dict[str, Interface]:
        """Get mapping of interfaces this service provides"""
        return {iface.interface_id: iface for iface in self.interfaces}
    
    @property
    def requires_interfaces(self) -> Dict[str, List[str]]:
        """Get mapping of interfaces this service requires from others"""
        requirements = {}
        for iface in self.interfaces:
            if iface.dependencies:
                requirements[iface.interface_id] = iface.dependencies
        return requirements
    
    def has_interface(self, interface_id: str) -> bool:
        """Check if service provides a specific interface"""
        return interface_id in self.provides_interfaces
    
    def add_interface(self, interface: Interface) -> None:
        """Add an interface to this ICD"""
        # Check for duplicates
        existing_ids = {iface.interface_id for iface in self.interfaces}
        if interface.interface_id not in existing_ids:
            self.interfaces.append(interface)
            self.last_updated = datetime.now()
    
    def remove_interface(self, interface_id: str) -> bool:
        """Remove an interface from this ICD"""
        original_count = len(self.interfaces)
        self.interfaces = [iface for iface in self.interfaces if iface.interface_id != interface_id]
        if len(self.interfaces) < original_count:
            self.last_updated = datetime.now()
            return True
        return False
    
    def update_interface(self, interface_id: str, updated_interface: Interface) -> bool:
        """Update an existing interface"""
        for i, iface in enumerate(self.interfaces):
            if iface.interface_id == interface_id:
                self.interfaces[i] = updated_interface
                self.last_updated = datetime.now()
                return True
        return False


class ServiceArchitecture(BaseModel):
    """Complete service architecture combining SRD and ICD"""
    model_config = ConfigDict(use_enum_values=True)
    
    srd: BaseSRD
    icd: BaseICD
    
    @validator('icd')
    def validate_consistency(cls, v, values):
        """Validate that SRD and ICD are consistent"""
        if 'srd' in values:
            srd = values['srd']
            if srd.service_name != v.service_name:
                raise ValueError(f"SRD and ICD service names don't match: {srd.service_name} vs {v.service_name}")
            if srd.service_id != v.service_id:
                raise ValueError(f"SRD and ICD service IDs don't match: {srd.service_id} vs {v.service_id}")
        return v
    
    @property
    def service_id(self) -> str:
        """Get the service identifier"""
        return self.srd.service_id
    
    @property
    def service_name(self) -> str:
        """Get the service name"""
        return self.srd.service_name
    
    def get_networkx_attributes(self) -> Dict[str, Any]:
        """Get attributes for NetworkX node"""
        return {
            'service_name': self.srd.service_name,
            'service_id': self.service_id,
            'service_type': self.srd.service_type,
            'srd_version': self.srd.version_info.version,
            'icd_version': self.icd.version_info.version,
            'purpose': self.srd.purpose,
            'interfaces_count': len(self.icd.interfaces),
            'dependencies_count': len(self.srd.dependencies),
            'technology_stack': self.srd.technology_stack,
            'runtime_state': self.srd.runtime.state,
            'pid': self.srd.runtime.pid,
            'port': self.srd.runtime.port,
            'endpoint_url': self.srd.runtime.endpoint_url,
            'is_running': self.srd.runtime.is_running,
            'provides_interfaces': list(self.icd.provides_interfaces.keys()),
            'requires_interfaces': self.icd.requires_interfaces
        }
    
    def get_edge_data(self, target_service_id: str, interface: Interface) -> Dict[str, Any]:
        """Get edge data for NetworkX edge to target service"""
        return {
            'interface_id': interface.interface_id,
            'interface_type': interface.interface_type,
            'interface_name': interface.name,
            'method': interface.method,
            'path': interface.path,
            'auth_required': interface.auth_required,
            'dependencies': interface.dependencies,
            'source_service': self.service_id,
            'target_service': target_service_id,
            'source_port': self.srd.runtime.port,
            'target_port': None,  # Will be filled by target service
            'version': interface.version
        }
    
    def sync_runtime_info(self) -> None:
        """Synchronize runtime info between SRD and ICD"""
        self.icd.runtime = self.srd.runtime


class SystemComposition(BaseModel):
    """UAF-based system composition model"""
    model_config = ConfigDict(use_enum_values=True)
    
    system_name: str
    system_id: str
    hierarchical_tier: HierarchicalTier
    description: str = ""
    
    # Component references
    component_services: List[str] = Field(default_factory=list)  # Service IDs
    subsystems: List[str] = Field(default_factory=list)  # Child system IDs
    parent_system: Optional[str] = None  # Parent system ID
    
    # System characteristics
    system_boundaries: Dict[str, Any] = Field(default_factory=dict)
    emergent_capabilities: List[str] = Field(default_factory=list)
    governance_policies: List[str] = Field(default_factory=list)
    
    # Integration specifications
    integration_interfaces: List[str] = Field(default_factory=list)
    system_constraints: List[str] = Field(default_factory=list)
    
    # Metadata
    version_info: VersionInfo = Field(default_factory=lambda: VersionInfo(version="1.0"))
    creation_date: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)


class EnhancedDependency(BaseModel):
    """Enhanced dependency specification with UAF-based typing"""
    target_service_id: str
    target_interface_id: str
    dependency_type: DependencyType
    communication_pattern: CommunicationPattern
    is_critical: bool = True
    failover_strategy: Optional[str] = None
    

# Example of how to extend for specific services
class APIGatewaySRD(BaseSRD):
    """API Gateway specific SRD with additional fields"""
    routing_rules: List[Dict[str, str]] = Field(default_factory=list)
    load_balancing_strategy: str = "round_robin"
    ssl_termination: bool = True
    rate_limiting_global: Dict[str, int] = Field(default_factory=dict)


class APIGatewayICD(BaseICD):
    """API Gateway specific ICD with additional fields"""
    routes: List[Dict[str, Any]] = Field(default_factory=list)
    middleware_chain: List[str] = Field(default_factory=list)
    upstream_services: List[str] = Field(default_factory=list)


# Factory function to create service architectures
def create_service_architecture(
    service_name: str,
    service_directory: str,
    srd_version: str,
    icd_version: str,
    service_type: ServiceType = ServiceType.CORE,
    hierarchical_tier: HierarchicalTier = HierarchicalTier.TIER_2_COMPONENTS,
    component_classification: ComponentClassification = ComponentClassification.SERVICE,
    is_external: bool = False,
    parent_system: Optional[str] = None,
    **kwargs
) -> ServiceArchitecture:
    """Factory function to create a UAF-compliant service architecture"""
    
    service_id = service_name.lower().replace(' ', '_').replace('-', '_')
    
    # Create version info
    srd_version_info = VersionInfo(version=srd_version, note="Auto-generated")
    icd_version_info = VersionInfo(version=icd_version, note="Auto-generated")
    
    # Create SRD with UAF fields
    srd_data = {
        'service_name': service_name,
        'service_id': service_id,
        'service_directory': service_directory,
        'version_info': srd_version_info,
        'service_type': service_type,
        'hierarchical_tier': hierarchical_tier,
        'component_classification': component_classification,
        'is_external': is_external,
        'parent_system': parent_system,
        **{k: v for k, v in kwargs.items() if k in BaseSRD.model_fields}
    }
    
    # Use specific SRD class if available
    if service_name == "API Gateway":
        srd = APIGatewaySRD(**srd_data)
    else:
        srd = BaseSRD(**srd_data)
    
    # Create ICD with UAF fields
    icd_data = {
        'service_name': service_name,
        'service_id': service_id,
        'version_info': icd_version_info,
        'component_classification': component_classification,
        'is_external': is_external,
        **{k: v for k, v in kwargs.items() if k in BaseICD.model_fields}
    }
    
    # Use specific ICD class if available
    if service_name == "API Gateway":
        icd = APIGatewayICD(**icd_data)
    else:
        icd = BaseICD(**icd_data)
    
    return ServiceArchitecture(srd=srd, icd=icd)


# Example usage
if __name__ == "__main__":
    # Create a sample service architecture with UAF classifications
    arch = create_service_architecture(
        service_name="Bluesky Queue Server",
        service_directory="./services/bluesky-queueserver",
        srd_version="1.0+2025-09-30",
        icd_version="1.0+2025-09-30",
        service_type=ServiceType.CORE,
        hierarchical_tier=HierarchicalTier.TIER_2_COMPONENTS,
        component_classification=ComponentClassification.SERVICE,
        parent_system="QSaaS_to_OaaS"
    )
    
    # Add an interface with UAF communication pattern
    interface = Interface(
        interface_type=InterfaceType.HTTP_ENDPOINT,
        name="Queue Management API",
        method=HTTPMethod.POST,
        path="/queue/item/add",
        description="Add item to experiment queue",
        communication_pattern=CommunicationPattern.SYNCHRONOUS,
        dependency_type=DependencyType.DIRECT
    )
    
    arch.icd.add_interface(interface)
    
    # Create an external system example
    external_ioc = create_service_architecture(
        service_name="EPICS IOC",
        service_directory="./external/epics-ioc",
        srd_version="1.0+2025-09-30", 
        icd_version="1.0+2025-09-30",
        service_type=ServiceType.INFRASTRUCTURE,
        hierarchical_tier=HierarchicalTier.TIER_2_COMPONENTS,
        component_classification=ComponentClassification.EXTERNAL,
        is_external=True,
        parent_system="Device_Control_System"
    )
    
    # Create a system composition example
    system_composition = SystemComposition(
        system_name="Bluesky Data Acquisition System",
        system_id="bluesky_daq_system",
        hierarchical_tier=HierarchicalTier.TIER_1_SYSTEMS,
        description="Complete data acquisition system for scientific experiments",
        component_services=["bluesky_queue_server", "device_monitoring", "coordination_service"],
        emergent_capabilities=["Automated experiment execution", "Real-time data monitoring"],
        parent_system="Laboratory_Automation_Ecosystem"
    )
    
    print(f"Created architecture for {arch.service_name}")
    print(f"Hierarchical tier: {arch.srd.hierarchical_tier}")
    print(f"Component classification: {arch.srd.component_classification}")
    print(f"Interfaces: {len(arch.icd.interfaces)}")
    print(f"Interface ID: {interface.interface_id}")
    print(f"Communication pattern: {interface.communication_pattern}")
    print(f"External IOC created: {external_ioc.service_name}")
    print(f"System composition: {system_composition.system_name} at {system_composition.hierarchical_tier}")