from pathlib import Path
class LocalPaths:
    __not_set = "Not set"
    def __init__(self,dataset_folder=None,output_folder=None,sibr_app=None):
        self.dataset_folder = dataset_folder
        self.output_folder = output_folder
        self.sibr_app = sibr_app
        
    def __str__(self):
        return f"""
    Dataset Folder: {self.dataset_folder if self.dataset_folder else self.__not_set}
    Output Folder: {self.output_folder if self.output_folder else self.__not_set}
    SIBR Viewer Application: {self.sibr_app if self.sibr_app else self.__not_set}
    """
    
    def get_dataset_path(self):
        return Path(self.dataset_folder) if self.dataset_folder else self.__not_set
    
    def get_output_path(self):
        return Path(self.output_folder) if self.output_folder else self.__not_set
    
    def get_sibr_path(self):
        return Path(self.sibr_app) if self.sibr_app else self.__not_set
    