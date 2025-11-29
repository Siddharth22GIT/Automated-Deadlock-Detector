import time
import random
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from resource_tracker import ResourceTracker
from process_monitor import ProcessMonitor
from wfg_builder import WFG
from deadlock_detector import DeadlockDetector
from utils.logger import log

def simulate_processes(monitor: ProcessMonitor, num_processes: int, num_resources: int):
    """Simulate processes requesting and releasing resources."""
    processes = [f"P{i+1}" for i in range(num_processes)]
    resources = [f"R{i+1}" for i in range(num_resources)]
    
    # Initialize processes
    for process in processes:
        monitor.create_process(process)
    
    # Simulate resource requests and releases
    for _ in range(20):  # Run 20 simulation steps
        process = random.choice(processes)
        resource = random.choice(resources)
        
        # Randomly decide to request or release a resource
        if random.random() > 0.5:
            log(f"Process {process} requesting {resource}")
            granted = monitor.request_resource(process, resource)
            log(f"  → {'Granted' if granted else 'Waiting'}")
        else:
            log(f"Process {process} releasing {resource}")
            monitor.release_resource(process, resource)
            
        # Check for deadlocks
        wfg = WFG(monitor)
        detector = DeadlockDetector(wfg)
        cycle = detector.find_cycle()
        
        if cycle:
            log(f"[DEADLOCK] Cycle detected: {' → '.join(cycle)}", "ERROR")
        
        time.sleep(0.5)  # Small delay for readability

def main():
    """Main function to run the deadlock detector."""
    log("Starting Deadlock Detector...")
    
    # Initialize components
    resource_tracker = ResourceTracker()
    monitor = ProcessMonitor(resource_tracker)
    
    try:
        # Simulate with 3 processes and 3 resources
        simulate_processes(monitor, num_processes=3, num_resources=3)
    except KeyboardInterrupt:
        log("\nSimulation stopped by user.")
    
    log("Deadlock Detector stopped.")

if __name__ == "__main__":
    main()