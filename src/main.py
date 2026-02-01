import os
import shutil
from pathlib import Path

def copy_files_to_dir(source, destination):
    print(f"Entering {source}")
    if os.path.isdir(source):
        dir_contents = os.listdir(source)
        print(f"directory contents: {dir_contents}")

        for dir_item in dir_contents:
            #check if in dest, if not create it
            print(f"Analyzing {dir_item}...")
            source_item = os.path.join(source, dir_item)
            dest_item  = os.path.join(destination, dir_item)

            if os.path.exists(dest_item):
                print(f"{dest_item} already exists")
                continue

            if os.path.isdir(source_item):
                print(f"{dir_item} is a folder")
                #create the folder
                os.mkdir(dest_item)
                #go to the folder and check if it has any files
                copy_files_to_dir(
                    os.path.join(source, dir_item), 
                    os.path.join(destination, dir_item)
                )

            elif os.path.isfile(source_item):
                print(f"{dir_item} is a file")
                print(f"Copying {source_item} to {destination}")
                shutil.copy(source_item,destination)
                

def main():
    try:
        current_dir = os.getcwd()
        print(f"The current working directory is: {current_dir}")
        source = os.path.join(current_dir, "static")
        destination = os.path.join(current_dir, "public")

        if not os.path.isdir(source):
            raise Exception("The source path does not exist")
        
        print(f"Deleting all contents of {destination}")
        
        if os.path.exists(destination):
            shutil.rmtree(os.path.join(destination))
    
        if not os.path.exists(destination):
            os.mkdir(destination)

        print(f"Copying files from {source} to {destination}")

        copy_files_to_dir(source, destination)
    except Exception as e:
        print(e)
        


main()