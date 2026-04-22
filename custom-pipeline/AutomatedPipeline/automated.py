import subprocess
import sys
from pathlib import Path

from Benchmarking.gpu_monitor_util import GPUMonitor
from AutomatedPipeline.file_handler import convert_metrics

IS_WINDOWS = sys.platform.startswith('win')

GS_ROOT = Path.cwd() / "gaussian-splatting"
CONVERT_PY = GS_ROOT / "convert.py"
TRAIN_PY = GS_ROOT / "train.py"
RENDER_PY = GS_ROOT / "render.py"
METRICS_PY = GS_ROOT / "metrics.py"

def convert_point_cloud(dataset_path):
    # For preprocessing only
    
    if(Path(dataset_path)/"sparse").is_dir():
        print("Dataset is already preprocessed.")
        return
        
    cmd=[
        sys.executable, 
        str(CONVERT_PY),
        "-s",
        str(dataset_path)
    ]
    
    try:
        if IS_WINDOWS:
            subprocess.run(cmd,shell=True)
            print("Conversion Complete")
        else:
            print("")
    except subprocess.CalledProcessError as e:
        print(f"Pipeline failed to run COLMAP: {e}")

def train(dataset_path,output_path,filename,iterations=30000,checkpoints=6,resolution = None):
    
    checkpoints = list(str(i) for i in range(1,iterations) if i % (iterations/checkpoints) == 0)
    cmd = [
        sys.executable,  
        str(TRAIN_PY),
        "-s", str(dataset_path),
        "-m", str(output_path),
        "--iterations", str(iterations),
        "--eval",
    ]
    
    cmd.append("--save_iterations")
    cmd.extend(checkpoints)
    
    cmd.append("--test_iterations")
    cmd.extend(checkpoints)
    
    if resolution:
        cmd.extend(["--resolution",str(resolution)])
    checkpoints.append(iterations)
    try:
        with (GPUMonitor(filename) if filename else GPUMonitor()):
            if IS_WINDOWS:
                result = subprocess.run(cmd,shell=True)
            else:
                result = subprocess.run(cmd)
            
    except subprocess.CalledProcessError as e:
            
            if e.returncode == -9:
                print("ERROR: Ran out of Video Memory")
            else:
                print(f"Training Crashed! The 3DGS script returned error code: {e.returncode}")

    except KeyboardInterrupt:
            print("Training manually aborted.")
            print("Returning to main menu...")

    except PermissionError:
            print(" Permission Denied! system blocked execution.")

    except Exception as e:
            print(f"An unexpected system error occurred: {e}")
    
    if result.returncode == 0:     
            evaluate_model(output_path,checkpoints)
    

def launch_viewer(output_path,sibr_viewer):
    if not IS_WINDOWS:
        print("Current System is not windows")
        return
    cmd=[
        str(sibr_viewer),
        "-m", str(output_path)
    ]
    
    subprocess.run(cmd,check=True)

def evaluate_model(output_path,save_points):
    for checkpoint in save_points:
        print(f"\n--- Rendering Test Views for Checkpoint: {checkpoint} ---")
        eval_cmd = [
            sys.executable,
            str(RENDER_PY),
            "-m", str(output_path),
            "--iteration",str(checkpoint),
            "--skip_train"
        ]
        subprocess.run(eval_cmd, shell=True)
        
    print(f"\n--- Calculating PSNR/SSIM/LPIPS for Checkpoint: {checkpoint} ---")
    metrics_cmd = [
        sys.executable,
        str(METRICS_PY),
        "-m", str(output_path)
    ]
    subprocess.run(metrics_cmd, shell=True)
    convert_metrics()