import os
import json

"""
Retroactively index all service_architecture.json files in the XRPL example directory.
Creates a service_architecture_index.json mapping service_id to absolute file path.
"""

ROOT = '/home/ajs7/project/saa_package/examples/xrpl_example'
INDEX_PATH = os.path.join(ROOT, 'service_architecture_index.json')

def find_service_architecture_files(root):
    index = {}
    for entry in os.listdir(root):
        entry_path = os.path.join(root, entry)
        if os.path.isdir(entry_path):
            sa_path = os.path.join(entry_path, 'service_architecture.json')
            if os.path.isfile(sa_path):
                try:
                    with open(sa_path, 'r') as f:
                        data = json.load(f)
                        # Try to extract service_id from top-level, srd, or icd
                        service_id = None
                        if 'service_id' in data:
                            service_id = data['service_id']
                        elif 'srd' in data and 'service_id' in data['srd']:
                            service_id = data['srd']['service_id']
                        elif 'icd' in data and 'service_id' in data['icd']:
                            service_id = data['icd']['service_id']
                        else:
                            # Fallback: use folder name
                            service_id = entry
                        index[service_id] = os.path.abspath(sa_path)
                except Exception as e:
                    print(f"Warning: Could not read {sa_path}: {e}")
    return index

def main():
    index = find_service_architecture_files(ROOT)
    with open(INDEX_PATH, 'w') as f:
        json.dump(index, f, indent=2)
    print(f"Indexed {len(index)} services. Index written to {INDEX_PATH}")

if __name__ == "__main__":
    main()
