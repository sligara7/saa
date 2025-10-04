#!/usr/bin/env python3
"""
Simple validation script to check if generated files conform to templates
"""
import json
import os
import sys
from pathlib import Path

def validate_service_architecture(file_path):
    """Validate a service_architecture.json file against template requirements"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        return False, f"JSON parse error: {e}"
    
    # Required fields from template
    required_fields = [
        "service_name", "service_id", "hierarchical_tier", 
        "component_classification", "purpose", "dependencies", 
        "interfaces", "is_external", "version"
    ]
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {missing_fields}"
    
    # Validate enum values
    valid_tiers = ["tier_0_system_of_systems", "tier_1_systems", "tier_2_components"]
    if data.get("hierarchical_tier") not in valid_tiers:
        return False, f"Invalid hierarchical_tier: {data.get('hierarchical_tier')}"
    
    valid_classifications = ["service", "function", "external", "interface_protocol"]
    if data.get("component_classification") not in valid_classifications:
        return False, f"Invalid component_classification: {data.get('component_classification')}"
    
    # Validate version format (X.Y+YYYY-MM-DD)
    version = data.get("version", "")
    import re
    if not re.match(r'^\d+\.\d+(\+\d{4}-\d{2}-\d{2})?$', version):
        return False, f"Invalid version format: {version} (should be X.Y+YYYY-MM-DD)"
    
    # Validate service_id format (lowercase with underscores)
    service_id = data.get("service_id", "")
    if not re.match(r'^[a-z][a-z0-9_]*$', service_id):
        return False, f"Invalid service_id format: {service_id} (should be lowercase with underscores)"
    
    return True, "Valid"

def validate_index(file_path):
    """Validate an index.json file against template requirements"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        return False, f"JSON parse error: {e}"
    
    # Required fields
    required_fields = ["system_name", "description", "last_updated", "components"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {missing_fields}"
    
    # Validate date format
    import re
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', data.get("last_updated", "")):
        return False, f"Invalid date format: {data.get('last_updated')} (should be YYYY-MM-DD)"
    
    # Validate components structure
    if not isinstance(data.get("components"), dict):
        return False, "Components must be a dictionary"
    
    return True, "Valid"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_templates.py <path_to_system_directory>")
        sys.exit(1)
    
    system_dir = Path(sys.argv[1])
    
    # Validate index.json
    index_path = system_dir / "index.json"
    if index_path.exists():
        valid, msg = validate_index(index_path)
        print(f"Index: {'✓' if valid else '✗'} {msg}")
    else:
        print("Index: ✗ index.json not found")
    
    # Validate all service_architecture.json files
    service_files = list(system_dir.glob("*/service_architecture.json"))
    print(f"\nFound {len(service_files)} service architecture files:")
    
    for service_file in service_files:
        valid, msg = validate_service_architecture(service_file)
        print(f"{service_file.parent.name}: {'✓' if valid else '✗'} {msg}")