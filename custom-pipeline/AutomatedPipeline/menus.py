from AutomatedPipeline import automated as auto
from AutomatedPipeline import file_handler as fh
from Benchmarking.training_time import BenchmarkTime
from Benchmarking.vram_monitor_util import VRAMMonitor
def locate_paths_menu():
    # user "locate" contains
    # 1. dataset
    # 2. output
    # 3. SIBR viewer app
    # 4. back to main menu
    while(True):
        inputs=(1,2,3,4)
        print("""
            Please select one:
            1. Locate Dataset Folder
            2. Locate Output Folder
            3. Locate SIBR Viewer app
            4: Back to main menu
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
        
        elif choice==2:
            fh.locate_output()
        
        elif choice==3:
            fh.locate_SIBR()
        
        elif choice==4:
            return
        
        else:
            pass    
        
def main_menu(dataset_path,output_path,sibr_viewer):
    # user menu contains
    # 1. convert dataset to point cloud
    # 2. train the model
    # 3. launch SIRB viewer
    # 4. locate dataset, output or SIBR viewer
    # 5. exit
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
            auto.convert_point_cloud(dataset_path)
            
        
        elif choice==2:
            iterations=0
            try:
                iterations=int(input("Iterations?(default=30'000): "))
            except ValueError:
                iterations=30000
            with BenchmarkTime(),VRAMMonitor():
                auto.train(dataset_path,output_path,iterations)
            
        
        elif choice==3:
            auto.launch_viewer(output_path,sibr_viewer)
        
        elif choice==4:
            locate_paths_menu()
        
        elif choice==5:
            return 0
        
        else:
            pass