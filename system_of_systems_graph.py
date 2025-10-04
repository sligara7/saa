
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
import sys
import argparse
from typing import Dict, List, Tuple

# --- STEP 1: Load the robust index file ---
def load_service_architecture_index(index_path: str) -> Dict[str, str]:
    """Load the mapping of service_id to file path from the index file.
    
    Handles both flat dictionaries and structured index files with 'components' key.
    Returns a flat mapping of service_id to file_path.
    """
    with open(index_path, 'r') as f:
        index_data = json.load(f)
    
    # Handle structured index format with metadata and components
    if isinstance(index_data, dict) and 'components' in index_data:
        return index_data['components']
    
    # Handle legacy flat format (service_id: file_path mapping)
    elif isinstance(index_data, dict):
        # Filter out non-component metadata keys
        metadata_keys = {'system_name', 'description', 'last_updated', 'version', 'metadata'}
        return {k: v for k, v in index_data.items() if k not in metadata_keys and isinstance(v, str)}
    
    else:
        raise ValueError(f"Invalid index format: expected dict with 'components' key or flat service mapping")

# --- STEP 2: Build the system-of-systems graph ---
def classify_node(service_id: str, data: dict) -> Tuple[str, str]:
    """Return (level, display_name) based on UAF hierarchical classification and service data."""
    
    # Use UAF hierarchical_tier if available
    tier = data.get('hierarchical_tier')
    if tier == 'tier_0_system_of_systems':
        level = 'system_of_systems'
    elif tier == 'tier_1_systems':
        level = 'system'
    elif tier == 'tier_2_components':
        level = 'package'  # Map to existing 'package' level for compatibility
    elif tier == 'tier_3_internal_modules':
        level = 'module'  # New level for internal modules
    else:
        # Fallback heuristics for non-UAF formatted data
        if service_id.endswith('_service') and 'package_name' not in data:
            level = 'service'
        elif 'package_name' in data:
            level = 'package'
        else:
            level = 'package'  # Default to package level
    
    # Get display name, preferring service_name
    display_name = (
        data.get('service_name') or 
        data.get('package_name') or 
        service_id.replace('_', '-')  # Convert underscores to hyphens for display
    )
    
    return (level, display_name)

def build_system_graph(index: Dict[str, str], include_levels: List[str]) -> nx.DiGraph:
    """Build a directed graph from all service_architecture.json files filtering by include_levels (e.g., ['package'])."""
    G = nx.DiGraph()
    service_info = {}
    node_levels = {}
    
    # Pass 1: load and classify
    for service_id, file_path in index.items():
        # Handle relative paths by making them relative to current working directory
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.getcwd(), file_path)
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Could not find file {file_path} for service {service_id}")
            continue
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {file_path} for service {service_id}")
            continue
            
        level, display = classify_node(service_id, data)
        node_levels[service_id] = level
        if level in include_levels:
            G.add_node(service_id, label=display, level=level, raw=data)
        service_info[service_id] = data
    # Pass 2: add edges only if both endpoints are kept (to avoid partial hierarchy clutter)
    for service_id, data in service_info.items():
        if service_id not in G:  # Skip nodes filtered out
            continue
        # Dependencies
        dependencies = []
        if 'dependencies' in data:
            dependencies = data['dependencies']
        elif 'srd' in data and 'dependencies' in data['srd']:
            dependencies = data['srd']['dependencies']
        for dep in dependencies:
            dep_id = None
            for sid, info in service_info.items():
                name_candidates = [sid,
                                   info.get('service_name', '').lower().replace(' ', '_'),
                                   info.get('package_name', '').lower().replace(' ', '_')]
                if dep.lower().replace(' ', '_') in name_candidates:
                    dep_id = sid
                    break
            if dep_id and dep_id in G:
                G.add_edge(service_id, dep_id, type='dependency')
        # Interfaces
        icd = data.get('icd', data)
        interfaces = icd.get('interfaces', [])
        for iface in interfaces:
            if isinstance(iface, dict):
                for dep in iface.get('dependencies', []):
                    dep_id = None
                    for sid, info in service_info.items():
                        name_candidates = [sid,
                                           info.get('service_name', '').lower().replace(' ', '_'),
                                           info.get('package_name', '').lower().replace(' ', '_')]
                        if dep.lower().replace(' ', '_') in name_candidates:
                            dep_id = sid
                            break
                    if dep_id and dep_id in G:
                        G.add_edge(service_id, dep_id, type='interface')
    return G

