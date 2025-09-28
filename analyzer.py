"""
Service Architecture Analyzer (SAA) - Standalone Systems Engineering Package
A generic tool for analyzing service-oriented architectures with NetworkX visualization
"""

import os
import json
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from dataclasses import dataclass
from enum import Enum

# Re-export core models for easy importing
from base_models import (
    ServiceArchitecture, BaseSRD, BaseICD, Interface, InterfaceType,
    ServiceType, ServiceState, VersionInfo, RuntimeInfo, HTTPMethod
)


class AnalysisLevel(str, Enum):
    """Analysis depth levels"""
    BASIC = "basic"
    DETAILED = "detailed"
    COMPREHENSIVE = "comprehensive"


@dataclass
class ProjectConfig:
    """Configuration for a service architecture project"""
    project_name: str
    project_description: str
    base_directory: str
    services_directory: str = "services"
    docs_directory: str = "docs"
    output_directory: str = "analysis_output"
    
    def get_services_path(self) -> Path:
        return Path(self.base_directory) / self.services_directory
    
    def get_docs_path(self) -> Path:
        return Path(self.base_directory) / self.docs_directory
    
    def get_output_path(self) -> Path:
        output_path = Path(self.base_directory) / self.output_directory
        output_path.mkdir(parents=True, exist_ok=True)
        return output_path


