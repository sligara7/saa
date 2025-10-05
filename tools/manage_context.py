#!/usr/bin/env python3

import json
import sys
from pathlib import Path
from datetime import datetime
import subprocess
from typing import Dict, List, Optional

class ContextManager:
    def __init__(self, system_path: Path):
        self.system_path = Path(system_path)
        self.working_memory_path = self.system_path / "working_memory.json"
        self.process_log_path = self.system_path / "process_log.md"
        self.checkpoint_path = self.system_path / "context_checkpoint.md"
        
        # Load or initialize working memory
        self.working_memory = self.load_or_init_working_memory()

    def load_or_init_working_memory(self) -> dict:
        """Load working memory or create new from template"""
        if self.working_memory_path.exists():
            with open(self.working_memory_path) as f:
                return json.load(f)
        
        # Load template
        template_path = Path("/home/ajs7/project/saa/templates/working_memory_template.json")
        with open(template_path) as f:
            memory = json.load(f)
        
        memory["last_updated"] = datetime.now().isoformat()
        return memory

    def should_refresh_context(self) -> bool:
        """Check if context refresh is needed"""
        if not self.working_memory["context_state"]["last_refresh"]:
            return True

        last_refresh = datetime.fromisoformat(self.working_memory["context_state"]["last_refresh"])
        time_since_refresh = (datetime.now() - last_refresh).total_seconds() / 60
        ops_since_refresh = self.working_memory["context_state"]["operations_since_refresh"]

        return (
            time_since_refresh >= self.working_memory["refresh_triggers"]["time_window_minutes"] or
            ops_since_refresh >= self.working_memory["refresh_triggers"]["operation_count"]
        )

    def refresh_context(self) -> dict:
        """Perform context refresh sequence"""
        refresh_time = datetime.now().isoformat()
        
        # 1. Create checkpoint
        self.create_context_checkpoint()
        
        # 2. Reload definitions and templates
        self.reload_definitions()
        
        # 3. Run architecture validation
        validation_results = self.run_validation()
        
        # 4. Update working memory
        self.working_memory["context_state"].update({
            "definitions_loaded": True,
            "templates_verified": True,
            "system_validated": True,
            "last_refresh": refresh_time,
            "operations_since_refresh": 0
        })
        
        # 5. Log refresh in process log
        self.log_refresh(validation_results)
        
        # 6. Save updated working memory
        self.save_working_memory()
        
        return {
            "status": "success",
            "refresh_time": refresh_time,
            "validation_results": validation_results
        }

    def create_context_checkpoint(self):
        """Create context checkpoint file"""
        template_path = Path("/home/ajs7/project/saa/templates/context_checkpoint_template.md")
        with open(template_path) as f:
            template = f.read()

        # Replace template variables
        checkpoint = template.replace(
            "{{system_name}}", self.working_memory["system_context"]["system_name"]
        ).replace(
            "{{current_step}}", self.working_memory["system_context"]["current_step"]
        ).replace(
            "{{working_directory}}", str(self.system_path)
        ).replace(
            "{{checkpoint_time}}", datetime.now().isoformat()
        ).replace(
            "{{current_objectives}}", self._format_list(self.working_memory["system_context"].get("objectives", []))
        ).replace(
            "{{critical_constraints}}", self._format_list(self.working_memory["critical_context"]["constraints"])
        ).replace(
            "{{active_decisions}}", self._format_list(self.working_memory["critical_context"]["decisions"])
        ).replace(
            "{{recent_operations}}", self._format_list(self._get_recent_operations())
        )

        with open(self.checkpoint_path, "w") as f:
            f.write(checkpoint)

    def reload_definitions(self):
        """Reload architectural definitions and templates"""
        # This would typically reload from files, for now just mark as reloaded
        self.working_memory["context_state"]["definitions_loaded"] = True
        self.working_memory["context_state"]["templates_verified"] = True

    def run_validation(self) -> dict:
        """Run architecture validation"""
        try:
            result = subprocess.run(
                ["python3", "/home/ajs7/project/saa/tools/validate_architecture.py", str(self.system_path)],
                capture_output=True,
                text=True
            )
            return json.loads(result.stdout) if result.stdout else {"status": "failed", "error": result.stderr}
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def log_refresh(self, validation_results: dict):
        """Add refresh entry to process log"""
        if not self.process_log_path.exists():
            # Create new process log from template
            template_path = Path("/home/ajs7/project/saa/templates/process_log_template.md")
            with open(template_path) as f:
                template = f.read()
            with open(self.process_log_path, "w") as f:
                f.write(template)

        # Add refresh entry
        entry = f"\n| {datetime.now().isoformat()} | Auto | {validation_results['status']} | Continue current task |\n"
        
        with open(self.process_log_path, "a") as f:
            f.write(entry)

    def record_operation(self, operation: str):
        """Record an operation and check if refresh needed"""
        self.working_memory["context_state"]["operations_since_refresh"] += 1
        
        if self.should_refresh_context():
            return self.refresh_context()
        return None

    def save_working_memory(self):
        """Save current working memory state"""
        self.working_memory["last_updated"] = datetime.now().isoformat()
        with open(self.working_memory_path, "w") as f:
            json.dump(self.working_memory, f, indent=2)

    def _format_list(self, items: List[str]) -> str:
        """Format list for markdown"""
        return "\n".join(f"- {item}" for item in items)

    def _get_recent_operations(self) -> List[str]:
        """Get list of recent operations from working memory"""
        # This would typically get from some operation history
        return ["Context refresh triggered"]

def main():
    if len(sys.argv) < 2:
        print("Usage: manage_context.py <system_path> [operation]")
        sys.exit(1)

    system_path = Path(sys.argv[1])
    operation = sys.argv[2] if len(sys.argv) > 2 else None

    manager = ContextManager(system_path)
    
    if operation:
        # Record operation and check if refresh needed
        refresh_result = manager.record_operation(operation)
        if refresh_result:
            print("Context refresh performed:")
            print(json.dumps(refresh_result, indent=2))
    elif manager.should_refresh_context():
        # Force refresh
        refresh_result = manager.refresh_context()
        print("Context refresh performed:")
        print(json.dumps(refresh_result, indent=2))
    else:
        print("Context is current")

if __name__ == "__main__":
    main()