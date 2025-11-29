from typing import Dict, List, Set, Optional
from wfg_builder import WFG

class DeadlockDetector:
    """
    Detects deadlocks by finding cycles in the Wait-For Graph (WFG).
    """
    def __init__(self, wfg: WFG):
        self.wfg = wfg

    def find_cycle(self) -> Optional[List[str]]:
        """
        Find a cycle in the WFG using DFS.
        Returns a list representing the cycle if found, None otherwise.
        """
        graph = self.wfg.get_graph()
        visited = set()
        rec_stack = set()
        path = []

        def dfs(node: str) -> Optional[List[str]]:
            if node in rec_stack:
                # Found a cycle, build the cycle path
                idx = path.index(node)
                return path[idx:] + [node]
            if node in visited:
                return None

            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in graph.get(node, set()):
                cycle = dfs(neighbor)
                if cycle:
                    return cycle

            path.pop()
            rec_stack.remove(node)
            return None

        for node in graph:
            cycle = dfs(node)
            if cycle:
                return cycle
        return None

    def has_deadlock(self) -> bool:
        """Check if there is a deadlock in the system."""
        return self.find_cycle() is not None