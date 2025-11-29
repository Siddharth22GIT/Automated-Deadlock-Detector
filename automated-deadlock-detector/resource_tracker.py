from typing import Dict, List, Optional

class ResourceTracker:
    """
    Maintains the state of resources, including owners and waiting processes.
    """
    def __init__(self):
        self.resource_owners: Dict[str, str] = {}
        self.wait_queue: Dict[str, List[str]] = {}

    def request_resource(self, process_id: str, resource_id: str) -> bool:
        """
        A process requests a resource. Returns True if granted, False if waiting.
        """
        if resource_id not in self.resource_owners:
            self.resource_owners[resource_id] = process_id
            return True
        else:
            if resource_id not in self.wait_queue:
                self.wait_queue[resource_id] = []
            self.wait_queue[resource_id].append(process_id)
            return False

    def release_resource(self, resource_id: str) -> Optional[str]:
        """
        Releases a resource and grants it to the next waiting process, if any.
        Returns the new owner's ID or None if the resource is now free.
        """
        if resource_id in self.resource_owners:
            del self.resource_owners[resource_id]

            if resource_id in self.wait_queue and self.wait_queue[resource_id]:
                next_process = self.wait_queue[resource_id].pop(0)
                self.resource_owners[resource_id] = next_process
                return next_process
        return None
