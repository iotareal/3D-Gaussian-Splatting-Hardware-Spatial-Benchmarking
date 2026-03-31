from AutomatedPipeline import automated as auto
from AutomatedPipeline import file_handler as fh
from Benchmarking.training_time import BenchmarkTime
from Benchmarking.vram_monitor_util import VRAMMonitor

from AutomatedPipeline.file_handler import DATASET_PATH_LABEL
from AutomatedPipeline.file_handler import SIBR_APP__PATH_LABEL
from AutomatedPipeline.file_handler import OUTPUT_PATH_LABEL

# Path variables

SIBR_APP__PATH_VARIABLE = None
DATASET_PATH_VARIABLE = None
OUTPUT_PATH_VARIABLE = None

def get_json_paths():
    data=fh.get_paths()
    fh.check_paths(data)
    global SIBR_APP__PATH_VARIABLE
    global DATASET_PATH_VARIABLE
    global OUTPUT_PATH_VARIABLE
    
    SIBR_APP__PATH_VARIABLE = data[SIBR_APP__PATH_LABEL]
    DATASET_PATH_VARIABLE = data[DATASET_PATH_LABEL]
    OUTPUT_PATH_VARIABLE = data[OUTPUT_PATH_LABEL]
    
    # print(f"[DEBUG]: {SIBR_APP__PATH_VARIABLE}")
    # print(f"[DEBUG]: {DATASET_PATH_VARIABLE}")
    # print(f"[DEBUG]: {OUTPUT_PATH_VARIABLE}")


def locate_paths_menu():
    # user "locate" contains
    # 1. dataset
    # 2. output
    # 3. SIBR viewer app
    # 4. back to main menu
    while(True):
        inputs=(1,2,3,4,5)
        print("""
            Please select one:
            1. Locate Dataset Folder
            2. Locate Output Folder
            3. Locate SIBR Viewer app
            4: Show current paths
            5: Back to main menu
        """)
        try:
            choice = int(input("Enter Choice: "))
        except ValueError:
            print("Please enter Valid Choice")
            continue
        if choice not in inputs:
            continue
        
        elif choice==1:
            fh.locate_dataset()
            get_json_paths()
        
        elif choice==2:
            fh.locate_output()
            get_json_paths()
        
        elif choice==3:
            fh.locate_SIBR()
            get_json_paths()
        
        elif choice==4:
            print(f"OUTPUT FOLDER: {OUTPUT_PATH_VARIABLE}")
            print(f"DATASET FOLDER: {DATASET_PATH_VARIABLE}")
            print(f"SIBR FOLDER: {SIBR_APP__PATH_VARIABLE}")
            
        elif choice == 5:
            return
        else:
            pass    
        
def main_menu():
    # user menu contains
    # 1. convert dataset to point cloud
    # 2. train the model
    # 3. launch SIRB viewer
    # 4. locate dataset, output or SIBR viewer
    # 5. exit
    get_json_paths()
    while(True):
        inputs=(1,2,3,4,5)
        print("""
            3DGS custom-pipeline main menu
            1. Convert dataset to point cloud
            2. Train the model
            3. Launch SIRB viewer
            4. Locate dataset, output or SIBR viewer
            5. exit
            """)
        
        try:
            choice = int(input("Enter Choice: "))
        except ValueError:
            print("Please enter Valid Choice")
            continue
        
        if choice not in inputs:
            continue
        
        if choice==1:
            auto.convert_point_cloud(DATASET_PATH_VARIABLE)
            
        
        elif choice==2:
            iterations=0
            filename=None
            try:
                iterations=int(input("Iterations?(default=30,000): "))
                
            except Exception:
                print("Invalid Value entered: iterations is set to default 30,000 ")
                iterations=30000
            try:
                savePoints=int(input("Checkpoints(default=5,000): "))
            except Exception:
                print("Invalid Value entered: Checkpoints will be saved to default 5,000 ")
                savePoints=5,000
            
            filename = input("Enter the name of CSV file record(default=current_timestamp): ")
            with BenchmarkTime(),(VRAMMonitor(filename) if filename else VRAMMonitor()):
                auto.train(DATASET_PATH_VARIABLE,OUTPUT_PATH_VARIABLE,iterations,savePoints)
            
        
        elif choice==3:
            auto.launch_viewer(OUTPUT_PATH_VARIABLE,SIBR_APP__PATH_VARIABLE)
        
        elif choice==4:
            locate_paths_menu()
        
        elif choice==5:
            return 0
        
        else:
            pass