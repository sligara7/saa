#!/usr/bin/env python3
"""
Example: E-commerce Microservices Architecture Analysis
"""
import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import SAA components
from base_models import create_service_architecture, ServiceType
from service_architecture_analyzer import ServiceArchitectureAnalyzer, ProjectConfig, AnalysisLevel
from saa_bootstrap import SAA_ProjectBootstrap

def main():
    # Define e-commerce services
    services = [
        "API Gateway",
        "User Service", 
        "Product Catalog Service",
        "Order Service",
        "Payment Service",
        "Inventory Service",
        "Notification Service",
        "Auth Service",
        "Shopping Cart Service"
    ]
    
    project_name = "ECommerce_Platform"
    base_dir = Path("./ecommerce_analysis")
    
    print("🛒 Creating E-commerce Architecture Analysis")
    
    # Create project
    bootstrap = SAA_ProjectBootstrap(project_name, str(base_dir))
    bootstrap.initialize_project(services)
    
    # Run analysis
    config = ProjectConfig(
        project_name=project_name,
        project_description="E-commerce platform analysis",
        base_directory=str(base_dir)
    )
    
    analyzer = ServiceArchitectureAnalyzer(config)
    services_found = analyzer.discover_services()
    
    if services_found:
        analyzer.analyze_architecture(AnalysisLevel.COMPREHENSIVE)
        analyzer.print_summary()
    else:
        analyzer = None
    
    if analyzer:
        print("\n🎨 Creating visualization...")
        analyzer.visualize_architecture(f"{project_name}_architecture.png")
        
        print("\n📄 Exporting analysis...")
        analyzer.export_analysis(f"{project_name}_analysis.json")
    
    print(f"\n✅ E-commerce analysis complete! Check: {base_dir}")

if __name__ == "__main__":
    main()
