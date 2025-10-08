
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

def build_system_graph(index: Dict[str, str], include_levels: List[str], index_dir: str) -> nx.DiGraph:
    """Build a directed graph from all service_architecture.json files filtering by include_levels (e.g., ['package']).
    
    Args:
        index: Dictionary mapping service_id to file paths
        include_levels: List of levels to include in the graph
        index_dir: Directory containing the index.json file, used for resolving relative paths
    """
    G = nx.DiGraph()
    service_info = {}
    node_levels = {}
    
    # Pass 1: load and classify
    for service_id, file_path in index.items():
        # Handle relative paths by making them relative to index directory
        if not os.path.isabs(file_path):
            file_path = os.path.join(index_dir, file_path)
        
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
    # Increase figure size for better readability
    plt.figure(figsize=(20, 14))
    
    # Choose layout algorithm with improved positioning
    if layout == 'spectral':
        pos = nx.spectral_layout(G, scale=2.0)
    elif layout == 'circular':
        pos = nx.circular_layout(G, scale=2.0)
    elif layout == 'shell':
        # Group nodes by level for shell layout
        levels = {}
        for n in G.nodes:
            level = G.nodes[n].get('level', 'unknown')
            if level not in levels:
                levels[level] = []
            levels[level].append(n)
        
        # Order shells from outer to inner based on hierarchy
        level_order = ['system_of_systems', 'system', 'service', 'package', 'module']
        ordered_shells = []
        for level in level_order:
            if level in levels and levels[level]:
                ordered_shells.append(levels[level])
        
        # Add any remaining levels not in the predefined order
        for level, nodes in levels.items():
            if level not in level_order and nodes:
                ordered_shells.append(nodes)
        
        pos = nx.shell_layout(G, nlist=ordered_shells, scale=2.0)
    elif layout == 'kamada':
        pos = nx.kamada_kawai_layout(G, scale=2.0)
    elif layout == 'hierarchical':
        # Create a better hierarchical layout
        try:
            import pygraphviz
            pos = nx.graphviz_layout(G, prog='dot', args='-Grankdir=TB -Gnodesep=1.5 -Granksep=2.0')
        except:
            # Fallback to a custom hierarchical layout
            pos = create_custom_hierarchical_layout(G)
    elif layout == 'custom_hierarchical':
        pos = create_custom_hierarchical_layout(G)
    else:  # spring (default fallback)
        pos = nx.spring_layout(G, seed=42, k=3.0, iterations=100, scale=2.0)
    
    # Scale positions to avoid overlap
    scale_factor = max(len(G.nodes) * 0.3, 2.0)
    pos = {node: (coord[0] * scale_factor, coord[1] * scale_factor) for node, coord in pos.items()}
    
    labels = nx.get_node_attributes(G, 'label')
    
    # Create color map with better contrast
    color_map = []
    node_sizes = []
    
    for n in G.nodes:
        node_data = G.nodes[n].get('raw', {})
        level = G.nodes[n].get('level', 'unknown')
        implementation_status = node_data.get('implementation_status', 'existing')
        
        # Set node size based on hierarchy level
        if level == 'system_of_systems':
            size = 3000
        elif level == 'system':
            size = 2500
        elif level == 'service':
            size = 2000
        elif level == 'package':
            size = 1500
        elif level == 'module':
            size = 1200
        else:
            size = 1500
        node_sizes.append(size)
        
        # Choose base color by level with better contrast
        if level == 'system_of_systems':
            base_color = '#003049'  # Dark blue
        elif level == 'system':
            base_color = '#219ebc'  # Blue
        elif level == 'service':
            base_color = '#ffb703'  # Orange
        elif level == 'package':
            base_color = '#8ecae6'  # Light blue
        elif level == 'module':
            base_color = '#fb8500'  # Dark orange
        else:
            base_color = '#adb5bd'  # Gray
        
        # Modify color based on implementation status
        if implementation_status == 'existing':
            # Use green tint for existing (verified) components
            color_map.append('#2d6a4f' if level == 'system_of_systems' else
                           '#40916c' if level == 'system' else 
                           '#52b788' if level == 'service' else
                           '#74c69d' if level == 'package' else
                           '#95d5b2' if level == 'module' else '#52b788')
        elif implementation_status == 'recommended':
            # Use amber tint for recommended components
            color_map.append('#f3722c' if level == 'system_of_systems' else
                           '#f8961e' if level == 'system' else
                           '#f9844a' if level == 'service' else
                           '#f9c74f' if level == 'package' else
                           '#90e0ef' if level == 'module' else '#f9c74f')
        elif implementation_status == 'hypothetical':
            # Use red tint for hypothetical components
            color_map.append('#6a040f' if level == 'system_of_systems' else
                           '#9d0208' if level == 'system' else
                           '#d00000' if level == 'service' else
                           '#dc2f02' if level == 'package' else
                           '#e85d04' if level == 'module' else '#f94144')
        else:
            # Default to original level-based colors for unknown status
            color_map.append(base_color)
    
    # Draw nodes with improved styling
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=color_map, 
                          alpha=0.9, linewidths=2, edgecolors='black')
    
    # Draw labels with better positioning and styling
    label_pos = {}
    for node, (x, y) in pos.items():
        label_pos[node] = (x, y)
    
    nx.draw_networkx_labels(G, label_pos, labels=labels, font_size=10, 
                           font_weight='bold', font_color='white',
                           bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
    
    # Draw different edge types with different styles
    dependency_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') == 'dependency']
    interface_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') == 'interface']
    other_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') not in ['dependency', 'interface']]
    
    if dependency_edges:
        nx.draw_networkx_edges(G, pos, edgelist=dependency_edges, edge_color='darkred', 
                              arrowsize=25, arrowstyle='->', width=3, alpha=0.8)
    if interface_edges:
        nx.draw_networkx_edges(G, pos, edgelist=interface_edges, edge_color='darkblue', 
                              arrowsize=20, arrowstyle='->', width=2, alpha=0.7, style='dashed')
    if other_edges:
        nx.draw_networkx_edges(G, pos, edgelist=other_edges, edge_color='gray', 
                              arrowsize=15, arrowstyle='->', width=1.5, alpha=0.6)
    
    # Add a comprehensive legend
    from matplotlib.lines import Line2D
    legend_elements = [
        # Edge types
        Line2D([0], [0], color='darkred', lw=3, label='Dependencies'),
        Line2D([0], [0], color='darkblue', lw=2, linestyle='--', label='Interfaces'),
        Line2D([0], [0], color='white', lw=0, label=''),  # Spacer
        # Implementation status
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#52b788', markersize=12, label='Existing (Verified)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#f9c74f', markersize=12, label='Recommended (LLM)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#f94144', markersize=12, label='Hypothetical (Guess)'),
        Line2D([0], [0], color='white', lw=0, label=''),  # Spacer
        # Component levels (with example existing status colors)
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#003049', markersize=15, label='System of Systems'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#40916c', markersize=12, label='Systems'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#52b788', markersize=10, label='Services'),  
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#74c69d', markersize=8, label='Packages'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#95d5b2', markersize=6, label='Internal Modules')
    ]
    plt.legend(handles=legend_elements, loc='upper left', fontsize=11, 
              fancybox=True, shadow=True, ncol=1)
    
    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    if out_file:
        plt.savefig(out_file, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Visualization saved to {out_file}")
    
    # Only show if not in headless mode
    import matplotlib
    if matplotlib.get_backend() != 'Agg':
        plt.show()
    else:
        plt.close()  # Close the figure to free memory

def create_custom_hierarchical_layout(G: nx.DiGraph) -> dict:
    """Create a custom hierarchical layout based on node levels"""
    pos = {}
    
    # Group nodes by level
    levels = {}
    for node in G.nodes:
        level = G.nodes[node].get('level', 'unknown')
        if level not in levels:
            levels[level] = []
        levels[level].append(node)
    
    # Define hierarchy order (top to bottom)
    level_order = ['system_of_systems', 'system', 'service', 'package', 'module']
    y_positions = {level: idx for idx, level in enumerate(reversed(level_order))}
    
    # Position nodes
    for level, nodes in levels.items():
        y = y_positions.get(level, len(level_order))
        x_spacing = 3.0 if len(nodes) > 1 else 0
        start_x = -(len(nodes) - 1) * x_spacing / 2
        
        for i, node in enumerate(sorted(nodes)):
            x = start_x + i * x_spacing
            pos[node] = (x, y * 2.0)  # Scale y for better separation
    
    return pos

# --- STEP 4: Export machine-readable graph object ---
def export_graph_json(G: nx.DiGraph, out_path: str):
    data = nx.node_link_data(G)
    with open(out_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Graph exported to {out_path}")

# --- STEP 5: Architectural Issue Detection ---
def detect_architectural_issues(G: nx.DiGraph) -> Dict[str, List[Dict]]:
    """Detect common architectural issues in the system graph"""
    issues = {
        'circular_dependencies': [],
        'orphaned_nodes': [],
        'missing_interfaces': [],
        'inconsistent_protocols': [],
        'security_gaps': [],
        'performance_bottlenecks': []
    }
    
    # 1. Detect circular dependencies
    try:
        cycles = list(nx.simple_cycles(G))
        for cycle in cycles:
            issues['circular_dependencies'].append({
                'cycle': cycle,
                'description': f"Circular dependency detected: {' -> '.join(cycle + [cycle[0]])}",
                'severity': 'critical',
                'recommendation': 'Consider introducing async communication or refactoring service responsibilities'
            })
    except:
        pass
    
    # 2. Find orphaned nodes (no incoming or outgoing edges)
    for node in G.nodes():
        in_degree = G.in_degree(node)
        out_degree = G.out_degree(node)
        if in_degree == 0 and out_degree == 0:
            issues['orphaned_nodes'].append({
                'node': node,
                'description': f"Orphaned node '{node}' has no connections",
                'severity': 'warning',
                'recommendation': 'Verify if this component is needed or add appropriate interfaces'
            })
    
    # 3. Check for nodes with high connectivity (potential bottlenecks)
    avg_degree = sum(dict(G.degree()).values()) / len(G.nodes()) if len(G.nodes()) > 0 else 0
    for node in G.nodes():
        total_degree = G.in_degree(node) + G.out_degree(node)
        if total_degree > max(avg_degree * 2, 5):  # Significantly above average or >5 connections
            issues['performance_bottlenecks'].append({
                'node': node,
                'connections': total_degree,
                'description': f"Node '{node}' has {total_degree} connections, potential bottleneck",
                'severity': 'warning',
                'recommendation': 'Consider load balancing or splitting responsibilities'
            })
    
    # 4. Check for missing authentication/security interfaces
    for node in G.nodes():
        node_data = G.nodes[node].get('raw', {})
        interfaces = node_data.get('interfaces', [])
        
        has_auth = False
        for interface in interfaces:
            if isinstance(interface, dict):
                if interface.get('auth_required', False) or 'auth' in interface.get('name', '').lower():
                    has_auth = True
                    break
        
        # If node has incoming connections but no auth, flag as potential security gap
        if G.in_degree(node) > 0 and not has_auth:
            issues['security_gaps'].append({
                'node': node,
                'description': f"Node '{node}' receives connections but lacks authentication interface",
                'severity': 'medium',
                'recommendation': 'Add authentication/authorization interface'
            })
    
    # 5. Check for inconsistent interface protocols
    protocol_map = {}
    for u, v, data in G.edges(data=True):
        edge_type = data.get('type', 'unknown')
        if edge_type not in protocol_map:
            protocol_map[edge_type] = []
        protocol_map[edge_type].append((u, v))
    
    # Look for nodes that mix protocols inconsistently
    for node in G.nodes():
        incoming_protocols = set()
        outgoing_protocols = set()
        
        for u, v, data in G.edges(data=True):
            protocol = data.get('type', 'unknown')
            if v == node:
                incoming_protocols.add(protocol)
            if u == node:
                outgoing_protocols.add(protocol)
        
        if len(incoming_protocols) > 2 or len(outgoing_protocols) > 2:
            issues['inconsistent_protocols'].append({
                'node': node,
                'incoming_protocols': list(incoming_protocols),
                'outgoing_protocols': list(outgoing_protocols),
                'description': f"Node '{node}' uses multiple communication protocols",
                'severity': 'info',
                'recommendation': 'Consider standardizing on fewer protocols for consistency'
            })
    
    return issues

def export_issues_report(issues: Dict, out_path: str):
    """Export architectural issues to a machine-readable JSON report"""
    
    # Count issues by severity
    severity_counts = {'critical': 0, 'warning': 0, 'medium': 0, 'info': 0}
    total_issues = 0
    
    for category, issue_list in issues.items():
        for issue in issue_list:
            severity = issue.get('severity', 'info')
            severity_counts[severity] += 1
            total_issues += 1
    
    report = {
        'analysis_timestamp': '2025-10-05T00:00:00Z',
        'summary': {
            'total_issues': total_issues,
            'critical_issues': severity_counts['critical'],
            'warning_issues': severity_counts['warning'],
            'medium_issues': severity_counts['medium'],
            'info_issues': severity_counts['info']
        },
        'architectural_issues': issues,
        'recommendations': {
            'immediate_action_required': severity_counts['critical'] > 0,
            'review_recommended': severity_counts['warning'] + severity_counts['medium'] > 0,
            'overall_status': 'needs_attention' if total_issues > 0 else 'healthy'
        }
    }
    
    with open(out_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Architectural issues report exported to {out_path}")
    print(f"Found {total_issues} issues: {severity_counts['critical']} critical, {severity_counts['warning']} warnings")
    
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build and visualize a system-of-systems graph from an index.json")
    parser.add_argument('index', help='Path to index.json (absolute path recommended)')
    parser.add_argument('--mode', choices=['all', 'systems', 'packages', 'components', 'modules', 'multi'], default='packages', 
                       help='Which hierarchy level(s) to include: modules (tier 3), packages/components (tier 2), systems (tier 1), all (all levels), or multi (generate multiple viewpoints)')
    parser.add_argument('--layout', choices=['spectral', 'circular', 'shell', 'kamada', 'hierarchical', 'spring', 'custom_hierarchical'], 
                       default='custom_hierarchical', help='Graph layout algorithm')
    parser.add_argument('--png', default='system_of_systems_graph.png', help='Output PNG filename (for single mode) or prefix (for multi mode)')
    parser.add_argument('--json', default='system_of_systems_graph.json', help='Output graph JSON filename')
    parser.add_argument('--issues', default='architecture_issues.json', help='Output architectural issues report filename')
    parser.add_argument('--no-display', action='store_true', help='Save files only, do not display graphs')
    parser.add_argument('--analyze-issues', action='store_true', help='Perform architectural issue analysis')
    args = parser.parse_args()

    # Resolve absolute path to index file and its containing directory
    index_path = os.path.abspath(args.index)
    index_dir = os.path.dirname(index_path)
    
    index = load_service_architecture_index(index_path)
    print(f"Loaded {len(index)} components from index")

    # Configure matplotlib for headless operation if requested
    if args.no_display:
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend

    # Define viewpoints for multi-mode
    viewpoints = [
        {'mode': 'systems', 'levels': ['system', 'service'], 'title': 'Systems & Services View'},
        {'mode': 'packages', 'levels': ['package'], 'title': 'Packages/Components View'},
        {'mode': 'modules', 'levels': ['module', 'package'], 'title': 'Internal Modules View'},
        {'mode': 'all', 'levels': ['system_of_systems', 'system', 'service', 'package', 'module'], 'title': 'Complete Architecture View'}
    ]

    if args.mode == 'multi':
        # Generate multiple viewpoints
        for viewpoint in viewpoints:
            include_levels = viewpoint['levels']
            G = build_system_graph(index, include_levels=include_levels, index_dir=index_dir)
            
            if len(G.nodes()) == 0:
                print(f"Skipping {viewpoint['mode']} view - no nodes at specified levels")
                continue
            
            # Create output filenames
            base_name = args.png.replace('.png', '')
            out_png = os.path.join(index_dir, f"{base_name}_{viewpoint['mode']}.png")
            out_json = os.path.join(index_dir, f"graph_{viewpoint['mode']}.json")
            
            title = f"{viewpoint['title']} - {args.layout} layout"
            
            if not args.no_display:
                visualize_graph(G, out_file=out_png, title=title, layout=args.layout)
            else:
                # Save without displaying
                import matplotlib.pyplot as plt
                plt.ioff()  # Turn off interactive mode
                visualize_graph(G, out_file=out_png, title=title, layout=args.layout)
                plt.close('all')
            
            export_graph_json(G, out_json)
            print(f"Generated {viewpoint['mode']} view: {len(G.nodes())} nodes, {len(G.edges())} edges")
            
            # Perform issue analysis if requested
            if args.analyze_issues:
                issues = detect_architectural_issues(G)
                issues_file = os.path.join(index_dir, f"issues_{viewpoint['mode']}.json")
                export_issues_report(issues, issues_file)
    
    else:
        # Single mode operation
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

        G = build_system_graph(index, include_levels=include_levels, index_dir=index_dir)
        
        # Write output files in the same directory as the index
        out_json = os.path.join(index_dir, args.json)
        out_png = os.path.join(index_dir, args.png)
        title = f"System Architecture ({args.mode}) - {args.layout} layout"
        
        if not args.no_display:
            visualize_graph(G, out_file=out_png, title=title, layout=args.layout)
        else:
            # Save without displaying
            import matplotlib.pyplot as plt
            plt.ioff()  # Turn off interactive mode
            visualize_graph(G, out_file=out_png, title=title, layout=args.layout)
            plt.close('all')
        
        export_graph_json(G, out_json)
        print(f"Nodes kept ({args.mode}): {len(G.nodes())}; Edges: {len(G.edges())}")
        
        # Perform issue analysis if requested
        if args.analyze_issues:
            issues = detect_architectural_issues(G)
            issues_file = os.path.join(index_dir, args.issues)
            export_issues_report(issues, issues_file)

    print("Graph generation complete!")
