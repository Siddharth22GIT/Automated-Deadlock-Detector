import tkinter as tk
from tkinter import ttk, messagebox
import time
import random
from resource_tracker import ResourceTracker
from process_monitor import ProcessMonitor
from wfg_builder import WFG
from deadlock_detector import DeadlockDetector
from utils.logger import log

class DeadlockDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deadlock Detector")
        self.root.geometry("900x600")
        
        # Initialize components
        self.resource_tracker = ResourceTracker()
        self.process_monitor = ProcessMonitor(self.resource_tracker)
        self.wfg = WFG(self.process_monitor)
        self.detector = DeadlockDetector(self.wfg)
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Controls
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Process controls
        ttk.Label(control_frame, text="Process ID:").pack(pady=(0, 5))
        self.process_entry = ttk.Entry(control_frame)
        self.process_entry.pack(pady=(0, 10))
        
        ttk.Label(control_frame, text="Resource ID:").pack(pady=(0, 5))
        self.resource_entry = ttk.Entry(control_frame)
        self.resource_entry.pack(pady=(0, 10))
        
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Request", command=self.request_resource).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Release", command=self.release_resource).pack(side=tk.LEFT, padx=5)
        
        # Right panel - Status
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Resource status
        ttk.Label(status_frame, text="Resource Allocation:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.resource_status = tk.Text(status_frame, height=8, width=50)
        self.resource_status.pack(fill=tk.X, pady=(0, 10))
        
        # Process status
        ttk.Label(status_frame, text="Process Status:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.process_status = tk.Text(status_frame, height=8, width=50)
        self.process_status.pack(fill=tk.X, pady=(0, 10))
        
        # WFG visualization
        ttk.Label(status_frame, text="Wait-For Graph:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.wfg_canvas = tk.Canvas(status_frame, bg='white', height=200)
        self.wfg_canvas.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Log
        ttk.Label(status_frame, text="Activity Log:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.log_text = tk.Text(status_frame, height=6, width=50)
        self.log_text.pack(fill=tk.X)
        
        # Auto-update status
        self.update_status()
    
    def log(self, message, level="INFO"):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] [{level}] {message}\n")
        self.log_text.see(tk.END)
    
    def request_resource(self):
        process_id = self.process_entry.get()
        resource_id = self.resource_entry.get()
        
        if not process_id or not resource_id:
            messagebox.showerror("Error", "Please enter both process and resource IDs")
            return
            
        self.log(f"Process {process_id} requesting {resource_id}")
        granted = self.process_monitor.request_resource(process_id, resource_id)
        self.log(f"  → {'Granted' if granted else 'Waiting'}")
        
        # Check for deadlocks
        self.check_deadlock()
        self.update_status()
    
    def release_resource(self):
        process_id = self.process_entry.get()
        resource_id = self.resource_entry.get()
        
        if not process_id or not resource_id:
            messagebox.showerror("Error", "Please enter both process and resource IDs")
            return
            
        self.log(f"Process {process_id} releasing {resource_id}")
        self.process_monitor.release_resource(process_id, resource_id)
        
        # Update status
        self.check_deadlock()
        self.update_status()
    
    def check_deadlock(self):
        self.wfg.build_graph()
        cycle = self.detector.find_cycle()
        if cycle:
            cycle_str = " → ".join(cycle)
            self.log(f"DEADLOCK DETECTED! Cycle: {cycle_str}", "ERROR")
            messagebox.showwarning("Deadlock Detected", f"Deadlock detected in cycle: {cycle_str}")
    
    def update_status(self):
        # Update resource status
        self.resource_status.delete(1.0, tk.END)
        for resource, process in self.resource_tracker.resource_owners.items():
            self.resource_status.insert(tk.END, f"Resource {resource} → Process {process}\n")
        
        # Update process status
        self.process_status.delete(1.0, tk.END)
        for process, resources in self.process_monitor.process_resources.items():
            self.process_status.insert(tk.END, f"Process {process} holds: {', '.join(resources) if resources else 'None'}\n")
        
        # Update WFG visualization
        self.wfg_canvas.delete("all")
        self.wfg.build_graph()
        self.draw_wfg()
        
        # Schedule next update
        self.root.after(1000, self.update_status)
    
    def draw_wfg(self):
        # Simple WFG visualization
        graph = self.wfg.get_graph()
        if not graph:
            self.wfg_canvas.create_text(150, 100, text="No waiting processes", fill="gray")
            return
            
        # Simple node positioning
        nodes = set()
        for src in graph:
            nodes.add(src)
            for dst in graph[src]:
                nodes.add(dst)
        
        node_pos = {}
        radius = 20
        width = self.wfg_canvas.winfo_width()
        height = self.wfg_canvas.winfo_height()
        
        # Position nodes in a circle
        num_nodes = len(nodes)
        if num_nodes > 0:
            center_x, center_y = width // 2, height // 2
            radius_circle = min(center_x, center_y) - 30
            
            for i, node in enumerate(nodes):
                angle = 2 * 3.14159 * i / num_nodes
                x = center_x + radius_circle * (0.8 * (i % 3) - 0.8)
                y = center_y + radius_circle * (0.8 * (i // 3) - 0.8)
                node_pos[node] = (x, y)
                
                # Draw node
                self.wfg_canvas.create_oval(
                    x - radius, y - radius,
                    x + radius, y + radius,
                    fill="lightblue"
                )
                self.wfg_canvas.create_text(x, y, text=node)
        
        # Draw edges
        for src in graph:
            for dst in graph[src]:
                if src in node_pos and dst in node_pos:
                    x1, y1 = node_pos[src]
                    x2, y2 = node_pos[dst]
                    self.wfg_canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)

if __name__ == "__main__":
    root = tk.Tk()
    app = DeadlockDetectorApp(root)
    root.mainloop()