# --- STEP 3: Visualize the graph ---
def visualize_graph(G: nx.DiGraph, out_file: str = None, title: str = 'System Architecture', layout: str = 'spectral'):
    plt.figure(figsize=(14, 9))
    
    # Choose layout algorithm
    if layout == 'spectral':
        pos = nx.spectral_layout(G)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    elif layout == 'shell':
        # Group nodes by level for shell layout
        levels = {}
        for n in G.nodes:
            level = G.nodes[n].get('level', 'unknown')
            if level not in levels:
                levels[level] = []
            levels[level].append(n)
        shells = list(levels.values())
        pos = nx.shell_layout(G, nlist=shells)
    elif layout == 'kamada':
        pos = nx.kamada_kawai_layout(G)
    elif layout == 'hierarchical':
        # Try to create a hierarchical layout based on dependencies
        try:
            import pygraphviz
            pos = nx.graphviz_layout(G, prog='dot')
        except:
            # Fallback to spring layout if graphviz not available
            pos = nx.spring_layout(G, seed=42, k=1.0, iterations=50)
    else:  # spring (default fallback)
        pos = nx.spring_layout(G, seed=42, k=1.0, iterations=50)
    labels = nx.get_node_attributes(G, 'label')
    color_map = []
    for n in G.nodes:
        node_data = G.nodes[n].get('raw', {})
        level = G.nodes[n].get('level', 'unknown')
        implementation_status = node_data.get('implementation_status', 'existing')
        
        # Choose base color by level, then modify for implementation status
        if level == 'package':
            base_color = '#8ecae6'  # Light blue
        elif level == 'service':
            base_color = '#ffb703'  # Orange
        elif level == 'module':
            base_color = '#fb8500'  # Dark orange for internal modules
        elif level == 'system':
            base_color = '#219ebc'  # Blue for systems
        else:
            base_color = '#adb5bd'  # Gray
        
        # Modify color based on implementation status
        if implementation_status == 'existing':
            # Use green tint for existing (verified) components
            color_map.append('#52b788' if level == 'package' else 
                           '#2d6a4f' if level == 'service' else
                           '#1b4332' if level == 'module' else
                           '#40916c' if level == 'system' else '#52b788')
        elif implementation_status == 'recommended':
            # Use yellow/amber tint for recommended components
            color_map.append('#f9c74f' if level == 'package' else
                           '#f9844a' if level == 'service' else
                           '#f8961e' if level == 'module' else
                           '#f3722c' if level == 'system' else '#f9c74f')
        elif implementation_status == 'hypothetical':
            # Use orange/red tint for hypothetical components
            color_map.append('#f94144' if level == 'package' else
                           '#f3722c' if level == 'service' else
                           '#f8961e' if level == 'module' else
                           '#f9844a' if level == 'system' else '#f94144')
        else:
            # Default to original level-based colors for unknown status
            color_map.append(base_color)
    
    # Draw nodes and edges with improved styling
    nx.draw_networkx_nodes(G, pos, node_size=1700, node_color=color_map, alpha=0.9)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=9, font_weight='bold')
    
    # Draw different edge types with different styles
    dependency_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') == 'dependency']
    interface_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') == 'interface']
    other_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') not in ['dependency', 'interface']]
    
    if dependency_edges:
        nx.draw_networkx_edges(G, pos, edgelist=dependency_edges, edge_color='red', 
                              arrowsize=18, arrowstyle='->', width=2, alpha=0.7)
    if interface_edges:
        nx.draw_networkx_edges(G, pos, edgelist=interface_edges, edge_color='blue', 
                              arrowsize=18, arrowstyle='->', width=1.5, alpha=0.6, style='dashed')
    if other_edges:
        nx.draw_networkx_edges(G, pos, edgelist=other_edges, edge_color='gray', 
                              arrowsize=15, arrowstyle='->', width=1, alpha=0.5)
    
    # Add a legend with both level and implementation status information
    from matplotlib.lines import Line2D
    legend_elements = [
        # Edge types
        Line2D([0], [0], color='red', lw=2, label='Dependencies'),
        Line2D([0], [0], color='blue', lw=1.5, linestyle='--', label='Interfaces'),
        # Implementation status
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#52b788', markersize=10, label='Existing (Verified)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#f9c74f', markersize=10, label='Recommended (LLM)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#f94144', markersize=10, label='Hypothetical (Guess)'),
        # Component levels (with example existing status colors)
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#40916c', markersize=8, label='Systems'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#52b788', markersize=8, label='Packages'),  
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#2d6a4f', markersize=8, label='Services'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#1b4332', markersize=8, label='Internal Modules')
    ]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=8)
    plt.title(title)
    plt.axis('off')
    if out_file:
        plt.savefig(out_file)
    plt.show()

# --- STEP 4: Export machine-readable graph object ---
def export_graph_json(G: nx.DiGraph, out_path: str):
    data = nx.node_link_data(G)
    with open(out_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Graph exported to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build and visualize a system-of-systems graph from an index.json")
    parser.add_argument('index', help='Path to index.json (absolute path recommended)')
    parser.add_argument('--mode', choices=['all', 'systems', 'packages', 'components', 'modules'], default='packages', 
                       help='Which hierarchy level(s) to include: modules (tier 3), packages/components (tier 2), systems (tier 1), or all')
    parser.add_argument('--layout', choices=['spectral', 'circular', 'shell', 'kamada', 'hierarchical', 'spring'], 
                       default='spectral', help='Graph layout algorithm')
    parser.add_argument('--png', default='system_of_systems_graph.png', help='Output PNG filename')
    parser.add_argument('--json', default='system_of_systems_graph.json', help='Output graph JSON filename')
    args = parser.parse_args()

    index_path = args.index
    index = load_service_architecture_index(index_path)
    print(f"Loaded {len(index)} components from index")

    if args.mode == 'all':
        include_levels = ['system_of_systems', 'system', 'service', 'package', 'module']
    elif args.mode == 'systems':
        include_levels = ['system', 'service']
    elif args.mode == 'components':
        include_levels = ['package']
    elif args.mode == 'modules':
        include_levels = ['module', 'package']  # Include parent packages for context
    else:  # packages (default)
        include_levels = ['package']

    G = build_system_graph(index, include_levels=include_levels)
    out_dir = os.path.dirname(index_path)
    out_json = os.path.join(out_dir, args.json)
    out_png = os.path.join(out_dir, args.png)
    title = f"System Architecture ({args.mode}) - {args.layout} layout"
    visualize_graph(G, out_file=out_png, title=title, layout=args.layout)
    export_graph_json(G, out_json)
    print(f"Nodes kept ({args.mode}): {len(G.nodes())}; Edges: {len(G.edges())}")
