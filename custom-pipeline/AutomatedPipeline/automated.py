import subprocess
import sys
import time
from pathlib import Path

from Benchmarking.gpu_monitor_util import GPUMonitor
from AutomatedPipeline.file_handler import convert_metrics

IS_WINDOWS = sys.platform.startswith('win')

GS_ROOT = Path(__file__).parent.parent.parent / "gaussian-splatting"
CONVERT_PY = GS_ROOT / "convert.py"
TRAIN_PY = GS_ROOT / "train.py"
RENDER_PY = GS_ROOT / "render.py"
METRICS_PY = GS_ROOT / "metrics.py"

def convert_point_cloud(dataset_path):
    # For preprocessing only
    if not IS_WINDOWS:
        print("Colmap preprocessing is available for Windows only")
        return
    
    if not Path(dataset_path).exists():
        print("Cannot find dataset at specified location, need to select dataset again")
        return
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
        subprocess.run(cmd,shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Pipeline failed to run COLMAP: {e}")

def train(dataset_path,output_path,iterations=30000,checkpoints=5000,resolution = None):
    if not Path(dataset_path).exists():
        print("Cannot find dataset at specified location, need to select dataset again")
        return
    if not Path(output_path).exists():
        print("Cannot find output at specified location, need to select output folder again")
        return
    checkpoints = list(str(i) for i in range(checkpoints,iterations,checkpoints))
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
        with GPUMonitor(str(output_path.name)):
            process = subprocess.Popen(
                cmd,
                shell=IS_WINDOWS,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True
            )

            last_line = 0
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break 

                if line:
                    current_time = time.time()
                    if current_time - last_line >= 60:
                        print(line.strip())
                        last_line = current_time

                    if "<" in line and "it/s" in line:
                        try:
                            eta_str = line.split("<")[1].split(",")[0].strip()
                            
                            parts = eta_str.split(":")
                            
                            hours = 0
                            minutes = 0
                            seconds = 0
                            if len(parts) == 3:
                                hours = int(parts[0])
                                minutes = int(parts[1])
                                seconds = int(parts[2])
                            
                            elif len(parts) == 2:
                                minutes = int(parts[0])
                                seconds = int(parts[1])
                            
                            elif len(parts) == 1:
                                seconds = int(parts[0])
                                
                            kill_time = hours + (minutes/60) + (seconds/3600)
                            limit = 3
                            if kill_time >= limit:
                                print(f"ETA ({eta_str}) exceeded from {limit} hours to {kill_time:.2f}, Training Aborted")
                                process.kill() # Terminate the subprocess
                                raise KeyboardInterrupt # Trigger your __exit__ 'exceeded' logic!
                        except Exception:
                            pass

            if process.returncode != 0 and process.returncode is not None:
                # We manually trigger the error so your __exit__ can rename it to "oom_"
                raise subprocess.CalledProcessError(process.returncode, cmd)
            
    except subprocess.CalledProcessError as e:
            
            if e.returncode == -9:
                print("ERROR: Ran out of Video Memory")
            else:
                print(f"Training Crashed! The 3DGS script returned error code: {e.returncode}")
                return

    except KeyboardInterrupt:
            print("Returning to main menu...")
            return

    except PermissionError:
            print(" Permission Denied! system blocked execution.")
            return

    except Exception as e:
            print(f"An unexpected system error occurred: {e}")
            return
    
    if process.returncode == 0:     
            evaluate_model(output_path,checkpoints)
    

def launch_viewer(is_ssh,output_path,sibr_viewer):
    if not IS_WINDOWS:
        print("SIBR viewer is only available in Windows")
        return
    
    if is_ssh:
        print("Running Pipeline via SSH cannot use SIBR viewer")
        return
    
    if not Path(sibr_viewer).exists():
        print("Cannot find SIBR viewer at specified location, need to select SIBR viewer application again")
        return
    cmd=[
        str(sibr_viewer),
        "-m", str(output_path)
    ]
    
    subprocess.run(cmd,check=True,shell=True)

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
        subprocess.run(eval_cmd, shell=IS_WINDOWS, check=True)
        
    print(f"\n--- Calculating PSNR/SSIM/LPIPS for Checkpoint: {checkpoint} ---")
    metrics_cmd = [
        sys.executable,
        str(METRICS_PY),
        "-m", str(output_path)
    ]
    subprocess.run(metrics_cmd, shell=IS_WINDOWS, check=True)
    convert_metrics()