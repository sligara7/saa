#!/usr/bin/env python3

import sys
import json
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime

class SystemCoverageValidator:
    def __init__(self, system_path: Path):
        self.system_path = Path(system_path)
        self.working_memory_path = self.system_path / "working_memory.json"
        self.issues = []
        self.required_systems = set()
        self.existing_systems = set()

    def load_required_systems(self) -> bool:
        """Load required systems from working memory"""
        try:
            if not self.working_memory_path.exists():
                self.issues.append("Working memory file not found")
                return False

            with open(self.working_memory_path) as f:
                memory = json.load(f)

            if "required_systems" not in memory:
                self.issues.append("No required systems defined in working memory")
                return False

            for system in memory["required_systems"]:
                self.required_systems.add(system["system_id"])

            return True

        except Exception as e:
            self.issues.append(f"Error loading working memory: {str(e)}")
            return False

    def find_existing_systems(self):
        """Find all existing system directories and their status"""
        try:
            # Find all system directories
            for dir_path in self.system_path.rglob("*_system"):
                if dir_path.is_dir():
                    system_id = dir_path.name
                    self.existing_systems.add(system_id)

                    # Check for service architecture file
                    arch_file = dir_path / "service_architecture.json"
                    if not arch_file.exists():
                        self.issues.append(f"System {system_id} missing service_architecture.json")

        except Exception as e:
            self.issues.append(f"Error scanning for systems: {str(e)}")

    def validate_coverage(self) -> dict:
        """Validate system coverage and generate report"""
        # Find missing required systems
        missing_systems = self.required_systems - self.existing_systems
        for system in missing_systems:
            self.issues.append(f"Required system {system} not found")

        # Find extra systems
        extra_systems = self.existing_systems - self.required_systems
        for system in extra_systems:
            self.issues.append(f"WARNING: System {system} exists but is not required")

        return {
            "timestamp": datetime.now().isoformat(),
            "system_path": str(self.system_path),
            "validation": {
                "required_systems": len(self.required_systems),
                "existing_systems": len(self.existing_systems),
                "missing_systems": list(missing_systems),
                "extra_systems": list(extra_systems),
                "status": "fail" if missing_systems else "pass"
            },
            "issues": self.issues
        }

    def update_working_memory(self, validation_results: dict):
        """Update working memory with validation results"""
        try:
            if not self.working_memory_path.exists():
                return

            with open(self.working_memory_path) as f:
                memory = json.load(f)

            # Update system status
            if "required_systems" in memory:
                for system in memory["required_systems"]:
                    system_id = system["system_id"]
                    if system_id in self.existing_systems:
                        # Check if service architecture exists
                        arch_file = self.system_path / system_id / "service_architecture.json"
                        if arch_file.exists():
                            system["status"] = "created"
                            system["created_at"] = datetime.now().isoformat()
                        else:
                            system["status"] = "incomplete"
                    else:
                        system["status"] = "missing"

            # Add validation results
            memory["last_validation"] = {
                "timestamp": validation_results["timestamp"],
                "status": validation_results["validation"]["status"],
                "issues": validation_results["issues"]
            }

            with open(self.working_memory_path, "w") as f:
                json.dump(memory, f, indent=2)

        except Exception as e:
            self.issues.append(f"Error updating working memory: {str(e)}")

def main():
    if len(sys.argv) != 2:
        print("Usage: validate_system_coverage.py <system_path>")
        sys.exit(1)

    system_path = Path(sys.argv[1])
    if not system_path.exists():
        print(f"Error: System path {system_path} does not exist")
        sys.exit(1)

    validator = SystemCoverageValidator(system_path)
    
    # Load required systems
    if not validator.load_required_systems():
        print("Error loading required systems")
        sys.exit(1)

    # Find existing systems
    validator.find_existing_systems()

    # Validate and generate report
    results = validator.validate_coverage()
    
    # Update working memory
    validator.update_working_memory(results)

    # Output results
    print(json.dumps(results, indent=2))
    
    # Exit with status
    sys.exit(0 if results["validation"]["status"] == "pass" else 1)

if __name__ == "__main__":
    main()