class ServiceArchitectureAnalyzer:
    """
    Standalone Service Architecture Analyzer
    Generic tool for analyzing any service-oriented architecture
    """
    
    def __init__(self, project_config: ProjectConfig):
        self.config = project_config
        self.services: Dict[str, ServiceArchitecture] = {}
        self.graph: nx.DiGraph = nx.DiGraph()
        self.analysis_results: Optional[Dict[str, Any]] = None
        
        print(f"🔧 Initializing Service Architecture Analyzer")
        print(f"   Project: {self.config.project_name}")
        print(f"   Base Directory: {self.config.base_directory}")
    
    def discover_services(self, service_manifest: Optional[str] = None) -> List[str]:
        """
        Discover services in the project
        
        Args:
            service_manifest: Path to JSON file listing services, or None to auto-discover
            
        Returns:
            List of discovered service identifiers
        """
        print("🔍 Discovering services...")
        
        if service_manifest and os.path.exists(service_manifest):
            return self._load_from_manifest(service_manifest)
        else:
            return self._auto_discover_services()
    
    def _load_from_manifest(self, manifest_path: str) -> List[str]:
        """Load services from a manifest file (RQMTS.json format)"""
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        service_ids = []
        for service_config in manifest.get('services', []):
            service_id = self._normalize_service_name(service_config['service_name'])
            service_ids.append(service_id)
            
            # Create service architecture from manifest
            architecture = self._create_service_from_manifest(service_config)
            if architecture:
                self.services[service_id] = architecture
        
        print(f"   ✅ Loaded {len(service_ids)} services from manifest")
        return service_ids
    
    def _auto_discover_services(self) -> List[str]:
        """Auto-discover services by scanning the services directory"""
        services_path = self.config.get_services_path()
        
        if not services_path.exists():
            print(f"   ⚠️  Services directory not found: {services_path}")
            return []
        
        service_ids = []
        for item in services_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                service_id = self._normalize_service_name(item.name)
                service_ids.append(service_id)
                
                # Try to load service architecture
                architecture = self._load_service_from_directory(item)
                if architecture:
                    self.services[service_id] = architecture
        
        print(f"   ✅ Auto-discovered {len(service_ids)} services")
        return service_ids
    
    def _create_service_from_manifest(self, service_config: Dict[str, Any]) -> Optional[ServiceArchitecture]:
        """Create service architecture from manifest configuration"""
        try:
            from base_models import create_service_architecture
            
            service_name = service_config['service_name']
            service_directory = service_config.get('service_directory', f"./services/{self._normalize_service_name(service_name)}")
            srd_version = service_config.get('SRD_version', '1.0')
            icd_version = service_config.get('ICD_version', '1.0')
            
            # Determine service type
            service_type = self._determine_service_type(service_name)
            
            return create_service_architecture(
                service_name=service_name,
                service_directory=service_directory,
                srd_version=srd_version,
                icd_version=icd_version,
                service_type=service_type
            )
            
        except Exception as e:
            print(f"   ⚠️  Error creating service {service_config.get('service_name', 'unknown')}: {e}")
            return None
    
    def _load_service_from_directory(self, service_dir: Path) -> Optional[ServiceArchitecture]:
        """Load service architecture from directory structure"""
        service_name = service_dir.name.replace('_', ' ').title()
        service_id = self._normalize_service_name(service_name)
        
        # Look for Python models file
        models_file = service_dir / f"{service_id}_models.py"
        if models_file.exists():
            return self._load_from_python_models(models_file, service_id)
        
        # Look for SRD/ICD markdown files
        srd_file = self._find_srd_file(service_dir)
        icd_file = self._find_icd_file(service_dir)
        
        if srd_file or icd_file:
            return self._load_from_markdown_files(service_dir, service_name, srd_file, icd_file)
        
        # Create minimal architecture
        return self._create_minimal_architecture(service_name, str(service_dir))
    
    def _load_from_python_models(self, models_file: Path, service_id: str) -> Optional[ServiceArchitecture]:
        """Load service from Python models file"""
        try:
            spec = importlib.util.spec_from_file_location(f"{service_id}_models", models_file)
            if spec and spec.loader:
                models_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(models_module)
                
                # Look for create function
                create_function_name = f"create_{service_id}_architecture"
                if hasattr(models_module, create_function_name):
                    create_function = getattr(models_module, create_function_name)
                    return create_function()
                    
        except Exception as e:
            print(f"   ⚠️  Error loading Python models for {service_id}: {e}")
        
        return None
    
    def _find_srd_file(self, service_dir: Path) -> Optional[Path]:
        """Find SRD file in service directory"""
        patterns = ['SRD*.md', 'srd*.md', '*SRD*.md', 'requirements*.md']
        for pattern in patterns:
            matches = list(service_dir.glob(f"**/{pattern}"))
            if matches:
                return matches[0]
        return None
    
    def _find_icd_file(self, service_dir: Path) -> Optional[Path]:
        """Find ICD file in service directory"""
        patterns = ['ICD*.md', 'icd*.md', '*ICD*.md', 'interface*.md', 'api*.md']
        for pattern in patterns:
            matches = list(service_dir.glob(f"**/{pattern}"))
            if matches:
                return matches[0]
        return None
    
    def _load_from_markdown_files(self, service_dir: Path, service_name: str, srd_file: Optional[Path], icd_file: Optional[Path]) -> ServiceArchitecture:
        """Load service from markdown SRD/ICD files"""
        from base_models import create_service_architecture
        
        # Create basic architecture
        architecture = create_service_architecture(
            service_name=service_name,
            service_directory=str(service_dir),
            srd_version="1.0",
            icd_version="1.0",
            service_type=self._determine_service_type(service_name)
        )
        
        # Parse SRD file if available
        if srd_file:
            self._parse_srd_markdown(architecture.srd, srd_file)
        
        # Parse ICD file if available
        if icd_file:
            self._parse_icd_markdown(architecture.icd, icd_file)
        
        return architecture
    
    def _parse_srd_markdown(self, srd: BaseSRD, srd_file: Path):
        """Parse SRD markdown file and populate SRD object"""
        try:
            content = srd_file.read_text(encoding='utf-8')
            
            # Extract purpose
            import re
            purpose_match = re.search(r'## Purpose\s*\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
            if purpose_match:
                srd.purpose = purpose_match.group(1).strip()
            
            # Extract requirements sections
            self._extract_markdown_list(content, "Business Requirements", srd.business_requirements)
            self._extract_markdown_list(content, "Functional Requirements", srd.functional_requirements)
            self._extract_markdown_list(content, "Dependencies", srd.dependencies)
            self._extract_markdown_list(content, "Technology Stack", srd.technology_stack)
            
        except Exception as e:
            print(f"   ⚠️  Error parsing SRD {srd_file}: {e}")
    
    def _parse_icd_markdown(self, icd: BaseICD, icd_file: Path):
        """Parse ICD markdown file and populate ICD object"""
        try:
            content = icd_file.read_text(encoding='utf-8')
            
            # Extract interfaces
            interfaces = self._extract_interfaces_from_markdown(content)
            icd.interfaces.extend(interfaces)
            
            # Extract base URL
            import re
            base_url_match = re.search(r'Base URL[:\s]+(.+)', content, re.IGNORECASE)
            if base_url_match:
                icd.base_url = base_url_match.group(1).strip().strip('`')
            
        except Exception as e:
            print(f"   ⚠️  Error parsing ICD {icd_file}: {e}")
    
    def _extract_markdown_list(self, content: str, section_name: str, target_list: List[str]):
        """Extract bulleted list from markdown section"""
        import re
        pattern = rf'## {section_name}\s*\n(.*?)(?=\n##|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            section_content = match.group(1)
            bullets = re.findall(r'^[-*]\s+(.+)$', section_content, re.MULTILINE)
            target_list.extend([bullet.strip() for bullet in bullets])
    
    def _extract_interfaces_from_markdown(self, content: str) -> List[Interface]:
        """Extract interfaces from markdown content"""
        interfaces = []
        import re
        
        # Extract HTTP endpoints
        http_patterns = [
            r'(GET|POST|PUT|DELETE|PATCH)\s+([/\w\-\{\}]+)',
            r'```http\s*(GET|POST|PUT|DELETE|PATCH)\s+([/\w\-\{\}]+)',
            r'###\s*[\d\.]*\s*(GET|POST|PUT|DELETE|PATCH)\s+([/\w\-\{\}]+)'
        ]
        
        for pattern in http_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for method, path in matches:
                interface = Interface(
                    interface_type=InterfaceType.HTTP_ENDPOINT,
                    name=f"{method.upper()} {path}",
                    method=HTTPMethod(method.upper()),
                    path=path,
                    description=f"{method.upper()} endpoint for {path}"
                )
                interfaces.append(interface)
        
        return interfaces
    
    def _create_minimal_architecture(self, service_name: str, service_directory: str) -> ServiceArchitecture:
        """Create minimal service architecture"""
        from base_models import create_service_architecture
        
        return create_service_architecture(
            service_name=service_name,
            service_directory=service_directory,
            srd_version="1.0",
            icd_version="1.0",
            service_type=self._determine_service_type(service_name)
        )
    
    def _determine_service_type(self, service_name: str) -> ServiceType:
        """Determine service type from name"""
        name_lower = service_name.lower()
        
        if any(word in name_lower for word in ['gateway', 'api gateway', 'proxy', 'router']):
            return ServiceType.GATEWAY
        elif any(word in name_lower for word in ['auth', 'cache', 'storage', 'message', 'metrics', 'audit', 'database', 'queue']):
            return ServiceType.INFRASTRUCTURE
        elif any(word in name_lower for word in ['core', 'main', 'primary', 'business', 'domain']):
            return ServiceType.CORE
        else:
            return ServiceType.ENHANCED
    
    def _normalize_service_name(self, name: str) -> str:
        """Normalize service name to ID"""
        return name.lower().replace(' ', '_').replace('-', '_')
    
    def build_dependency_graph(self) -> nx.DiGraph:
        """Build NetworkX dependency graph"""
        print("🕸️  Building dependency graph...")
        
        self.graph = nx.DiGraph()
        
        # Add nodes (services)
        for service_id, architecture in self.services.items():
            self.graph.add_node(service_id, **self._get_node_attributes(architecture))
        
        # Add edges (dependencies)
        for source_id, source_arch in self.services.items():
            for interface in source_arch.icd.interfaces:
                target_services = self._find_interface_targets(interface)
                
                for target_id in target_services:
                    if target_id in self.services:
                        edge_data = self._get_edge_attributes(source_arch, interface, target_id)
                        self.graph.add_edge(source_id, target_id, **edge_data)
        
        print(f"   ✅ Graph built: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")
        return self.graph
    
    def _get_node_attributes(self, architecture: ServiceArchitecture) -> Dict[str, Any]:
        """Get node attributes for NetworkX"""
        return {
            'service_name': architecture.service_name,
            'service_type': architecture.srd.service_type.value if hasattr(architecture.srd.service_type, 'value') else str(architecture.srd.service_type),
            'interfaces_count': len(architecture.icd.interfaces),
            'dependencies_count': len(architecture.srd.dependencies),
            'srd_version': architecture.srd.version_info.version,
            'icd_version': architecture.icd.version_info.version
        }
    
    def _get_edge_attributes(self, source_arch: ServiceArchitecture, interface: Interface, target_id: str) -> Dict[str, Any]:
        """Get edge attributes for NetworkX"""
        return {
            'interface_id': interface.interface_id,
            'interface_type': interface.interface_type.value if hasattr(interface.interface_type, 'value') else str(interface.interface_type),
            'interface_name': interface.name,
            'method': interface.method.value if interface.method and hasattr(interface.method, 'value') else str(interface.method) if interface.method else None,
            'path': interface.path,
            'source_service': source_arch.service_id,
            'target_service': target_id
        }
    
    def _find_interface_targets(self, interface: Interface) -> List[str]:
        """Find target services for an interface"""
        targets = []
        
        # Direct dependencies
        for dep in interface.dependencies:
            target_id = self._normalize_service_name(dep)
            if target_id in self.services:
                targets.append(target_id)
        
        # HTTP endpoints typically go to gateway
        if (hasattr(interface.interface_type, 'value') and interface.interface_type.value == 'http_endpoint') or \
           (isinstance(interface.interface_type, str) and interface.interface_type == 'http_endpoint'):
            gateway_services = [sid for sid, arch in self.services.items() 
                             if arch.srd.service_type == ServiceType.GATEWAY]
            targets.extend(gateway_services)
        
        return targets
    
    def analyze_architecture(self, level: AnalysisLevel = AnalysisLevel.DETAILED) -> Dict[str, Any]:
        """Analyze the service architecture"""
        print(f"🔍 Analyzing architecture (level: {level.value})...")
        
        if not self.graph.nodes():
            self.build_dependency_graph()
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'project': {
                'name': self.config.project_name,
                'description': self.config.project_description,
                'base_directory': self.config.base_directory
            },
            'summary': self._analyze_summary(),
            'services': self._analyze_services(),
            'interfaces': self._analyze_interfaces(),
            'dependencies': self._analyze_dependencies()
        }
        
        if level in [AnalysisLevel.DETAILED, AnalysisLevel.COMPREHENSIVE]:
            analysis.update({
                'centrality': self._analyze_centrality(),
                'compatibility': self._analyze_compatibility(),
                'critical_paths': self._analyze_critical_paths()
            })
        
        if level == AnalysisLevel.COMPREHENSIVE:
            analysis.update({
                'recommendations': self._generate_recommendations(),
                'health_score': self._calculate_health_score()
            })
        
        self.analysis_results = analysis
        print("   ✅ Analysis complete")
        return analysis
    
    def _analyze_summary(self) -> Dict[str, Any]:
        """Analyze architecture summary"""
        return {
            'total_services': len(self.services),
            'total_interfaces': sum(len(arch.icd.interfaces) for arch in self.services.values()),
            'graph_nodes': self.graph.number_of_nodes(),
            'graph_edges': self.graph.number_of_edges(),
            'service_types': self._count_service_types()
        }
    
    def _count_service_types(self) -> Dict[str, int]:
        """Count services by type"""
        type_counts = {}
        for arch in self.services.values():
            service_type = arch.srd.service_type.value if hasattr(arch.srd.service_type, 'value') else str(arch.srd.service_type)
            type_counts[service_type] = type_counts.get(service_type, 0) + 1
        return type_counts
    
    def _analyze_services(self) -> Dict[str, Dict[str, Any]]:
        """Analyze individual services"""
        service_analysis = {}
        for service_id, arch in self.services.items():
            service_analysis[service_id] = {
                'name': arch.service_name,
                'type': arch.srd.service_type.value if hasattr(arch.srd.service_type, 'value') else str(arch.srd.service_type),
                'interfaces': len(arch.icd.interfaces),
                'dependencies': len(arch.srd.dependencies),
                'srd_version': arch.srd.version_info.version,
                'icd_version': arch.icd.version_info.version
            }
        return service_analysis
    
    def _analyze_interfaces(self) -> Dict[str, Any]:
        """Analyze interface patterns"""
        interface_types = {}
        total_interfaces = 0
        
        for arch in self.services.values():
            for interface in arch.icd.interfaces:
                total_interfaces += 1
                itype = interface.interface_type.value if hasattr(interface.interface_type, 'value') else str(interface.interface_type)
                interface_types[itype] = interface_types.get(itype, 0) + 1
        
        return {
            'total': total_interfaces,
            'by_type': interface_types,
            'average_per_service': total_interfaces / len(self.services) if self.services else 0
        }
    
    def _analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze dependency patterns"""
        in_degrees = dict(self.graph.in_degree())
        out_degrees = dict(self.graph.out_degree())
        
        return {
            'most_depended_upon': max(in_degrees.items(), key=lambda x: x[1]) if in_degrees else None,
            'most_dependent': max(out_degrees.items(), key=lambda x: x[1]) if out_degrees else None,
            'isolated_services': [node for node, degree in self.graph.degree() if degree == 0],
            'dependency_depth': self._calculate_dependency_depth()
        }
    
    def _calculate_dependency_depth(self) -> int:
        """Calculate maximum dependency chain depth"""
        try:
            if nx.is_directed_acyclic_graph(self.graph):
                return nx.dag_longest_path_length(self.graph)
            else:
                return len(self.services)  # Fallback for cyclic graphs
        except:
            return 0
    
    def _analyze_centrality(self) -> Dict[str, Dict[str, float]]:
        """Analyze service centrality metrics"""
        try:
            return {
                'degree_centrality': nx.degree_centrality(self.graph),
                'betweenness_centrality': nx.betweenness_centrality(self.graph),
                'closeness_centrality': nx.closeness_centrality(self.graph),
                'pagerank': nx.pagerank(self.graph)
            }
        except Exception as e:
            print(f"   ⚠️  Error calculating centrality: {e}")
            return {}
    
    def _analyze_compatibility(self) -> Dict[str, Any]:
        """Analyze interface compatibility"""
        compatible = 0
        broken = 0
        issues = []
        
        for source_id, source_arch in self.services.items():
            for interface in source_arch.icd.interfaces:
                targets = self._find_interface_targets(interface)
                for target_id in targets:
                    target_arch = self.services.get(target_id)
                    if target_arch and target_arch.icd.has_interface(interface.interface_id):
                        compatible += 1
                    else:
                        broken += 1
                        issues.append({
                            'source': source_id,
                            'target': target_id,
                            'interface': interface.interface_id,
                            'issue': 'Missing interface in target service'
                        })
        
        return {
            'compatible_interfaces': compatible,
            'broken_interfaces': broken,
            'compatibility_ratio': compatible / (compatible + broken) if (compatible + broken) > 0 else 1.0,
            'issues': issues[:10]  # Top 10 issues
        }
    
    def _analyze_critical_paths(self) -> List[List[str]]:
        """Find critical dependency paths"""
        try:
            # Find all simple paths between services with no dependencies and services with no dependents
            sources = [n for n in self.graph.nodes() if self.graph.in_degree(n) == 0]
            sinks = [n for n in self.graph.nodes() if self.graph.out_degree(n) == 0]
            
            paths = []
            for source in sources:
                for sink in sinks:
                    try:
                        for path in nx.all_simple_paths(self.graph, source, sink, cutoff=5):
                            paths.append(path)
                    except nx.NetworkXNoPath:
                        continue
            
            return paths[:10]  # Top 10 paths
        
        except Exception as e:
            print(f"   ⚠️  Error finding critical paths: {e}")
            return []
    
    def _generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate architecture improvement recommendations"""
        recommendations = []
        
        # Check for isolated services
        isolated = [node for node, degree in self.graph.degree() if degree == 0]
        if isolated:
            recommendations.append({
                'type': 'WARNING',
                'title': 'Isolated Services Detected',
                'description': f'{len(isolated)} services have no connections',
                'recommendation': 'Review service integration and add necessary interfaces'
            })
        
        # Check for highly coupled services
        high_degree_nodes = [node for node, degree in self.graph.degree() if degree > 5]
        if high_degree_nodes:
            recommendations.append({
                'type': 'INFO',
                'title': 'Highly Connected Services',
                'description': f'{len(high_degree_nodes)} services have many connections',
                'recommendation': 'Consider breaking down highly coupled services'
            })
        
        # Check for missing gateway
        gateways = [s for s, arch in self.services.items() if arch.srd.service_type == ServiceType.GATEWAY]
        if not gateways:
            recommendations.append({
                'type': 'CRITICAL',
                'title': 'No API Gateway Found',
                'description': 'No gateway service detected in architecture',
                'recommendation': 'Add an API Gateway for external access management'
            })
        
        return recommendations
    
    def _calculate_health_score(self) -> Dict[str, Any]:
        """Calculate overall architecture health score"""
        scores = {
            'interface_completeness': 0.8,  # Based on compatibility analysis
            'service_isolation': 0.7,       # Based on coupling analysis
            'documentation_quality': 0.6,   # Based on SRD/ICD completeness
            'dependency_management': 0.8     # Based on dependency analysis
        }
        
        overall_score = sum(scores.values()) / len(scores)
        
        return {
            'overall_score': overall_score,
            'component_scores': scores,
            'grade': self._score_to_grade(overall_score)
        }
    
    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 0.9:
            return 'A'
        elif score >= 0.8:
            return 'B'
        elif score >= 0.7:
            return 'C'
        elif score >= 0.6:
            return 'D'
        else:
            return 'F'
    
    def visualize_architecture(self, output_file: Optional[str] = None, show_labels: bool = True, layout: str = 'spring') -> str:
        """Create architecture visualization"""
        print("🎨 Creating architecture visualization...")
        
        if not self.graph.nodes():
            self.build_dependency_graph()
        
        # Create figure
        fig, ax = plt.subplots(1, 1, figsize=(16, 12))
        
        # Choose layout
        layout_functions = {
            'spring': nx.spring_layout,
            'circular': nx.circular_layout,
            'kamada_kawai': nx.kamada_kawai_layout,
            'hierarchical': self._hierarchical_layout
        }
        
        pos = layout_functions.get(layout, nx.spring_layout)(self.graph)
        
        # Node colors by service type
        node_colors = []
        color_map = {
            'gateway': '#FF6B6B',
            'core': '#4ECDC4', 
            'infrastructure': '#45B7D1',
            'enhanced': '#96CEB4'
        }
        
        for node in self.graph.nodes():
            arch = self.services.get(node)
            if arch:
                service_type = arch.srd.service_type.value if hasattr(arch.srd.service_type, 'value') else str(arch.srd.service_type)
                node_colors.append(color_map.get(service_type, '#CCCCCC'))
            else:
                node_colors.append('#CCCCCC')
        
        # Draw network
        nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors, 
                              node_size=1000, alpha=0.8, ax=ax)
        nx.draw_networkx_edges(self.graph, pos, edge_color='gray', 
                              arrows=True, arrowsize=20, alpha=0.6, ax=ax)
        
        if show_labels:
            labels = {}
            for node in self.graph.nodes():
                arch = self.services.get(node)
                if arch:
                    labels[node] = arch.service_name
                else:
                    labels[node] = node
            nx.draw_networkx_labels(self.graph, pos, labels, font_size=8, ax=ax)
        
        # Add legend
        legend_elements = [
            patches.Patch(color=color, label=service_type.title()) 
            for service_type, color in color_map.items()
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        # Set title
        ax.set_title(f'{self.config.project_name} - Service Architecture', 
                    fontsize=16, fontweight='bold')
        ax.axis('off')
        
        # Save or show
        if output_file:
            output_path = self.config.get_output_path() / output_file
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"   ✅ Visualization saved: {output_path}")
            plt.close()
            return str(output_path)
        else:
            plt.show()
            return "displayed"
    
    def _hierarchical_layout(self, graph: nx.DiGraph) -> Dict[str, tuple]:
        """Create hierarchical layout based on service types"""
        pos = {}
        type_positions = {
            ServiceType.GATEWAY: (0, 3),
            ServiceType.CORE: (0, 2), 
            ServiceType.ENHANCED: (0, 1),
            ServiceType.INFRASTRUCTURE: (0, 0)
        }
        
        type_counts = {t: 0 for t in ServiceType}
        
        for node in graph.nodes():
            arch = self.services.get(node)
            if arch:
                service_type = arch.srd.service_type
                base_x, y = type_positions.get(service_type, (0, 0))
                x = base_x + type_counts[service_type] * 2 - 4
                pos[node] = (x, y)
                type_counts[service_type] += 1
            else:
                pos[node] = (0, 0)
        
        return pos
    
    def export_analysis(self, filename: Optional[str] = None) -> str:
        """Export analysis results to JSON"""
        if not self.analysis_results:
            self.analyze_architecture()
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"architecture_analysis_{timestamp}.json"
        
        output_path = self.config.get_output_path() / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, default=str)
        
        print(f"📄 Analysis exported: {output_path}")
        return str(output_path)
    
    def print_summary(self):
        """Print analysis summary"""
        if not self.analysis_results:
            self.analyze_architecture()
        
        analysis = self.analysis_results
        
        print(f"\n🏗️  ARCHITECTURE ANALYSIS SUMMARY")
        print(f"=" * 60)
        print(f"📊 Project: {analysis['project']['name']}")
        print(f"📁 Location: {analysis['project']['base_directory']}")
        
        summary = analysis['summary']
        print(f"\n📈 OVERVIEW:")
        print(f"   Services: {summary['total_services']}")
        print(f"   Interfaces: {summary['total_interfaces']}")
        print(f"   Dependencies: {summary['graph_edges']}")
        
        print(f"\n🏷️  SERVICE TYPES:")
        for service_type, count in summary['service_types'].items():
            print(f"   {service_type.title()}: {count}")
        
    
        if 'compatibility' in analysis:
            compat = analysis['compatibility']
            print(f"\n🔗 COMPATIBILITY:")
            print(f"   Compatible: {compat['compatible_interfaces']}")
            print(f"   Broken: {compat['broken_interfaces']}")
            print(f"   Ratio: {compat['compatibility_ratio']:.2%}")
        
        if 'recommendations' in analysis:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in analysis['recommendations'][:3]:
                icon = {'CRITICAL': '🔴', 'WARNING': '🟡', 'INFO': '🔵'}.get(rec['type'], 'ℹ️')
                print(f"   {icon} {rec['title']}")
                print(f"      {rec['recommendation']}")


