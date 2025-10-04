import subprocess
def run_validation(system_name):
    base = Path(__file__).parent
    validate_script = base / 'validate_templates.py'
    target_dir = base / f'systems/{system_name}'
    print(f'Running template validation for {target_dir}...')
    result = subprocess.run(['python3', str(validate_script), str(target_dir)], capture_output=True, text=True)
    print('Validation output:')
    print(result.stdout)
    if result.returncode != 0:
        print('Validation errors:')
        print(result.stderr)
    else:
        print('All files passed template validation.')

def run_visualization(system_name):
    base = Path(__file__).parent
    graph_script = base / 'system_of_systems_graph.py'
    index_file = base / f'systems/{system_name}/index.json'
    print(f'Generating system graph visualization for {index_file}...')
    result = subprocess.run(['python3', str(graph_script), str(index_file)], capture_output=True, text=True)
    print('Visualization output:')
    print(result.stdout)
    if result.returncode != 0:
        print('Visualization errors:')
        print(result.stderr)
    else:
        print('System graph visualization generated.')
# Utility to safely create directories
def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

# Generate service_architecture.json for each component

def generate_service_architecture_files(decomposed, templates, system_name):
    base = Path(__file__).parent
    output_paths = []
    for svc in decomposed:
        svc_dir = base / f'systems/{system_name}/{svc["service_name"].replace(" ", "_")}'
        ensure_dir(svc_dir)
        for comp in svc['components']:
            comp_dir = svc_dir / comp['name'].replace(' ', '_').replace('/', '_')
            ensure_dir(comp_dir)
            arch_file = comp_dir / 'service_architecture.json'
            data = templates['service'].copy()
            # Fill fields with actual data
            data['service_name'] = comp['name']
            data['service_id'] = f"{svc['service_name'].replace(' ', '_')}_{comp['name'].replace(' ', '_').replace('/', '_')}"
            data['hierarchical_tier'] = 'component'
            data['component_classification'] = svc['service_name']
            # Description: combine service purpose and subcomponents
            sub_desc = f"Subcomponents: {', '.join(comp['subcomponents'])}" if comp['subcomponents'] else ""
            data['description'] = f"{svc['purpose']} {sub_desc}".strip()
            data['implementation_status'] = 'existing'
            data['verification_notes'] = f"Generated from markdown system description."
            data['justification'] = f"Component extracted from '{svc['service_name']}' in system markdown."
            data['source_references'] = []
            data['version'] = '1.0'
            with open(arch_file, 'w') as f:
                json.dump(data, f, indent=2)
            output_paths.append(str(arch_file))
    return output_paths

# Generate index.json mapping components to file paths
def generate_index_file(decomposed, system_name):
    base = Path(__file__).parent
    index = {}
    for svc in decomposed:
        for comp in svc['components']:
            comp_path = f'systems/{system_name}/{svc["service_name"].replace(" ", "_")}/{comp["name"].replace(" ", "_").replace("/", "_")}/service_architecture.json'
            index[comp['name']] = comp_path
    index_file = base / f'systems/{system_name}/index.json'
    ensure_dir(index_file.parent)
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)
    return str(index_file)
"""
Automation script for LLM-Driven System-of-Systems Architecture Analysis
Follows the process defined in llm_execution_process.json
"""
import os
import json
from pathlib import Path

# Step 1: Initialize Analysis Context
def load_definitions_and_templates():
    base = Path(__file__).parent
    definitions_path = base / 'definitions/architectural_definitions.json'
    templates = {
        'index': base / 'templates/index_template.json',
        'service': base / 'templates/service_architecture_template.json',
        'internal_module': base / 'templates/internal_module_template.json'
    }
    with open(definitions_path) as f:
        definitions = json.load(f)
    templates_data = {}
    for key, path in templates.items():
        with open(path) as f:
            templates_data[key] = json.load(f)
    return definitions, templates_data

# Step 2: Parse Input System Description (Markdown)

import re


