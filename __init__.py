"""
Service Architecture Analyzer (SAA) Package
A generic tool for analyzing service-oriented architectures with NetworkX visualization
"""

from .base_models import (
    ServiceArchitecture, BaseSRD, BaseICD, Interface, InterfaceType,
    ServiceType, ServiceState, VersionInfo, RuntimeInfo, HTTPMethod,
    create_service_architecture
)

from .analyzer import (
    ServiceArchitectureAnalyzer, ProjectConfig, AnalysisLevel
)

from .bootstrap import SAA_ProjectBootstrap

__version__ = "1.0.0"
__author__ = "SAA Development Team"

# Main entry points
def create_project(project_name: str, base_directory: str, services: list = None):
    """Quick project creation"""
    bootstrap = SAA_ProjectBootstrap(project_name, base_directory)
    return bootstrap.initialize_project(services or [])

def analyze_project(project_name: str, base_directory: str, manifest_file: str = None):
    """Quick project analysis"""
    from .analyzer import ProjectConfig, AnalysisLevel
    
    config = ProjectConfig(
        project_name=project_name,
        project_description=f"Analysis for {project_name}",
        base_directory=base_directory
    )
    
    analyzer = ServiceArchitectureAnalyzer(config)
    services = analyzer.discover_services(manifest_file)
    
    if services:
        results = analyzer.analyze_architecture(AnalysisLevel.COMPREHENSIVE)
        analyzer.print_summary()
        return analyzer
    else:
        print("No services found to analyze")
        return None