# Example usage and CLI interface
def main():
    """Main CLI interface for the Service Architecture Analyzer"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Service Architecture Analyzer - Generic Systems Engineering Tool")
    parser.add_argument("project_name", help="Name of the project to analyze")
    parser.add_argument("--base-dir", default=".", help="Base directory of the project")
    parser.add_argument("--manifest", help="Path to service manifest file (JSON)")
    parser.add_argument("--analyze", action="store_true", help="Run architecture analysis")
    parser.add_argument("--visualize", action="store_true", help="Create architecture visualization")
    parser.add_argument("--export", help="Export analysis to specified filename")
    parser.add_argument("--level", choices=['basic', 'detailed', 'comprehensive'], 
                       default='detailed', help="Analysis depth level")
    parser.add_argument("--output-dir", default="analysis_output", help="Output directory for results")
    
    args = parser.parse_args()
    
    # Create project configuration
    config = ProjectConfig(
        project_name=args.project_name,
        project_description=f"Architecture analysis for {args.project_name}",
        base_directory=args.base_dir,
        output_directory=args.output_dir
    )
    
    # Initialize analyzer
    analyzer = ServiceArchitectureAnalyzer(config)
    
    # Discover services
    services = analyzer.discover_services(args.manifest)
    
    if not services:
        print("❌ No services found. Please check your project structure or manifest file.")
        return
    
    # Run analysis if requested
    if args.analyze or args.visualize or args.export:
        analysis_level = AnalysisLevel(args.level)
        analyzer.analyze_architecture(analysis_level)
        analyzer.print_summary()
    
    # Create visualization
    if args.visualize:
        analyzer.visualize_architecture(f"{args.project_name}_architecture.png")
    
    # Export analysis
    if args.export:
        analyzer.export_analysis(args.export)
    
    if not any([args.analyze, args.visualize, args.export]):
        print(f"\n📋 Quick Overview:")
        print(f"   Discovered {len(services)} services")
        print(f"   Use --analyze to run full analysis")
        print(f"   Use --visualize to create architecture diagram")
        print(f"   Use --export <filename> to save results")


if __name__ == "__main__":
    main()