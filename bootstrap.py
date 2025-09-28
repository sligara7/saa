"""
Generic Service Architecture Analysis Package
Setup script for creating standalone analysis environments
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class SAA_ProjectBootstrap:
    """
    Service Architecture Analyzer Project Bootstrap
    Creates a new project environment for architecture analysis
    """
    
    TEMPLATE_CONFIG = {
        "project_name": "",
        "project_description": "",
        "base_directory": "",
        "services_directory": "services",
        "docs_directory": "docs", 
        "output_directory": "analysis_output"
    }
    
    TEMPLATE_MANIFEST = {
        "format_version": "1.0",
        "project_name": "",
        "created_date": "",
        "services": []
    }
    
    SERVICE_TEMPLATE = {
        "service_name": "",
        "service_directory": "",
        "service_type": "enhanced",
        "SRD_version": "1.0",
        "ICD_version": "1.0",
        "architecture_config": {
            "port": None,
            "pid": None,
            "health_check_url": None
        }
    }
    
    def __init__(self, project_name: str, base_directory: str):
        self.project_name = project_name
        self.base_directory = Path(base_directory).resolve()
        self.config_file = self.base_directory / "saa_config.json"
        self.manifest_file = self.base_directory / "services_manifest.json"
    
    def initialize_project(self, services: Optional[List[str]] = None) -> str:
        """Initialize a new SAA analysis project"""
        print(f"🚀 Initializing SAA project: {self.project_name}")
        print(f"   Directory: {self.base_directory}")
        
        # Create directory structure
        self._create_directory_structure()
        
        # Create configuration files
        self._create_config_files(services or [])
        
        # Copy SAA core files
        self._setup_analysis_environment()
        
        # Create example service files
        if services:
            self._create_example_services(services)
        
        # Create README
        self._create_readme()
        
        print(f"✅ Project initialized successfully!")
        print(f"   Configuration: {self.config_file}")
        print(f"   Service Manifest: {self.manifest_file}")
        print(f"\n📖 Next Steps:")
        print(f"   1. Edit {self.manifest_file} to define your services")
        print(f"   2. Create SRD/ICD documentation for each service")
        print(f"   3. Run: python saa_analyze.py {self.project_name}")
        
        return str(self.base_directory)
    
    def _create_directory_structure(self):
        """Create project directory structure"""
        directories = [
            "",  # Base directory
            "services",
            "docs", 
            "analysis_output",
            "templates",
            "scripts"
        ]
        
        for dir_path in directories:
            full_path = self.base_directory / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
    
    def _create_config_files(self, services: List[str]):
        """Create configuration files"""
        # Project configuration
        config = self.TEMPLATE_CONFIG.copy()
        config.update({
            "project_name": self.project_name,
            "project_description": f"Service architecture analysis for {self.project_name}",
            "base_directory": str(self.base_directory)
        })
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        # Service manifest
        manifest = self.TEMPLATE_MANIFEST.copy()
        manifest.update({
            "project_name": self.project_name,
            "created_date": datetime.now().isoformat(),
            "services": [self._create_service_entry(service) for service in services]
        })
        
        with open(self.manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
    
    def _create_service_entry(self, service_name: str) -> Dict[str, Any]:
        """Create service entry for manifest"""
        service_id = service_name.lower().replace(' ', '_').replace('-', '_')
        
        entry = self.SERVICE_TEMPLATE.copy()
        entry.update({
            "service_name": service_name,
            "service_directory": f"./services/{service_id}",
            "service_type": self._guess_service_type(service_name)
        })
        
        return entry
    
    def _guess_service_type(self, service_name: str) -> str:
        """Guess service type from name"""
        name_lower = service_name.lower()
        
        if any(word in name_lower for word in ['gateway', 'api gateway', 'proxy', 'router']):
            return "gateway"
        elif any(word in name_lower for word in ['auth', 'cache', 'storage', 'message', 'metrics', 'audit', 'database', 'queue']):
            return "infrastructure" 
        elif any(word in name_lower for word in ['core', 'main', 'primary', 'business', 'domain']):
            return "core"
        else:
            return "enhanced"
    
    def _setup_analysis_environment(self):
        """Setup analysis environment by copying core files"""
        current_dir = Path(__file__).parent
        
        core_files = [
            "base_models.py",
            "service_architecture_analyzer.py"
        ]
        
        for filename in core_files:
            source_file = current_dir / filename
            if source_file.exists():
                dest_file = self.base_directory / filename
                shutil.copy2(source_file, dest_file)
                print(f"   📄 Copied: {filename}")
        
        # Create analysis runner script
        self._create_analysis_runner()
    
    def _create_analysis_runner(self):
        """Create analysis runner script"""
        runner_content = f'''#!/usr/bin/env python3
"""
Service Architecture Analysis Runner
Auto-generated for project: {self.project_name}
"""

import sys
from pathlib import Path
from service_architecture_analyzer import ServiceArchitectureAnalyzer, ProjectConfig, AnalysisLevel

def main():
    project_name = "{self.project_name}"
    base_directory = "{self.base_directory}"
    
    # Load configuration
    config = ProjectConfig(
        project_name=project_name,
        project_description="Architecture analysis for {{project_name}}",
        base_directory=base_directory
    )
    
    # Initialize analyzer
    analyzer = ServiceArchitectureAnalyzer(config)
    
    # Discover services
    manifest_file = Path(base_directory) / "services_manifest.json"
    services = analyzer.discover_services(str(manifest_file) if manifest_file.exists() else None)
    
    if not services:
        print("❌ No services found. Please check your services_manifest.json file.")
        return
    
    # Run comprehensive analysis
    analyzer.analyze_architecture(AnalysisLevel.COMPREHENSIVE)
    analyzer.print_summary()
    
    # Create visualization
    print("\\n🎨 Creating architecture visualization...")
    analyzer.visualize_architecture(f"{{project_name}}_architecture.png")
    
    # Export analysis
    print("\\n📄 Exporting analysis results...")
    analyzer.export_analysis(f"{{project_name}}_analysis.json")
    
    print(f"\\n✅ Analysis complete! Check the analysis_output directory.")

if __name__ == "__main__":
    main()
'''
        
        runner_file = self.base_directory / "saa_analyze.py"
        with open(runner_file, 'w', encoding='utf-8') as f:
            f.write(runner_content)
        
        # Make executable
        os.chmod(runner_file, 0o755)
        print(f"   🔧 Created: saa_analyze.py")
    
    def _create_example_services(self, services: List[str]):
        """Create example service structures"""
        for service_name in services:
            service_id = service_name.lower().replace(' ', '_').replace('-', '_')
            service_dir = self.base_directory / "services" / service_id
            service_dir.mkdir(parents=True, exist_ok=True)
            
            # Create SRD template
            self._create_srd_template(service_dir, service_name)
            
            # Create ICD template
            self._create_icd_template(service_dir, service_name)
            
            print(f"   📁 Created service structure: {service_id}")
    
    def _create_srd_template(self, service_dir: Path, service_name: str):
        """Create SRD template file"""
        srd_content = f'''# Software Requirements Document (SRD)
## Service: {service_name}

### Version Information
- **Version**: 1.0
- **Date**: {datetime.now().strftime("%Y-%m-%d")}
- **Author**: Auto-generated

### Purpose
Define the requirements and specifications for the {service_name} service.

### Business Requirements
- Requirement 1: [Define business requirement]
- Requirement 2: [Define business requirement]

### Functional Requirements
- FR-001: [Define functional requirement]
- FR-002: [Define functional requirement]

### Non-Functional Requirements
- NFR-001: Performance requirements
- NFR-002: Security requirements
- NFR-003: Scalability requirements

### Dependencies
- Dependency 1: [Service or system dependency]
- Dependency 2: [External dependency]

### Technology Stack
- Programming Language: [e.g., Python, Java, Node.js]
- Framework: [e.g., FastAPI, Spring Boot, Express]
- Database: [e.g., PostgreSQL, MongoDB]
- Message Queue: [e.g., RabbitMQ, Apache Kafka]

### Configuration
- Environment Variables
- Configuration Files
- Service Ports
'''
        
        srd_file = service_dir / f"SRD_{service_name.replace(' ', '_')}.md"
        with open(srd_file, 'w', encoding='utf-8') as f:
            f.write(srd_content)
    
    def _create_icd_template(self, service_dir: Path, service_name: str):
        """Create ICD template file"""
        service_id = service_name.lower().replace(' ', '_').replace('-', '_')
        
        icd_content = f'''# Interface Control Document (ICD)
## Service: {service_name}

### Version Information
- **Version**: 1.0
- **Date**: {datetime.now().strftime("%Y-%m-%d")}
- **Author**: Auto-generated

### Base URL
`http://localhost:8000` (Update with actual service URL)

### API Endpoints

#### Health Check
```http
GET /health
```
Returns the health status of the service.

**Response:**
```json
{{
  "status": "healthy",
  "timestamp": "2025-01-01T00:00:00Z",
  "service": "{service_name}"
}}
```

#### Service Information
```http
GET /info
```
Returns service information and version.

**Response:**
```json
{{
  "service_name": "{service_name}",
  "version": "1.0",
  "description": "Service description"
}}
```

#### Main Service Endpoints
```http
GET /{service_id}
POST /{service_id}
PUT /{service_id}/{{id}}
DELETE /{service_id}/{{id}}
```

### Message Interfaces

#### Published Messages
- `{service_id}.created`: Published when a new {service_id} is created
- `{service_id}.updated`: Published when a {service_id} is updated
- `{service_id}.deleted`: Published when a {service_id} is deleted

#### Subscribed Messages
- `system.heartbeat`: System-wide heartbeat messages
- `user.authenticated`: User authentication events

### Database Interfaces

#### Tables/Collections
- `{service_id}`: Main data entity
- `{service_id}_audit`: Audit trail

### External Dependencies
- Authentication Service: For user validation
- Logging Service: For centralized logging
- Configuration Service: For dynamic configuration

### Error Handling
- Standard HTTP status codes
- Consistent error response format
- Detailed error logging
'''
        
        icd_file = service_dir / f"ICD_{service_name.replace(' ', '_')}.md"
        with open(icd_file, 'w', encoding='utf-8') as f:
            f.write(icd_content)
    
    def _create_readme(self):
        """Create project README"""
        readme_content = f'''# {self.project_name} - Service Architecture Analysis

This project uses the **Service Architecture Analyzer (SAA)** package for analyzing and visualizing service-oriented architectures.

## 📁 Project Structure

```
{self.project_name}/
├── saa_config.json          # Project configuration
├── services_manifest.json   # Service definitions
├── saa_analyze.py          # Analysis runner script
├── base_models.py          # Core data models
├── service_architecture_analyzer.py  # Analysis engine
├── services/               # Service documentation
│   ├── service1/
│   │   ├── SRD_Service1.md
│   │   └── ICD_Service1.md
│   └── ...
├── docs/                   # Additional documentation
├── analysis_output/        # Generated analysis results
└── README.md              # This file
```

## 🚀 Quick Start

1. **Define Your Services**: Edit `services_manifest.json` to list all your services
2. **Document Services**: Create SRD/ICD files for each service in the `services/` directory
3. **Run Analysis**: Execute the analysis script

```bash
python saa_analyze.py
```

## 📊 Analysis Features

- **Service Discovery**: Automatic detection of services and their interfaces
- **Dependency Analysis**: Identify service dependencies and communication patterns
- **Interface Compatibility**: Detect broken or missing interfaces between services
- **Architecture Visualization**: Generate NetworkX-based architecture diagrams
- **Health Assessment**: Calculate architecture health scores and recommendations
- **Export Capabilities**: JSON, GraphML, and visualization exports

## 📖 Service Documentation Format

### SRD (Software Requirements Document)
Document your service requirements in `services/[service_name]/SRD_[ServiceName].md`:

```markdown
# Software Requirements Document (SRD)
## Service: [Service Name]

### Purpose
[Service purpose and description]

### Business Requirements
- Requirement 1
- Requirement 2

### Functional Requirements  
- FR-001: [Functional requirement]

### Dependencies
- [Service dependencies]

### Technology Stack
- [Technologies used]
```

### ICD (Interface Control Document)
Document your service interfaces in `services/[service_name]/ICD_[ServiceName].md`:

```markdown
# Interface Control Document (ICD)
## Service: [Service Name]

### Base URL
`http://localhost:8000`

### API Endpoints
```http
GET /health
GET /api/v1/resource
POST /api/v1/resource
```

### Message Interfaces
- Published: [message types]
- Subscribed: [message types]
```

## 🔧 Configuration

Edit `saa_config.json` to customize analysis settings:

```json
{{
  "project_name": "{self.project_name}",
  "project_description": "Service architecture analysis",
  "base_directory": "{self.base_directory}",
  "services_directory": "services",
  "docs_directory": "docs",
  "output_directory": "analysis_output"
}}
```

## 📈 Analysis Results

The analyzer generates:

1. **Architecture Summary**: Overview of services, interfaces, and dependencies
2. **Compatibility Report**: Interface compatibility analysis
3. **Centrality Analysis**: Service importance and connectivity metrics
4. **Health Score**: Overall architecture health assessment
5. **Recommendations**: Improvement suggestions
6. **Visual Diagram**: NetworkX-based architecture visualization

## 🎯 Analysis Levels

- **Basic**: Service count and basic metrics
- **Detailed**: Include centrality and compatibility analysis
- **Comprehensive**: Full analysis with recommendations and health scoring

## 📄 Output Files

Generated in `analysis_output/`:
- `[project]_analysis.json`: Complete analysis results
- `[project]_architecture.png`: Architecture visualization
- `[project]_services.graphml`: NetworkX graph export

## 🛠️ Advanced Usage

### Command Line Interface

```bash
# Run specific analysis level
python service_architecture_analyzer.py {self.project_name} --level comprehensive

# Create visualization only
python service_architecture_analyzer.py {self.project_name} --visualize

# Export to custom file
python service_architecture_analyzer.py {self.project_name} --export my_analysis.json
```

### Programmatic Usage

```python
from service_architecture_analyzer import ServiceArchitectureAnalyzer, ProjectConfig

config = ProjectConfig(
    project_name="{self.project_name}",
    project_description="My architecture analysis",
    base_directory="{self.base_directory}"
)

analyzer = ServiceArchitectureAnalyzer(config)
services = analyzer.discover_services("services_manifest.json")
results = analyzer.analyze_architecture()
analyzer.visualize_architecture()
```

## 📚 Resources

- [NetworkX Documentation](https://networkx.org/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Service-Oriented Architecture Best Practices](https://martinfowler.com/articles/microservices.html)

## 🤝 Contributing

1. Update service documentation as services evolve
2. Run analysis regularly to monitor architecture health
3. Use recommendations to improve service design
4. Share analysis results with team members

---

Generated by SAA Bootstrap on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
'''
        
        readme_file = self.base_directory / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"   📖 Created: README.md")
    
    def add_service(self, service_name: str, service_type: str = "enhanced") -> str:
        """Add a new service to existing project"""
        if not self.manifest_file.exists():
            raise FileNotFoundError(f"Project not initialized. Run initialize_project() first.")
        
        # Load existing manifest
        with open(self.manifest_file, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # Create service entry
        entry = self._create_service_entry(service_name)
        entry["service_type"] = service_type
        
        # Add to manifest
        manifest["services"].append(entry)
        
        # Save updated manifest
        with open(self.manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        # Create service structure
        self._create_example_services([service_name])
        
        print(f"✅ Added service: {service_name}")
        return entry["service_directory"]


def main():
    """CLI for SAA Project Bootstrap"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Service Architecture Analyzer - Project Bootstrap")
    parser.add_argument("project_name", help="Name of the project to create/manage")
    parser.add_argument("--base-dir", default=".", help="Base directory for the project")
    parser.add_argument("--init", action="store_true", help="Initialize new project")
    parser.add_argument("--services", nargs="*", help="List of services to create")
    parser.add_argument("--add-service", help="Add a new service to existing project")
    parser.add_argument("--service-type", default="enhanced", 
                       choices=["gateway", "core", "infrastructure", "enhanced"],
                       help="Type of service to add")
    
    args = parser.parse_args()
    
    bootstrap = SAA_ProjectBootstrap(args.project_name, args.base_dir)
    
    if args.init:
        bootstrap.initialize_project(args.services or [])
    elif args.add_service:
        bootstrap.add_service(args.add_service, args.service_type)
    else:
        print("❌ Please specify --init to create new project or --add-service to add service")
        print("Example: python saa_bootstrap.py MyProject --init --services 'API Gateway' 'User Service' 'Data Service'")


if __name__ == "__main__":
    main()