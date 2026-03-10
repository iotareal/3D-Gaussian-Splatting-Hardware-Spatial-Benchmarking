import subprocess
from pathlib import Path
def convert_point_cloud(dataset_path):
    # RUNS
    # python gaussian-splatting/convert.py -s <path_to_dataset>
    
    if(Path(dataset_path)/"sparse").is_dir():
        print("SfM data found. Skipping conversion operation")
        return
        
    cmd=("python","gaussian-splatting/convert.py","-s",str(dataset_path))
    subprocess.run(cmd,check=True)

def train(dataset_path,output_path,iterations=30000):
    # RUNS
    # python gaussian-splatting/train.py -s <path_to_dataset> -m <path_to_output_folder> --iterations 30000
    cmd=("python","gaussian-splatting/train.py", "-s", str(dataset_path), "-m",str(output_path), "--iterations",str(iterations))
    subprocess.run(cmd,check=True)

def launch_viewer(output_path,sibr_viewer):
    # RUNS
    # SIBR_gaussianViewer_app.exe -m <path_to_model>
    cmd=(str(sibr_viewer),"-m",str(output_path))
    subprocess.run(cmd,check=True)
