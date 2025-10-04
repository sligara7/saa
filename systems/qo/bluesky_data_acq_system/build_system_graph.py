#!/usr/bin/env python3
"""
Build global system graph for Bluesky Data Acquisition System-of-Systems
Analyzes communication paths and validates interface consistency
"""

import json
import os
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Set

def load_service_architecture(file_path: str) -> Dict:
    """Load service architecture JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def find_all_service_files(base_path: str) -> List[Tuple[str, str]]:
    """Find all service_architecture.json files and return (service_id, file_path) tuples"""
    service_files = []
    base_path = Path(base_path)
    
    for json_file in base_path.rglob("service_architecture.json"):
        # Load to get service_id
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                service_id = data.get('service_id', json_file.parent.name)
                service_files.append((service_id, str(json_file)))
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
    
    return service_files

def build_system_graph(base_path: str) -> nx.DiGraph:
    """Build directed graph of system architecture"""
    G = nx.DiGraph()
    
    # Find all service architecture files
    service_files = find_all_service_files(base_path)
    
    # Load all services and add as nodes
    services = {}
    for service_id, file_path in service_files:
        try:
            service_data = load_service_architecture(file_path)
            services[service_id] = service_data
            
            # Add node with attributes
            G.add_node(service_id, 
                      name=service_data.get('service_name', service_id),
                      tier=service_data.get('hierarchical_tier', 'unknown'),
                      classification=service_data.get('component_classification', 'unknown'),
                      is_external=service_data.get('is_external', False),
                      file_path=file_path)
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Add edges based on dependencies and interfaces
    for service_id, service_data in services.items():
        # Add dependency edges
        for dep in service_data.get('dependencies', []):
            if dep in services:
                G.add_edge(service_id, dep, 
                          relationship='dependency',
                          description=f"{service_id} depends on {dep}")
        
        # Add interface edges
        for interface in service_data.get('interfaces', []):
            interface_type = interface.get('interface_type', 'unknown')
            communication_pattern = interface.get('communication_pattern', 'unknown')
            dependency_type = interface.get('dependency_type', 'unknown')
            
            # For service dependencies, add edges to the target services
            if interface_type == 'service_dependency':
                # Try to infer target service from interface description or name
                description = interface.get('description', '').lower()
                interface_name = interface.get('name', '').lower()
                
                # Look for service names in description
                for target_service in services.keys():
                    if target_service.lower() in description or target_service.lower() in interface_name:
                        G.add_edge(service_id, target_service,
                                  relationship='interface',
                                  interface_type=interface_type,
                                  communication_pattern=communication_pattern,
                                  dependency_type=dependency_type,
                                  description=interface.get('description', ''))
    
    return G

def analyze_communication_paths(G: nx.DiGraph) -> Dict:
    """Analyze end-to-end communication paths in the system"""
    analysis = {
        'total_nodes': G.number_of_nodes(),
        'total_edges': G.number_of_edges(),
        'external_nodes': [],
        'tier_distribution': {},
        'communication_paths': [],
        'potential_bottlenecks': [],
        'isolated_nodes': [],
        'cycles': []
    }
    
    # Analyze node characteristics
    for node, attrs in G.nodes(data=True):
        tier = attrs.get('tier', 'unknown')
        analysis['tier_distribution'][tier] = analysis['tier_distribution'].get(tier, 0) + 1
        
        if attrs.get('is_external', False):
            analysis['external_nodes'].append(node)
    
    # Find isolated nodes
    analysis['isolated_nodes'] = list(nx.isolates(G))
    
    # Find cycles
    try:
        cycles = list(nx.simple_cycles(G))
        analysis['cycles'] = cycles
    except:
        analysis['cycles'] = []
    
    # Find potential bottlenecks (high degree nodes)
    degrees = dict(G.degree())
    avg_degree = sum(degrees.values()) / len(degrees) if degrees else 0
    analysis['potential_bottlenecks'] = [
        (node, degree) for node, degree in degrees.items() 
        if degree > avg_degree * 1.5
    ]
    
    # Analyze communication paths between major services
    major_services = [
        'queue_server_service',
        'device_monitoring_service', 
        'coordination_service'
    ]
    
    for i, source in enumerate(major_services):
        for target in major_services[i+1:]:
            if source in G and target in G:
                try:
                    if nx.has_path(G, source, target):
                        path = nx.shortest_path(G, source, target)
                        analysis['communication_paths'].append({
                            'source': source,
                            'target': target,
                            'path': path,
                            'length': len(path) - 1
                        })
                except:
                    pass
    
    return analysis

def generate_interface_recommendations(G: nx.DiGraph, analysis: Dict) -> List[Dict]:
    """Generate recommendations for missing or improved interfaces"""
    recommendations = []
    
    # Check for coordination service integration
    coordination_service = 'coordination_service'
    major_services = ['queue_server_service', 'device_monitoring_service']
    
    if coordination_service in G:
        for service in major_services:
            if service in G:
                # Check if coordination interface exists
                has_coordination_interface = False
                for _, neighbor, data in G.edges(service, data=True):
                    if neighbor == coordination_service or 'coordination' in data.get('description', '').lower():
                        has_coordination_interface = True
                        break
                
                if not has_coordination_interface:
                    recommendations.append({
                        'type': 'missing_interface',
                        'source': service,
                        'target': coordination_service,
                        'description': f'Add coordination interface between {service} and {coordination_service}',
                        'priority': 'high',
                        'rationale': 'Required for safe multi-user remote operation'
                    })
    
    # Check for unified web client access
    web_services = ['bluesky_httpserver', 'ophyd_websocket']
    nginx_service = 'nginx'
    
    if nginx_service in G:
        for web_service in web_services:
            if web_service in G and not G.has_edge(nginx_service, web_service):
                recommendations.append({
                    'type': 'missing_routing',
                    'source': nginx_service,
                    'target': web_service,
                    'description': f'Add nginx routing to {web_service}',
                    'priority': 'medium',
                    'rationale': 'Required for unified web client access'
                })
    
    return recommendations

def visualize_system_graph(G: nx.DiGraph, output_path: str):
    """Create visualization of the system graph"""
    plt.figure(figsize=(20, 16))
    
    # Create layout
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # Color nodes by tier
    tier_colors = {
        'tier_0_system_of_systems': '#ff7f7f',
        'tier_1_systems': '#7f7fff', 
        'tier_2_components': '#7fff7f',
        'unknown': '#ffff7f'
    }
    
    node_colors = []
    for node in G.nodes():
        tier = G.nodes[node].get('tier', 'unknown')
        node_colors.append(tier_colors.get(tier, '#cccccc'))
    
    # Draw external nodes differently
    external_nodes = [node for node, attrs in G.nodes(data=True) if attrs.get('is_external', False)]
    internal_nodes = [node for node in G.nodes() if node not in external_nodes]
    
    # Draw internal nodes
    if internal_nodes:
        internal_colors = [tier_colors.get(G.nodes[node].get('tier', 'unknown'), '#cccccc') 
                          for node in internal_nodes]
        nx.draw_networkx_nodes(G, pos, nodelist=internal_nodes, 
                              node_color=internal_colors, node_size=1000, alpha=0.8)
    
    # Draw external nodes
    if external_nodes:
        external_colors = [tier_colors.get(G.nodes[node].get('tier', 'unknown'), '#cccccc') 
                          for node in external_nodes]
        nx.draw_networkx_nodes(G, pos, nodelist=external_nodes,
                              node_color=external_colors, node_size=800, 
                              node_shape='s', alpha=0.6)
    
    # Draw edges
    dependency_edges = [(u, v) for u, v, d in G.edges(data=True) 
                       if d.get('relationship') == 'dependency']
    interface_edges = [(u, v) for u, v, d in G.edges(data=True) 
                      if d.get('relationship') == 'interface']
    
    if dependency_edges:
        nx.draw_networkx_edges(G, pos, edgelist=dependency_edges, 
                              edge_color='blue', style='solid', alpha=0.6, width=2)
    
    if interface_edges:
        nx.draw_networkx_edges(G, pos, edgelist=interface_edges,
                              edge_color='red', style='dashed', alpha=0.6, width=1)
    
    # Draw labels
    labels = {node: node.replace('_', '\n') for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
    
    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#ff7f7f', 
                  markersize=10, label='Tier 0: System-of-Systems'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#7f7fff', 
                  markersize=10, label='Tier 1: Systems'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#7fff7f', 
                  markersize=10, label='Tier 2: Components'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', 
                  markersize=8, label='External Systems'),
        plt.Line2D([0], [0], color='blue', linewidth=2, label='Dependencies'),
        plt.Line2D([0], [0], color='red', linestyle='--', label='Interfaces')
    ]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
    
    plt.title('Bluesky Data Acquisition System-of-Systems Architecture', fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Main analysis function"""
    base_path = "/home/asligar/git_projects/saa/systems/qo/bluesky_data_acq_system"
    
    print("Building system graph...")
    G = build_system_graph(base_path)
    
    print(f"Graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    
    print("Analyzing communication paths...")
    analysis = analyze_communication_paths(G)
    
    print("Generating interface recommendations...")
    recommendations = generate_interface_recommendations(G, analysis)
    
    # Save analysis results
    results = {
        'analysis': analysis,
        'recommendations': recommendations,
        'graph_summary': {
            'nodes': list(G.nodes()),
            'edges': [(u, v, d) for u, v, d in G.edges(data=True)]
        }
    }
    
    output_file = f"{base_path}/system_analysis.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Analysis saved to {output_file}")
    
    # Generate visualization
    viz_path = f"{base_path}/system_graph.png"
    print(f"Generating visualization at {viz_path}...")
    visualize_system_graph(G, viz_path)
    
    # Print summary
    print("\n=== SYSTEM ANALYSIS SUMMARY ===")
    print(f"Total components: {analysis['total_nodes']}")
    print(f"Total connections: {analysis['total_edges']}")
    print(f"External systems: {len(analysis['external_nodes'])}")
    print(f"Tier distribution: {analysis['tier_distribution']}")
    
    if analysis['isolated_nodes']:
        print(f"Isolated nodes: {analysis['isolated_nodes']}")
    
    if analysis['cycles']:
        print(f"Circular dependencies detected: {analysis['cycles']}")
    
    if analysis['potential_bottlenecks']:
        print("Potential bottlenecks:")
        for node, degree in analysis['potential_bottlenecks']:
            print(f"  - {node}: {degree} connections")
    
    print(f"\nCommunication paths between major services:")
    for path_info in analysis['communication_paths']:
        print(f"  {path_info['source']} -> {path_info['target']}: {' -> '.join(path_info['path'])}")
    
    print(f"\nInterface recommendations ({len(recommendations)}):")
    for rec in recommendations:
        print(f"  - {rec['type']}: {rec['description']} (Priority: {rec['priority']})")

if __name__ == "__main__":
    main()