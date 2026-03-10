import subprocess
from datetime import datetime 
import os
from pathlib import Path

class VRAMMonitor:
    def __init__(self):
        log_path = Path(f"custom-pipeline/Benchmarking/VRAM logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv")
    
        os.makedirs(log_path.parent, exist_ok=True)
    
        if not log_path.exists():
            with open(log_path, 'x') as f:
                pass
            
        self.log_name = str(log_path) 
        self.process = None

    def __enter__(self):
        # Start nvidia-smi as a background process
        # It queries timestamp and used memory every 1 second (-l 1)
        self.file_handle = open(self.log_name, "a", buffering=1)
        self.process = subprocess.Popen([
        "nvidia-smi", 
        "--query-gpu=timestamp,memory.used", 
        "--format=csv", "-l", "1"
        ], stdout=self.file_handle, stderr=subprocess.STDOUT)
    
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.process:
            self.process.terminate()
            self.process.wait() # Wait for it to shut down cleanly
    
        if self.file_handle:
            self.file_handle.close() # This forces the final 'flush' to disk
            
        print(f"VRAM log finalized: {self.log_name}")
