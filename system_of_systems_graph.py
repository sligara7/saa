
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List

# --- CONFIG ---
# Path to the robust index file
INDEX_PATH = '/home/ajs7/project/saa_package/examples/xrpl_example/service_architecture_index.json'

# --- STEP 1: Load the robust index file ---
def load_service_architecture_index(index_path: str) -> Dict[str, str]:
    """Load the mapping of service_id to absolute file path from the index file."""
    with open(index_path, 'r') as f:
        return json.load(f)

# --- STEP 2: Build the system-of-systems graph ---
def build_system_graph(index: Dict[str, str]) -> nx.DiGraph:
    """Build a directed graph from all service_architecture.json files."""
    G = nx.DiGraph()
    service_info = {}
    # First, add all nodes
    for service_id, file_path in index.items():
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Try to get a human-friendly name
            if 'service_name' in data:
                name = data['service_name']
            elif 'srd' in data and 'service_name' in data['srd']:
                name = data['srd']['service_name']
            else:
                name = service_id
            G.add_node(service_id, label=name)
            service_info[service_id] = data
    # Then, add edges based on dependencies/interfaces
    for service_id, data in service_info.items():
        # Try both top-level and nested (srd/icd) structures
        dependencies = []
        if 'dependencies' in data:
            dependencies = data['dependencies']
        elif 'srd' in data and 'dependencies' in data['srd']:
            dependencies = data['srd']['dependencies']
        # Add edges for dependencies
        for dep in dependencies:
            # Try to match dependency to a known service_id
            dep_id = None
            for sid, info in service_info.items():
                if dep.lower().replace(' ', '_') in [sid, info.get('service_name', '').lower().replace(' ', '_')]:
                    dep_id = sid
                    break
            if dep_id:
                G.add_edge(service_id, dep_id, type='dependency')
            else:
                G.add_edge(service_id, dep, type='external_dependency')
        # Optionally, add edges for interfaces (if they specify dependencies)
        icd = data.get('icd', data)
        interfaces = icd.get('interfaces', [])
        for iface in interfaces:
            for dep in iface.get('dependencies', []):
                dep_id = None
                for sid, info in service_info.items():
                    if dep.lower().replace(' ', '_') in [sid, info.get('service_name', '').lower().replace(' ', '_')]:
                        dep_id = sid
                        break
                if dep_id:
                    G.add_edge(service_id, dep_id, type='interface')
                else:
                    G.add_edge(service_id, dep, type='external_interface')
    return G

# --- STEP 3: Visualize the graph ---
def visualize_graph(G: nx.DiGraph, out_file: str = None):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', arrowsize=20)
    edge_labels = {(u, v): d['type'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.title('System-of-Systems Service Architecture')
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
    index = load_service_architecture_index(INDEX_PATH)
    print(f"Indexed services: {list(index.keys())}")
    G = build_system_graph(index)
    # Save the graph JSON in the same directory as the index
    out_json = os.path.join(os.path.dirname(INDEX_PATH), 'system_of_systems_graph.json')
    visualize_graph(G)
    export_graph_json(G, out_json)
