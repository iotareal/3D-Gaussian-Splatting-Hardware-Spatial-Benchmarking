from tkinter import filedialog
from pathlib import Path
import json
import tkinter as tk

from main import SIBR_APP__PATH_VARIABLE
from main import DATASET_PATH_VARIABLE
from main import OUTPUT_PATH_VARIABLE


def locate_dataset(custom_title="Locate \'dataset\' folder") -> str:
    root = tk.Tk()
    root.withdraw() 
    root.attributes('-topmost', True)
    
    path = filedialog.askdirectory(title=custom_title)
    root.destroy()
    print(f"Path located: {path}\nMake sure all images are in \"\input\" folder")
    store_paths(path,identifier=DATASET_PATH_VARIABLE)
    print(f"{DATASET_PATH_VARIABLE} saved to paths.json")
    

def locate_output(custom_title="Locate \'output\' folder") -> str:
    root = tk.Tk()
    root.withdraw() 
    root.attributes('-topmost', True)
    
    path = filedialog.askdirectory(title=custom_title)
    root.destroy()
    print(f"Path located: {path}\nOutput will be stored here")
    store_paths(path,identifier=OUTPUT_PATH_VARIABLE)
    print(f"{OUTPUT_PATH_VARIABLE} saved to paths.json")

def locate_SIBR(custom_title="Locate \'SIBR Viewer\' application") -> str:
    root = tk.Tk()
    root.withdraw() 
    root.attributes('-topmost', True)
    
    path = filedialog.askopenfilename(filetypes=[("Application", "*.exe")],title=custom_title)
    root.destroy()
    
    print(f"Path Located: {path}")
    store_paths(path,identifier=SIBR_APP__PATH_VARIABLE)
    print(f"{SIBR_APP__PATH_VARIABLE} saved to paths.json")


def get_paths():
    config_file = Path("custom-pipeline/paths.json")
    if config_file.exists():
        with open(config_file, "r") as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                data = {}

def store_paths(path,identifier:str):
    config_file = Path("custom-pipeline/paths.json")
    data = get_paths()
    
    data[identifier] = path
    
    if not config_file.exists():
        with open(config_file, "x") as f:
            pass
        
    with open(config_file, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"{identifier} = {path} Saved Successfully to paths.json")
            
def check_paths(data:dict):
    path_variables=data.keys()
    if DATASET_PATH_VARIABLE not in path_variables:
        locate_dataset(custom_title="Dataset path not found please locate dataset folder")
    if OUTPUT_PATH_VARIABLE not in path_variables:
        locate_output(custom_title="output path not found please locate output/<model_name> folder")
    if SIBR_APP__PATH_VARIABLE not in path_variables:
        locate_SIBR(custom_title="Path to SIBR app not found please locate SIBR viewer Application")