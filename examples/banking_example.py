#!/usr/bin/env python3
"""
Example: Banking System Architecture Analysis
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import saa_package as saa

def main():
    # Define banking services
    services = [
        "API Gateway",
        "Customer Service",
        "Account Service", 
        "Transaction Service",
        "Payment Processing Service",
        "Credit Scoring Service",
        "Fraud Detection Service",
        "Audit Service",
        "Notification Service",
        "Auth Service",
        "Reporting Service"
    ]
    
    project_name = "Banking_System"
    base_dir = Path("./banking_analysis")
    
    print("🏦 Creating Banking System Architecture Analysis")
    
    # Create project
    bootstrap = saa.SAA_ProjectBootstrap(project_name, str(base_dir))
    bootstrap.initialize_project(services)
    
    # Run comprehensive analysis
    config = saa.ProjectConfig(
        project_name=project_name,
        project_description="Banking system architecture analysis",
        base_directory=str(base_dir)
    )
    
    analyzer = saa.ServiceArchitectureAnalyzer(config)
    services_found = analyzer.discover_services()
    
    if services_found:
        analyzer.analyze_architecture(saa.AnalysisLevel.COMPREHENSIVE)
        analyzer.print_summary()
        
        print("\n🎨 Creating visualization...")
        analyzer.visualize_architecture(f"{project_name}_architecture.png", layout='hierarchical')
        
        print("\n📄 Exporting analysis...")
        analyzer.export_analysis(f"{project_name}_analysis.json")
    
    print(f"\n✅ Banking analysis complete! Check: {base_dir}")

if __name__ == "__main__":
    main()
