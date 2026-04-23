from AutomatedPipeline import automated as auto
from AutomatedPipeline import file_handler as fh


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
        
        elif choice==2:
            fh.locate_output()
        
        elif choice==3:
            fh.locate_SIBR()
        
        elif choice==4:
            print(f"DATASET FOLDER: {fh.get_dataset()}")
            print(f"OUTPUT FOLDER: {fh.get_output()}")
            print(f"SIBR FOLDER: {fh.get_sibr()}")
            
        elif choice == 5:
            fh.save_paths()
            return
        else:
            pass    
        
def main_menu():
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
            auto.convert_point_cloud(fh.get_dataset())
            
        
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
                savePoints=5000
            
            try:
                resolution = int(input("Specify build resolution(leave empty if you don't know what it does): "))
            except Exception:
                resolution = None
            auto.train(fh.get_dataset(),fh.get_output(),iterations,savePoints,resolution)
            
        
        elif choice==3:
            auto.launch_viewer(fh.get_output(),fh.get_sibr())
        
        elif choice==4:
            locate_paths_menu()
        
        elif choice==5:
            return 0
        
        else:
            pass