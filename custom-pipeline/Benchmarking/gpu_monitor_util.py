import os
import csv
import time
import subprocess
import threading
from pathlib import Path
from datetime import datetime


class GPUMonitor:
    def __init__(self,filename):
        self.log_path = Path(__file__).parent / "GPU_logs" / f"{filename}.csv"
        os.makedirs(self.log_path.parent, exist_ok=True)
        print(f"----   Now Logging: {filename}.csv   ----")
    
        if not self.log_path.exists():
            with open(self.log_path, 'x') as f:
                pass
        
        self.log_name = str(self.log_path) 
        self.is_running = False
        self.thread = None
        self.start_time = None

    def __enter__(self):
        self.is_running = True
        self.start_time = time.time()
        
        self.thread = threading.Thread(target=self._log_loop)
        self.thread.start()
        
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.is_running = False 
        if self.thread:
            self.thread.join()
            
        if exc_type is not None:
            self.__delete_log()
            print(f"GPU log: '{self.log_name}' has been deleted due to failed run")
            return
            
        print(f"VRAM log finalized: {self.log_name}")
        
    def __delete_log(self):
        self.log_path.unlink(missing_ok=True)

    def _log_loop(self):
        with open(self.log_name, 'w', newline='') as f:
            writer = csv.writer(f)
            
            writer.writerow(["Time_Minutes", "Memory_Used_MiB", "GPU_Utilization_Pct", "Power_Watts"])
            
            while self.is_running:
                # 2. Calculate relative time in minutes
                elapsed_mins = (time.time() - self.start_time) / 60.0
                
                # 3. Ask NVIDIA for pure numbers (no headers, no units)
                cmd = [
                    "nvidia-smi", 
                    "--query-gpu=memory.used,utilization.gpu,power.draw", 
                    "--format=csv,noheader,nounits"
                ]
                
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    # Split the output "12050, 98, 215" into a list
                    data = result.stdout.strip().split(', ')
                    
                    if len(data) == 3:
                        # 4. Write the row: [0.0167, 12050, 98, 215]
                        writer.writerow([f"{elapsed_mins:.4f}", data[0], data[1], data[2]])
                        
                        # Force Python to save to disk immediately! 
                        # This lets you open the CSV live while training to check on it.
                        f.flush() 
                        
                except subprocess.CalledProcessError:
                    pass # Ignore microsecond errors if nvidia-smi is busy
                    
                time.sleep(1) # Wait 1 second before polling again