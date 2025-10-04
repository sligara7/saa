import json
import networkx as nx
import matplotlib.pyplot as plt
import os

INDEX_PATH = "systems/human_body/index.json"

# Load index
with open(INDEX_PATH, "r") as f:
    index = json.load(f)

G = nx.DiGraph()

# Add nodes and edges from service_architecture.json files
for comp_id, json_path in index["components"].items():
    abs_path = os.path.join(os.getcwd(), json_path)
    with open(abs_path, "r") as f:
        service = json.load(f)
    G.add_node(comp_id, label=service["service_name"])
    for dep in service.get("dependencies", []):
        if dep in index["components"]:
            G.add_edge(comp_id, dep)
    # Add edges for explicit interfaces
    for iface in service.get("interfaces", []):
        target = None
        # Try to infer target from description or dependency
        for dep in service.get("dependencies", []):
            if dep in iface["description"] or dep in iface.get("name", ""):
                target = dep
        if target and target in index["components"]:
            G.add_edge(comp_id, target)

# Draw graph
plt.figure(figsize=(12,8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'), node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', arrowsize=20)
plt.title("Human Body System-of-Systems Architecture")
plt.savefig("systems/human_body/system_graph.png")
plt.show()

# Analysis
orphans = [n for n in G.nodes if G.in_degree(n) == 0 and G.out_degree(n) == 0]
print("Orphaned nodes:", orphans)
cycles = list(nx.simple_cycles(G))
print("Cycles:", cycles)
critical_nodes = list(nx.articulation_points(G.to_undirected()))
print("Single points of failure:", critical_nodes)
