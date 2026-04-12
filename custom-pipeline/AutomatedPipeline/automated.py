import subprocess
import sys
import os
from pathlib import Path

from Benchmarking.training_time import BenchmarkTime
from Benchmarking.vram_monitor_util import VRAMMonitor

GS_ROOT = Path(os.getcwd()) /"gaussian-splatting"

def convert_point_cloud(dataset_path):
    # RUNS
    # python gaussian-splatting/convert.py -s <path_to_dataset>
    
    if(Path(dataset_path)/"sparse").is_dir():
        print("SfM data found. Skipping conversion operation")
        return
        
    cmd=f'python "{str(Path(GS_ROOT/"convert.py"))}" -s "{str(dataset_path)}"'
    try:
        subprocess.run(
            cmd, 
            shell=True, 
            check=True, 
            cwd=str(GS_ROOT) 
        )
        print("\nConversion Complete! Check your 'images' and 'sparse' folders.")
    except subprocess.CalledProcessError as e:
        print(f"\nPipeline failed to run COLMAP: {e}")

def train(dataset_path,output_path,filename,iterations=30000,checkpoints=5000):
    # RUNS
    # python gaussian-splatting/train.py -s <path_to_dataset> -m <path_to_output_folder> --iterations 30000

    # save_points = chkpt 1 chkpt 2 .... chkpt n
    checkpoints = list(str(i) for i in range(1,iterations) if i%checkpoints == 0)
    cmd = [
        sys.executable,  
        str(Path(GS_ROOT) / "train.py"),
        "-s", str(dataset_path),
        "-m", str(output_path),
        "--iterations", str(iterations),
        "--eval",
        "--save_iterations"
    ]
    cmd.extend(checkpoints)
    checkpoints.append(iterations)
    with BenchmarkTime(),(VRAMMonitor(filename) if filename else VRAMMonitor()):
        result = subprocess.run(cmd,shell=True)
    if result.returncode == 0:     
        evaluate_model(output_path,checkpoints)

def launch_viewer(output_path,sibr_viewer):
    # RUNS
    # SIBR_gaussianViewer_app.exe -m <path_to_model>
    cmd=(str(sibr_viewer),"-m",str(output_path))
    subprocess.run(cmd,check=True)

def evaluate_model(output_path,save_points):
    for checkpoint in save_points:
        print(f"\n--- Rendering Test Views for Checkpoint: {checkpoint} ---")
        # cmd = f'python "{str(Path(GS_ROOT / "render.py"))}" -m "{output_path}" --skip_train'
        eval_cmd = [
            sys.executable,
            str(Path(GS_ROOT / "render.py")),
            "-m",output_path,
            "--iteration",str(checkpoint),
            "--skip_train"
        ]
        subprocess.run(eval_cmd, shell=True)
        
    print(f"\n--- Calculating PSNR/SSIM/LPIPS for Checkpoint: {checkpoint} ---")
    # metrics_cmd = f'python "{str(Path(GS_ROOT / "metrics.py"))}" -m "{output_path}"'
    metrics_cmd = [
        sys.executable,
        str(Path(GS_ROOT / "metrics.py")),
        "-m",output_path
    ]
    subprocess.run(metrics_cmd, shell=True)