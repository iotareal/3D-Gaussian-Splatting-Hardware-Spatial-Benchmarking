from AutomatedPipeline import menus
from AutomatedPipeline import file_handler as fh
SIBR_APP__PATH_VARIABLE="sibr_viewer"
DATASET_PATH_VARIABLE="dataset_path"
OUTPUT_PATH_VARIABLE="output_path"
def main():
    data=fh.get_paths()
    fh.check_paths(data)
    menus.main_menu(data[DATASET_PATH_VARIABLE],data[OUTPUT_PATH_VARIABLE],data[SIBR_APP__PATH_VARIABLE])
    
if __name__=="__main__":
    main()