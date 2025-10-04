#!/usr/bin/env python3
"""
Template generator for creating standardized architecture files
"""
import json
import os
from datetime import datetime
from pathlib import Path

def load_template(template_name):
    """Load a template file"""
    template_path = Path(__file__).parent / "templates" / template_name
    with open(template_path, 'r') as f:
        template = json.load(f)
    # Remove instruction fields
    if "INSTRUCTIONS" in template:
        del template["INSTRUCTIONS"]
    return template

def generate_service_architecture(
    service_name: str,
    service_id: str,
    purpose: str,
    hierarchical_tier: str = "tier_2_components",
    component_classification: str = "service",
    dependencies: list = None,
    interfaces: list = None,
    is_external: bool = False,
    parent_system: str = None,
    **kwargs
):
    """Generate a service_architecture.json file from template"""
    
    template = load_template("service_architecture_template.json")
    
    # Fill in required fields
    template["service_name"] = service_name
    template["service_id"] = service_id
    template["purpose"] = purpose
    template["hierarchical_tier"] = hierarchical_tier
    template["component_classification"] = component_classification
    template["dependencies"] = dependencies or []
    template["interfaces"] = interfaces or []
    template["is_external"] = is_external
    template["parent_system"] = parent_system
    template["version"] = f"1.0+{datetime.now().strftime('%Y-%m-%d')}"
    
    # Add any additional fields
    for key, value in kwargs.items():
        if key not in template:
            template[key] = value
    
    return template

def generate_index(
    system_name: str,
    description: str,
    components: dict,
    **kwargs
):
    """Generate an index.json file from template"""
    
    template = load_template("index_template.json")
    
    # Fill in required fields
    template["system_name"] = system_name
    template["description"] = description
    template["last_updated"] = datetime.now().strftime('%Y-%m-%d')
    template["components"] = components
    
    # Update metadata
    if "metadata" not in template:
        template["metadata"] = {}
    template["metadata"]["total_components"] = len(components)
    template["metadata"]["generated_by"] = "Template Generator Script"
    
    # Add any additional fields
    for key, value in kwargs.items():
        if key not in template:
            template[key] = value
    
    # Remove template fields
    if "INSTRUCTIONS" in template:
        del template["INSTRUCTIONS"]
    
    return template

def save_json(data, file_path):
    """Save data as pretty-printed JSON"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Generated: {file_path}")

# Example usage
if __name__ == "__main__":
    # Example: Generate a simple service architecture
    service_arch = generate_service_architecture(
        service_name="Example Service",
        service_id="example_service",
        purpose="Example service for demonstration",
        dependencies=["other_service"],
        interfaces=[
            {
                "name": "Example API",
                "interface_type": "http_endpoint",
                "communication_pattern": "synchronous",
                "dependency_type": "direct",
                "description": "Example HTTP API endpoint",
                "path": "/api/example",
                "method": "GET",
                "auth_required": False,
                "version": "1.0"
            }
        ]
    )
    
    # Example: Generate an index
    index = generate_index(
        system_name="Example System",
        description="Example system for demonstration",
        components={
            "example_service": "systems/example_system/example_service/service_architecture.json"
        }
    )
    
    print("Example service architecture:")
    print(json.dumps(service_arch, indent=2))
    print("\nExample index:")
    print(json.dumps(index, indent=2))