import random
from typing import Dict, List, Set, Tuple
from resource_tracker import ResourceTracker

class ProcessMonitor:
    """Simulates processes and their resource usage."""
    def __init__(self, resource_tracker: ResourceTracker):
        self.resource_tracker = resource_tracker
        self.process_resources: Dict[str, Set[str]] = {}
        self.waiting_processes: Dict[str, str] = {}

    def create_process(self, process_id: str):
        """Initialize a new process with no resources."""
        self.process_resources[process_id] = set()

    def request_resource(self, process_id: str, resource_id: str) -> bool:
        """Process requests a resource. Returns True if granted, False if waiting."""
        if process_id not in self.process_resources:
            self.create_process(process_id)
            
        granted = self.resource_tracker.request_resource(process_id, resource_id)
        if granted:
            self.process_resources[process_id].add(resource_id)
        else:
            self.waiting_processes[process_id] = resource_id
        return granted

    def release_resource(self, process_id: str, resource_id: str):
        """Release a resource held by a process."""
        if (process_id in self.process_resources and 
            resource_id in self.process_resources[process_id]):
            self.process_resources[process_id].remove(resource_id)
            self.resource_tracker.release_resource(resource_id)

    def get_process_resources(self, process_id: str) -> Set[str]:
        """Get all resources held by a process."""
        return self.process_resources.get(process_id, set())

    def get_waiting_processes(self) -> Dict[str, str]:
        """Get all processes waiting for resources."""
        return self.waiting_processes

    def get_all_processes(self) -> List[str]:
        """Get all process IDs."""
        return list(self.process_resources.keys())