from typing import Dict, List, Set, Tuple
from process_monitor import ProcessMonitor

class WFG:
    """
    Builds and maintains a Wait-For Graph (WFG) to detect deadlocks.
    An edge P1 -> P2 means P1 is waiting for a resource held by P2.
    """
    def __init__(self, process_monitor: ProcessMonitor):
        self.process_monitor = process_monitor
        self.graph: Dict[str, Set[str]] = {}

    def build_graph(self) -> Dict[str, Set[str]]:
        """
        Build the WFG by checking which processes are waiting for resources
        held by other processes.
        """
        self.graph = {}
        waiting_processes = self.process_monitor.get_waiting_processes()
        
        for process, resource in waiting_processes.items():
            # Find which process holds the resource we're waiting for
            for other_process in self.process_monitor.get_all_processes():
                if resource in self.process_monitor.get_process_resources(other_process):
                    if process not in self.graph:
                        self.graph[process] = set()
                    self.graph[process].add(other_process)
        
        return self.graph

    def get_graph(self) -> Dict[str, Set[str]]:
        """Return the current WFG."""
        return self.graph