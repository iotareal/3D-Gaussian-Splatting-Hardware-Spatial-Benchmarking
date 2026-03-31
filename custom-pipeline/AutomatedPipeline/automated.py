import subprocess
import sys
from pathlib import Path


GS_ROOT = Path("D:/Projects/3DGS/gaussian-splatting")

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

def train(dataset_path,output_path,iterations=30000,save_points=5000):
    # RUNS
    # python gaussian-splatting/train.py -s <path_to_dataset> -m <path_to_output_folder> --iterations 30000
    save_points = [str(i) for i in range(save_points, int(iterations) + 1) if i%save_points == 0]
    cmd = [
        sys.executable,  
        str(Path(GS_ROOT) / "train.py"),
        "-s", str(dataset_path),
        "-m", str(output_path),
        "--iterations", str(iterations),
        "--eval",
        "--save_iterations", save_points
    ]
    # FIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIX
    #FIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIX
    #FIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIXFIX
    cmd.extend(save_points)
    # cmd=f'python "{str(Path(GS_ROOT/"train.py"))}" -s "{str(dataset_path)}" -m "{str(output_path)}" --iterations "{str(iterations)}" --eval --save_iterations {save_points}'
    result = subprocess.run(cmd,shell=True)
    if result.returncode == 0:
        evaluate_model(output_path)

def launch_viewer(output_path,sibr_viewer):
    # RUNS
    # SIBR_gaussianViewer_app.exe -m <path_to_model>
    cmd=(str(sibr_viewer),"-m",str(output_path))
    subprocess.run(cmd,check=True)

def evaluate_model(output_path):
    
    print("\n--- Rendering Test Views for All Checkpoints ---")
    render_cmd = f'python "{str(Path(GS_ROOT / "render.py"))}" -m "{output_path}" --skip_train'
    subprocess.run(render_cmd, shell=True, check=True, cwd=str(GS_ROOT))
    
    print("\n--- Calculating PSNR/SSIM/LPIPS ---")
    metrics_cmd = f'python "{str(Path(GS_ROOT / "metrics.py"))}" -m "{output_path}"'
    subprocess.run(metrics_cmd, shell=True, check=True, cwd=str(GS_ROOT))