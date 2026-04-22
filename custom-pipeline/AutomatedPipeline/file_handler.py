from AutomatedPipeline.local_paths import LocalPaths

from tkinter import filedialog
from pathlib import Path
import tkinter as tk
import pandas as pd
import sys
import json
import pickle

IS_WINDOWS = sys.platform.startswith('win')

def __get_paths() -> LocalPaths:
    config_file = Path.cwd() / "custom-pipeline" / "path_state.pkl"
    if not config_file.exists():
        with open(config_file,'x'):
            pass
    
    with open(config_file,"rb") as file:
        try:
            return pickle.load(file)
        except EOFError:
            print("\n--- New Environment detected: You may need to specify directories ---")
            return LocalPaths()
        
#Initializing Paths
LOADED_PATHS = __get_paths()

def locate_dataset(custom_title="Locate \'dataset\' folder"):
    root = tk.Tk()
    root.withdraw() 
    root.attributes('-topmost', True)
    
    path = filedialog.askdirectory(title=custom_title,initialdir=Path.cwd())
    root.destroy()
    
    if not path:
        print("You did not selected any path for dataset, path left unchanged")
        return
    
    LOADED_PATHS.dataset_folder = Path(path)
    print(f"Path saved: {LOADED_PATHS.get_dataset_path()}")
    
def get_dataset():
    return LOADED_PATHS.get_dataset_path()

def locate_output(custom_title="Locate \'output\' folder") -> str:
    root = tk.Tk()
    root.withdraw() 
    root.attributes('-topmost', True)
    
    path = filedialog.askdirectory(title=custom_title,initialdir=Path.cwd())
    root.destroy()
    
    if not path:
        print("You did not selected any path for output, path left unchanged")
        return
    
    LOADED_PATHS.output_folder = Path(path)
    print(f"Path saved: {LOADED_PATHS.get_output_path()}")
    
def get_output():
    return LOADED_PATHS.get_output_path()

def locate_SIBR(custom_title="Locate \'SIBR Viewer\' application") -> str:
    root = tk.Tk()
    root.withdraw() 
    root.attributes('-topmost', True)
    
    path = filedialog.askopenfilename(filetypes=[("Application", "*.exe")],title=custom_title,initialdir=Path.cwd())
    root.destroy()
    
    if not path:
        print("You did not selected any path for SIBR viewer, path left unchanged")
        return
    
    LOADED_PATHS.sibr_app = Path(path)
    print(f"Path saved: {LOADED_PATHS.get_sibr_path()}")

def get_sibr():
    return LOADED_PATHS.get_sibr_path()

def save_paths():
    config_file = Path.cwd() / "custom-pipeline" / "path_state.pkl"
    
    with open(config_file,'wb') as file:
        pickle.dump(LOADED_PATHS,file)
        print("Paths saved to \'path_state.pkl\'.")

def convert_metrics():
    json_path = Path(get_output()) / "results.json"
    csv = Path(__file__).parent.parent /"Benchmarking"/"GPU_logs"/ f"results_{str(get_output().name)}.csv"
    
    if not json_path.exists():
        print("results.json is not found for this output")
        return
    try:
        with open(json_path, 'r') as f:
            data = dict(json.load(f))
        
        cleaned_data = [["Iterations","SSIM","PSNR","LPIPS"]]
        cleaned_data.extend( [key.replace("ours_",""), metrics["SSIM"], metrics["PSNR"], metrics["LPIPS"]] for key,metrics in data.items() )
        df = pd.DataFrame(cleaned_data[1:],columns=cleaned_data[0])
        df.to_csv(csv,index=False)
        
        print(f"Saved {csv.name} to {Path(csv).parent.name}")
    except FileNotFoundError:
        print(f"Error: Could not find '{csv}'")

def begin_setup():
    locate_dataset()
    locate_output()
    if IS_WINDOWS:
        locate_SIBR()
    save_paths()

if not LOADED_PATHS:
    begin_setup()
