#!/usr/bin/env python3

import sys
from pathlib import Path
import json
import shutil
from typing import Dict, List, Tuple

class SystemCleaner:
    def __init__(self, system_path: Path):
        """Initialize with system path and load working memory"""
        self.system_path = Path(system_path)
        self.issues_found = []
        self.actions_taken = []
        self.required_systems = self.load_required_systems()

    def load_required_systems(self) -> dict:
        """Load required systems from working memory and feature summary"""
        working_memory_path = self.system_path / "working_memory.json"
        feature_summary_path = self.system_path / "dnd_service_feature_summary.md"
        required_systems = set()

        # Load from working memory if exists
        if working_memory_path.exists():
            try:
                with open(working_memory_path) as f:
                    memory = json.load(f)
                    if "required_systems" in memory:
                        for sys in memory["required_systems"]:
                            required_systems.add(sys["system_id"])
            except Exception as e:
                self.issues_found.append(f"Failed to load working memory: {str(e)}")

        # Parse feature summary for system requirements
        if feature_summary_path.exists():
            try:
                with open(feature_summary_path) as f:
                    content = f.read()
                    # Look for major section headers that indicate system requirements
                    sections = [
                        "Search & Discovery",
                        "Integration & Communication",
                        "Data Management & Persistence"
                    ]
                    for section in sections:
                        if section in content:
                            system_id = section.lower().replace(" & ", "_").replace(" ", "_") + "_system"
                            required_systems.add(system_id)
            except Exception as e:
                self.issues_found.append(f"Failed to parse feature summary: {str(e)}")

        return required_systems
        self.system_path = Path(system_path)
        self.issues_found = []
        self.actions_taken = []

    def find_empty_directories(self) -> List[Path]:
        """Find empty directories, marking required systems separately"""
        empty_dirs = []
        for dir_path in self.system_path.rglob('*'):
            if dir_path.is_dir():
                # Skip utility directories
                if any(x in str(dir_path) for x in ['__pycache__', '.git']):
                    continue
                    
                # Check if empty
                if not any(dir_path.iterdir()):
                    dir_name = dir_path.name
                    if dir_name in self.required_systems:
                        # Don't include required systems in removal list
                        self.issues_found.append(f"WARNING: Required system directory is empty: {dir_path}")
                    else:
                        empty_dirs.append(dir_path)
                        self.issues_found.append(f"Empty directory found: {dir_path}")
        return empty_dirs

    def find_incomplete_systems(self) -> List[Path]:
        """Find system directories missing service_architecture.json, with special handling for required systems"""
        incomplete_systems = []
        for dir_path in self.system_path.rglob('*'):
            if dir_path.is_dir():
                if 'system' in str(dir_path) and not (dir_path / 'service_architecture.json').exists():
                    # Check if it's a required system
                    dir_name = dir_path.name
                    is_required = dir_name in self.required_systems
                    
                    # Exclude parent directories that contain subsystems
                    if not any(d.is_dir() for d in dir_path.iterdir()):
                        if is_required:
                            self.issues_found.append(f"WARNING: Required system missing architecture: {dir_path}")
                        incomplete_systems.append(dir_path)
                        self.issues_found.append(f"System missing architecture: {dir_path}")
        return incomplete_systems

    def cleanup_empty_directories(self, empty_dirs: List[Path]):
        """Remove empty directories"""
        for dir_path in empty_dirs:
            try:
                dir_path.rmdir()
                self.actions_taken.append(f"Removed empty directory: {dir_path}")
            except Exception as e:
                self.issues_found.append(f"Failed to remove {dir_path}: {str(e)}")

    def create_stub_architecture(self, incomplete_systems: List[Path]):
        """Create stub service_architecture.json files for incomplete systems"""
        stub_architecture = {
            "service_name": "UNDEFINED",
            "service_id": "undefined",
            "hierarchical_tier": "tier_1_systems",
            "component_classification": "service",
            "purpose": "UNDEFINED - This is a stub architecture file",
            "dependencies": [],
            "interfaces": [],
            "is_external": False,
            "implementation_status": "stub",
            "version": "0.1+2025-10-05",
            "verification_notes": "This is a stub file created by cleanup_system.py"
        }
        
        for dir_path in incomplete_systems:
            try:
                # Customize stub for this system
                system_name = dir_path.name.replace('_', ' ').title()
                stub = stub_architecture.copy()
                stub["service_name"] = system_name
                stub["service_id"] = dir_path.name.lower()
                
                # Write stub file
                arch_file = dir_path / 'service_architecture.json'
                with open(arch_file, 'w') as f:
                    json.dump(stub, f, indent=2)
                self.actions_taken.append(f"Created stub architecture: {arch_file}")
            except Exception as e:
                self.issues_found.append(f"Failed to create stub for {dir_path}: {str(e)}")

    def generate_report(self) -> dict:
        """Generate cleanup report"""
        return {
            "timestamp": "2025-10-05T00:15:00Z",
            "system_path": str(self.system_path),
            "issues_found": self.issues_found,
            "actions_taken": self.actions_taken
        }

def main():
    if len(sys.argv) != 2:
        print("Usage: cleanup_system.py <system_path>")
        sys.exit(1)

    system_path = Path(sys.argv[1])
    if not system_path.exists():
        print(f"Error: System path {system_path} does not exist")
        sys.exit(1)

    cleaner = SystemCleaner(system_path)
    
    # Find issues
    empty_dirs = cleaner.find_empty_directories()
    incomplete_systems = cleaner.find_incomplete_systems()
    
    if not empty_dirs and not incomplete_systems:
        print("No issues found.")
        sys.exit(0)
    
    # Summarize issues
    print("\nIssues found:")
    for issue in cleaner.issues_found:
        print(f"- {issue}")
    
    # Ask for confirmation
    response = input("\nWould you like to:\n1) Remove empty directories\n2) Create stub architectures\n3) Both\n4) Cancel\nChoice: ")
    
    if response == "1":
        cleaner.cleanup_empty_directories(empty_dirs)
    elif response == "2":
        cleaner.create_stub_architecture(incomplete_systems)
    elif response == "3":
        cleaner.cleanup_empty_directories(empty_dirs)
        cleaner.create_stub_architecture(incomplete_systems)
    else:
        print("Operation cancelled.")
        sys.exit(0)
    
    # Generate and save report
    report = cleaner.generate_report()
    report_path = system_path / "cleanup_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print("\nActions taken:")
    for action in cleaner.actions_taken:
        print(f"- {action}")
    print(f"\nCleanup report saved to: {report_path}")

if __name__ == "__main__":
    main()