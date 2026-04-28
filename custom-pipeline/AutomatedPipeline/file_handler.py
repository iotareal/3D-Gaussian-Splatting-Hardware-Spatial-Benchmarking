from AutomatedPipeline.local_paths import LocalPaths

from tkinter import filedialog
from pathlib import Path
import tkinter as tk
import pandas as pd
import sys
import json
import pickle

IS_WINDOWS = sys.platform.startswith('win')
CONFIG_FILE = Path(__file__) .parent.parent / "path_state.pkl"

def __get_paths() -> LocalPaths:
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE,'x'):
            pass
    
    with open(CONFIG_FILE,"rb") as file:
        try:
            return pickle.load(file)
        except EOFError:
            print("\n--- New Environment detected: You may need to specify directories ---")
            return LocalPaths()
        
#Initializing Paths
LOADED_PATHS = __get_paths()

def locate_dataset(is_ssh,custom_title="Locate \'dataset\' folder"):
    path = None
    if is_ssh:
        path = input("Enter absolute path to dataset folder: ").strip('\'" ')
        if not path:
            print("You did not select any dataset folder")
            return
        else:
            path = Path(path)
        if not path.exists():
            print("Error: dataset folder does not exist, please check the path again")
            return
    else:
        root = tk.Tk()
        root.withdraw() 
        root.attributes('-topmost', True)
        initdir = Path(__file__) .parent.parent.parent / "dataset"
        if not initdir.exists():
            initdir = Path(__file__) .parent.parent.parent
        path = filedialog.askdirectory(title=custom_title,initialdir=initdir)
        root.destroy()
    
    if not path or str(path) == ".":
        print("You did not selected any path for dataset, path left unchanged")
        return
    
    LOADED_PATHS.dataset_folder = Path(path)
    print(f"Path saved: {LOADED_PATHS.get_dataset_path()}")
    
def get_dataset():
    return LOADED_PATHS.get_dataset_path()

def locate_output(is_ssh,custom_title="Locate \'output\' folder") -> str:
    path = None
    if is_ssh:
        path = input("Enter absolute path to output folder: ").strip('\'" ')
        if not path:
            print("You did not select any output folder")
            return
        else:
            path = Path(path)
            if not path.parent.exists():
                print("output folder does not exists")
            if not path.exists():
                path.mkdir(parents=True,exist_ok=True)
                print(f"created directory for {path.name}")
    else:
        root = tk.Tk()
        root.withdraw() 
        root.attributes('-topmost', True)
        
        initdir = Path(__file__) .parent.parent.parent / "output"
        if not initdir.exists():
            initdir = Path(__file__) .parent.parent.parent
        path = filedialog.askdirectory(title=custom_title,initialdir=initdir)
        root.destroy()
    
    if not path or str(path) == ".":
        print("You did not selected any path for output, path left unchanged")
        return
    
    LOADED_PATHS.output_folder = Path(path)
    print(f"Path saved: {LOADED_PATHS.get_output_path()}")
    
def get_output():
    return LOADED_PATHS.get_output_path()

def locate_SIBR(is_ssh,custom_title="Locate \'SIBR Viewer\' application"):
    if is_ssh:
        print("Running Pipeline via SSH cannot use SIBR viewer")
        return
        
    root = tk.Tk()
    root.withdraw() 
    root.attributes('-topmost', True)
    initdir = Path(__file__) .parent.parent.parent / "viewers"
    if not initdir.exists():
        initdir = Path(__file__) .parent.parent.parent
    path = filedialog.askopenfilename(filetypes=[("Application", "*.exe")],title=custom_title,initialdir=initdir)
    root.destroy()
    
    if not path or str(path) == ".":
        print("You did not selected any path for SIBR viewer, path left unchanged")
        return
    
    LOADED_PATHS.sibr_app = Path(path)
    print(f"Path saved: {LOADED_PATHS.get_sibr_path()}")

def get_sibr():
    return LOADED_PATHS.get_sibr_path()

def save_paths():
    
    with open(CONFIG_FILE,'wb') as file:
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