def parse_system_description(md_path):
    with open(md_path) as f:
        content = f.read()
    # Extract service sections
    service_pattern = r"### Service (\d+): ([^\n]+)\n\*\*Purpose:\*\*\s*([^\n]+)"  # Service number, name, purpose
    services = []
    for match in re.finditer(service_pattern, content):
        service_num = match.group(1)
        service_name = match.group(2).strip()
        service_purpose = match.group(3).strip()
        # Find deployed components for this service
        deployed_match = re.search(rf"### Service {service_num}:.*?\*\*Deployed Components:\*\*\n(- [^\n]+(?:\n- [^\n]+)*)", content, re.DOTALL)
        if deployed_match:
            components = [c.strip('- ').strip() for c in deployed_match.group(1).split('\n')]
        else:
            components = []
        # Find internal/external interfaces
        interface_match = re.search(rf"### Service {service_num}:.*?\*\*Interfaces:\*\*\n- \*\*External:\*\*\s*([^\n]+)(.*?)\*\*Internal:\*\*\s*([^\n]+)(.*?)\n\*\*Security:\*\*", content, re.DOTALL)
        if interface_match:
            external = interface_match.group(1).strip()
            internal = interface_match.group(3).strip()
        else:
            # Try to find communication flow
            comm_match = re.search(rf"### Service {service_num}:.*?\*\*Communication Flow:\*\*\n```([\s\S]+?)```", content)
            external = comm_match.group(1).strip() if comm_match else ''
            internal = ''
        services.append({
            'service_num': service_num,
            'service_name': service_name,
            'purpose': service_purpose,
            'components': components,
            'external_interfaces': external,
            'internal_interfaces': internal
        })
    # Coordination Service (special case)
    coord_match = re.search(r"### Service 3: Coordination Service.*?\*\*Purpose:\*\* ([^\n]+)", content, re.DOTALL)
    if coord_match:
        # Find communication flow for coordination service
        comm_match = re.search(r"### Service 3: Coordination Service.*?\*\*Communication Flow:\*\*\n```([\s\S]+?)```", content)
        external = comm_match.group(1).strip() if comm_match else ''
        services.append({
            'service_num': '3',
            'service_name': 'Coordination Service',
            'purpose': coord_match.group(1).strip(),
            'components': [],
            'external_interfaces': external,
            'internal_interfaces': ''
        })
    return services

# Decompose components further (stub for now, can be expanded)
def decompose_components(services):
    decomposed = []
    for svc in services:
        svc_entry = {
            'service_num': svc['service_num'],
            'service_name': svc['service_name'],
            'purpose': svc['purpose'],
            'components': []
        }
        for comp in svc['components']:
            # Example: subcomponent extraction (could be expanded with more parsing)
            subcomponents = []
            if 'nginx' in comp:
                subcomponents = ['HTTPS termination', 'API routing', 'Load balancing']
            elif 'redis' in comp:
                subcomponents = ['Queue state storage', 'Plan metadata', 'Inter-process comm']
            elif 'bluesky-queueserver' in comp:
                subcomponents = ['Queue management', 'Plan execution']
            elif 'bluesky-httpserver' in comp:
                subcomponents = ['Web interface', 'API gateway']
            elif 'ophyd-websocket' in comp:
                subcomponents = ['WebSocket server', 'Device monitoring', 'Control']
            svc_entry['components'].append({
                'name': comp,
                'subcomponents': subcomponents
            })
        decomposed.append(svc_entry)
    return decomposed

# Map interfaces between services/components
def map_interfaces(services):
    interface_map = []
    for svc in services:
        interface_map.append({
            'service_name': svc['service_name'],
            'external_interfaces': svc['external_interfaces'],
            'internal_interfaces': svc['internal_interfaces']
        })
    return interface_map

# Main entry point




def main():
    system_md = 'systems/QSaaS_to_OaaS/bluesky_data_acq_system.md'
    system_name = 'QSaaS_to_OaaS'
    print('Initializing context...')
    definitions, templates = load_definitions_and_templates()
    print('Parsing system description and extracting hierarchy...')
    services = parse_system_description(system_md)
    print('\nDecomposed hierarchy:')
    decomposed = decompose_components(services)
    for svc in decomposed:
        print(f"Service {svc['service_num']}: {svc['service_name']}")
        for comp in svc['components']:
            print(f"  Component: {comp['name']}")
            for sub in comp['subcomponents']:
                print(f"    Subcomponent: {sub}")
    print('\nGenerating service_architecture.json files...')
    arch_paths = generate_service_architecture_files(decomposed, templates, system_name)
    print(f'Generated {len(arch_paths)} service_architecture.json files.')
    print('\nGenerating index.json...')
    index_path = generate_index_file(decomposed, system_name)
    print(f'Index file created at: {index_path}')

    print('\nRunning validation...')
    run_validation(system_name)

    print('\nRunning visualization...')
    run_visualization(system_name)

if __name__ == '__main__':
    main()
