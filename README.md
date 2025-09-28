# Service Architecture Analyzer (SAA)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![NetworkX](https://img.shields.io/badge/powered%20by-NetworkX-orange.svg)](https://networkx.org/)
[![Pydantic](https://img.shields.io/badge/validated%20with-Pydantic-green.svg)](https://pydantic-docs.helpmanual.io/)

A comprehensive Python systems engineering package for analyzing, visualizing, and optimizing service-oriented architectures using NetworkX graph analysis.

## 🎯 What is SAA?

**Service Architecture Analyzer (SAA)** transforms static service documentation into living, analyzable systems. It automatically discovers services, maps interfaces, identifies compatibility issues, and generates comprehensive architecture insights through NetworkX-powered graph analysis.

### Key Capabilities
- 🔍 **Service Discovery**: Auto-detect services from directories or manifest files
- 🕸️ **Dependency Mapping**: Build NetworkX graphs of service relationships
- 🔗 **Interface Analysis**: Identify broken connections and compatibility issues
- 📊 **Health Assessment**: Calculate architecture health scores and metrics
- 🎨 **Visualization**: Generate clear architecture diagrams
- 📄 **Multi-format Export**: JSON, GraphML, CSV, and PNG outputs

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/sligara7/saa.git
cd saa

# Install dependencies
pip install -r requirements.txt
```

### Create Your First Analysis

```bash
# Initialize a new project
python -c "
from bootstrap import SAA_ProjectBootstrap
bootstrap = SAA_ProjectBootstrap('MyProject', '.')
bootstrap.initialize_project(['API Gateway', 'User Service', 'Data Service'])
"

# Run analysis
python -c "
from analyzer import ServiceArchitectureAnalyzer, ProjectConfig, AnalysisLevel
config = ProjectConfig('MyProject', 'My first analysis', '.')
analyzer = ServiceArchitectureAnalyzer(config)
analyzer.discover_services('services_manifest.json')
analyzer.analyze_architecture(AnalysisLevel.COMPREHENSIVE)
analyzer.print_summary()
analyzer.visualize_architecture('architecture.png')
"
```

## 📦 Package Structure

```
saa/
├── __init__.py              # Main package interface
├── base_models.py           # Pydantic data models
├── analyzer.py              # Core analysis engine  
├── bootstrap.py             # Project creation tools
├── requirements.txt         # Dependencies
├── examples/                # Working examples
│   ├── ecommerce_example.py
│   └── banking_example.py
└── README.md               # This file
```

## 🛠️ Usage Examples

### 1. E-commerce Platform Analysis

```python
from bootstrap import SAA_ProjectBootstrap
from analyzer import ServiceArchitectureAnalyzer, ProjectConfig, AnalysisLevel

# Define services
services = [
    "API Gateway", "User Service", "Product Catalog Service",
    "Order Service", "Payment Service", "Inventory Service",
    "Notification Service", "Auth Service", "Shopping Cart Service"
]

# Create project
bootstrap = SAA_ProjectBootstrap("ECommerce_Platform", "./ecommerce")
bootstrap.initialize_project(services)

# Analyze
config = ProjectConfig("ECommerce_Platform", "E-commerce analysis", "./ecommerce")
analyzer = ServiceArchitectureAnalyzer(config)
analyzer.discover_services()
analyzer.analyze_architecture(AnalysisLevel.COMPREHENSIVE)
analyzer.print_summary()
analyzer.visualize_architecture("ecommerce_architecture.png")
```

### 2. Banking System Analysis

```python
# Banking services
banking_services = [
    "API Gateway", "Customer Service", "Account Service",
    "Transaction Service", "Payment Processing Service",
    "Fraud Detection Service", "Audit Service", "Auth Service"
]

# Create and analyze
bootstrap = SAA_ProjectBootstrap("Banking_System", "./banking")
bootstrap.initialize_project(banking_services)

config = ProjectConfig("Banking_System", "Banking analysis", "./banking")
analyzer = ServiceArchitectureAnalyzer(config)
analyzer.discover_services()
results = analyzer.analyze_architecture(AnalysisLevel.COMPREHENSIVE)
analyzer.visualize_architecture("banking_architecture.png", layout='hierarchical')
```

### 3. Adding Services Dynamically

```python
# Add new service to existing project
bootstrap = SAA_ProjectBootstrap("MyProject", "./my_analysis")
bootstrap.add_service("Notification Service", "infrastructure")

# Re-analyze with new service
analyzer = ServiceArchitectureAnalyzer(config) 
analyzer.discover_services()
analyzer.analyze_architecture()
```

## 📊 Analysis Output Example

When you run SAA analysis, you get comprehensive insights:

```
🏗️  ARCHITECTURE ANALYSIS SUMMARY
============================================================
📊 Project: ECommerce_Platform
📁 Location: ./ecommerce

📈 OVERVIEW:
   Services: 9
   Interfaces: 81
   Dependencies: 9

🏷️  SERVICE TYPES:
   Enhanced: 7
   Infrastructure: 1
   Gateway: 1

🔗 COMPATIBILITY:
   Compatible: 41
   Broken: 40
   Ratio: 50.62%

💡 RECOMMENDATIONS:
   🔵 Highly Connected Services
      Consider breaking down highly coupled services
```

## 🎨 Visualization Features

SAA generates NetworkX-powered visualizations with:

- **Service Type Coloring**: Different colors for Gateway, Core, Infrastructure, Enhanced services
- **Multiple Layouts**: Spring, hierarchical, circular layouts
- **Interactive Elements**: Hover information and service details
- **Export Formats**: PNG, SVG, PDF support

### Layout Options

```python
# Different visualization layouts
analyzer.visualize_architecture("spring_layout.png", layout='spring')
analyzer.visualize_architecture("hierarchical.png", layout='hierarchical') 
analyzer.visualize_architecture("circular.png", layout='circular')
```

## 📄 Service Documentation Format

SAA works with markdown-based service documentation:

### Software Requirements Document (SRD)
```markdown
# Software Requirements Document (SRD)
## Service: User Service

### Purpose
Manages user accounts, authentication, and profile data

### Business Requirements
- User registration and login
- Profile management
- Role-based access control

### Functional Requirements
- FR-001: User can create account with email/password
- FR-002: User can update profile information
- FR-003: System validates user credentials

### Dependencies
- Auth Service: For authentication tokens
- Database Service: For user data storage

### Technology Stack
- Python FastAPI
- PostgreSQL database
- Redis caching
```

### Interface Control Document (ICD)
```markdown
# Interface Control Document (ICD)
## Service: User Service

### Base URL
`http://localhost:8001`

### API Endpoints
```http
GET /health
GET /api/v1/users/{id}
POST /api/v1/users
PUT /api/v1/users/{id}
DELETE /api/v1/users/{id}
```

### Message Interfaces
- Published: `user.created`, `user.updated`, `user.deleted`
- Subscribed: `auth.token.validated`
```

## 🔧 Configuration

### Project Configuration (saa_config.json)
```json
{
  "project_name": "MyProject",
  "project_description": "My service architecture analysis",
  "base_directory": ".",
  "services_directory": "services",
  "docs_directory": "docs",
  "output_directory": "analysis_output"
}
```

### Service Manifest (services_manifest.json)
```json
{
  "format_version": "1.0",
  "project_name": "MyProject",
  "services": [
    {
      "service_name": "API Gateway",
      "service_directory": "./services/api_gateway",
      "service_type": "gateway",
      "SRD_version": "1.0",
      "ICD_version": "1.0"
    }
  ]
}
```

## 📈 Analysis Levels

SAA supports three analysis depths:

### Basic Analysis
- Service count and basic metrics
- Interface type distribution  
- Simple dependency mapping

### Detailed Analysis (Default)
- All basic analysis features
- NetworkX centrality metrics
- Interface compatibility checking
- Critical path identification

### Comprehensive Analysis
- All detailed analysis features
- Architecture health scoring
- Improvement recommendations
- Performance bottleneck identification

```python
# Choose analysis level
analyzer.analyze_architecture(AnalysisLevel.BASIC)
analyzer.analyze_architecture(AnalysisLevel.DETAILED)
analyzer.analyze_architecture(AnalysisLevel.COMPREHENSIVE)
```

## 🔍 Advanced Features

### NetworkX Integration

SAA leverages NetworkX for powerful graph analysis:

```python
# Access the NetworkX graph directly
graph = analyzer.build_dependency_graph()

# Custom NetworkX analysis
import networkx as nx
centrality = nx.degree_centrality(graph)
communities = nx.community.greedy_modularity_communities(graph)
```

### Custom Service Types

```python
from base_models import ServiceType

# Define custom service types
class CustomServiceType(ServiceType):
    ANALYTICS = "analytics"
    MONITORING = "monitoring"
```

### Export Capabilities

```python
# Multiple export formats
analyzer.export_analysis("results.json")           # JSON analysis
graph = analyzer.build_dependency_graph()
nx.write_graphml(graph, "architecture.graphml")    # GraphML for Gephi/Cytoscape
analyzer.visualize_architecture("diagram.png")     # PNG visualization
```

## 🎯 Use Cases

### Enterprise Architecture Review
- Microservices dependency analysis
- Legacy system modernization planning
- Service mesh architecture validation
- Cross-team interface coordination

### Development Process Integration  
- CI/CD pipeline architecture validation
- Interface compatibility checking in builds
- Automated architecture documentation
- Service integration testing

### Systems Engineering
- New service-oriented system design
- Architecture health monitoring over time
- Capacity planning and scaling decisions
- Security boundary analysis

## 🤝 Contributing

We welcome contributions! Areas where you can help:

1. **New Analysis Algorithms**: Implement additional NetworkX-based metrics
2. **Visualization Enhancements**: Improve diagram generation and layouts
3. **Export Formats**: Add support for additional output formats
4. **Integration**: Build integrations with architecture tools
5. **Documentation**: Improve examples and tutorials

### Development Setup

```bash
# Clone repository
git clone https://github.com/sligara7/saa.git
cd saa

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest

# Format code
black .
```

## 📚 Examples

Check the `examples/` directory for complete working examples:

- **E-commerce Platform**: 9-service online store architecture
- **Banking System**: 8-service financial system architecture

Run examples:
```bash
python examples/ecommerce_example.py
python examples/banking_example.py
```

## 🐛 Troubleshooting

### Common Issues

**ImportError: No module named 'networkx'**
```bash
pip install networkx matplotlib pydantic psutil
```

**No services found**
- Ensure services_manifest.json exists and is properly formatted
- Check that service directories contain SRD/ICD markdown files
- Verify service directory structure

**Visualization not displaying**
- Install matplotlib with GUI backend: `pip install matplotlib[gui]`
- For headless systems, use: `analyzer.visualize_architecture("output.png")`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋 Support

- **Issues**: [GitHub Issues](https://github.com/sligara7/saa/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sligara7/saa/discussions)
- **Documentation**: This README and inline code documentation

## 🔮 Roadmap

- [ ] **LLM Integration**: Auto-generate SRD/ICD from code
- [ ] **Real-time Monitoring**: Live architecture health dashboards  
- [ ] **Cloud Integration**: AWS/Azure/GCP service discovery
- [ ] **Performance Metrics**: Response time and throughput analysis
- [ ] **Security Analysis**: Interface security assessment
- [ ] **Web Interface**: Browser-based analysis dashboard

---

**Service Architecture Analyzer (SAA)** - Transforming complex service architectures into manageable, analyzable systems through automated discovery, validation, and NetworkX-powered visualization.

🌟 **Star this repository** if SAA helps you understand and improve your service architectures!