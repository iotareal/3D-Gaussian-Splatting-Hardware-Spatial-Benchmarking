import argparse

from AutomatedPipeline import menus

def main():
    parser = argparse.ArgumentParser(description="3DGS Tkinter disabler")
    parser.add_argument("--ssh",action="store_true",help="Disables tkinter filedialogs")
    args = parser.parse_args()    
    menus.main_menu(is_ssh=args.ssh)
    
    
if __name__=="__main__":
    main()