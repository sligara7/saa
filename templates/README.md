# Architecture Templates and Standards

This directory contains standardized templates and schemas for generating consistent architecture files in the LLM-driven system analysis process.

## Files Overview

### Templates
- **`index_template.json`** - Template for creating system index files
- **`service_architecture_template.json`** - Template for individual service architecture files

### Schemas  
- **`index_schema.json`** - JSON Schema for validating index.json files
- **`service_architecture_schema.json`** - JSON Schema for validating service_architecture.json files

## Usage Instructions

### For LLM Agents

When generating architecture files, **ALWAYS** use these templates as the authoritative format specification:

1. **Copy the template structure exactly**
2. **Replace all REPLACE_WITH_* placeholders** with actual values
3. **Use only the enum values specified** in the templates and schemas
4. **Follow the validation rules** listed in the INSTRUCTIONS sections

### Index.json Format

```json
{
  "system_name": "Your System Name",
  "description": "System description", 
  "last_updated": "2025-09-30",
  "components": {
    "component_id": "systems/system_name/component_id/service_architecture.json"
  }
}
```

**Key Rules:**
- Use relative paths from repository root
- Component IDs must be lowercase with underscores
- Paths must follow pattern: `systems/SYSTEM_NAME/COMPONENT_ID/service_architecture.json`

### Service Architecture Format

```json
{
  "service_name": "Human Readable Name",
  "service_id": "lowercase_with_underscores", 
  "hierarchical_tier": "tier_2_components",
  "component_classification": "service",
  "purpose": "Clear purpose description",
  "dependencies": ["other_service_id"],
  "interfaces": [
    {
      "name": "Interface Name",
      "interface_type": "http_endpoint",
      "communication_pattern": "synchronous", 
      "dependency_type": "direct",
      "description": "Interface description"
    }
  ],
  "is_external": false,
  "version": "1.0+2025-09-30"
}
```

**Key Rules:**
- All enum fields must use exact values from UAF definitions
- Version must follow semver-date format: `X.Y+YYYY-MM-DD`
- Dependencies must reference valid service_ids
- External systems must set `is_external: true`

## UAF Hierarchical Tiers

- **`tier_0_system_of_systems`** - Highest level federation (enterprise)
- **`tier_1_systems`** - Independent systems that can operate standalone  
- **`tier_2_components`** - Individual services/components within systems

## Component Classifications

- **`service`** - Black-box functionality exposed to external consumers
- **`function`** - Internal behavior within a service
- **`external`** - External/non-modifiable systems (IOCs, databases)
- **`interface_protocol`** - Data transport mechanisms (EPICS/CA, protocols)

## Communication Patterns

- **`synchronous`** - Request-response, caller waits for response
- **`asynchronous`** - Fire-and-forget, pub-sub, event-driven
- **`bidirectional`** - Two-way communication, both parties can initiate

## Dependency Types

- **`direct`** - Component directly communicates with another
- **`indirect`** - Communication through intermediary service
- **`external`** - Dependency on service outside current system boundary

## Validation

Use the provided JSON schemas to validate generated files:

```bash
# Install a JSON schema validator like ajv-cli
npm install -g ajv-cli

# Validate files
ajv validate -s templates/index_schema.json -d systems/*/index.json
ajv validate -s templates/service_architecture_schema.json -d "systems/*/*/service_architecture.json"
```

## Integration with system_of_systems_graph.py

The visualization script expects these exact formats:

1. **Index structure**: Must have `components` key with component_id → file_path mapping
2. **Service structure**: Must have UAF fields (`hierarchical_tier`, `component_classification`)
3. **Path format**: Relative paths from repository root
4. **Dependency format**: Array of service_ids that match other components

By following these templates, the visualization script will work without modification across different systems.

## Error Prevention

Common issues prevented by using these templates:

- ❌ Inconsistent field names (service_name vs serviceName)
- ❌ Invalid enum values (synchronous vs sync)  
- ❌ Wrong path formats (absolute vs relative)
- ❌ Missing required fields
- ❌ Invalid JSON structure
- ❌ Inconsistent component_id formats
- ❌ Circular dependencies
- ❌ References to non-existent components

## Future Extensions

When extending the templates:

1. Update both template and schema files
2. Add new enum values to UAF definitions
3. Update validation rules in INSTRUCTIONS
4. Test with system_of_systems_graph.py
5. Document changes in this README

This ensures the LLM-driven process remains robust and the visualization tools continue working without code changes.