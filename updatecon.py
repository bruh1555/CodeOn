import os
from pathlib import Path
import requests
import shutil
import sys

def create_file_from_url(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "w") as file:
            file.write(response.text)
        print(f"Finished writing {file_path}.")
    else:
        raise Exception(f"Failed to fetch {url}")

def main():
    current_script_path = Path(__file__).resolve()
    new_script_name = "updatecon2.py"
    new_script_path = current_script_path.parent / new_script_name

    print(f"Renaming the script to {new_script_name}...")
    os.rename(current_script_path, new_script_path)
    print(f"Script renamed to {new_script_name}.")

    print("Creating guftemp folder...")
    guftemp_path = current_script_path.parent / "guftemp"
    os.makedirs(guftemp_path, exist_ok=True)
    print("Created guftemp folder.")

    files_to_create = [
        ("https://raw.githubusercontent.com/bruh1555/CodeOn/main/CodeOn%20for%20windows.py", "CodeOn for windows.py"),
        ("https://raw.githubusercontent.com/bruh1555/CodeOn/main/CodeOn%20for%20windows%20file%20runner.py", "CodeOn for windows file runner.py"),
        ("https://raw.githubusercontent.com/bruh1555/CodeOn/main/updatecon.py", "updatecon.py"),
        ("https://raw.githubusercontent.com/bruh1555/CodeOn/main/gnv.py", "gnv.py"),
        ("https://raw.githubusercontent.com/bruh1555/CodeOn/main/LICENSE", "LICENSE"),
        ("https://raw.githubusercontent.com/bruh1555/CodeOn/main/checkinternet.py", "checkinternet.py")
    ]

    for url, filename in files_to_create:
        try:
            create_file_from_url(url, guftemp_path / filename)
        except Exception as e:
            print(e)
            shutil.rmtree(guftemp_path)
            sys.exit()

    print("All files created in guftemp.")

    print("Deleting old files...")
    current_directory = current_script_path.parent
    for fileordirectory in current_directory.iterdir():
        if fileordirectory.name not in {new_script_name, "guftemp"}:
            if fileordirectory.is_dir():
                shutil.rmtree(fileordirectory)
            else:
                fileordirectory.unlink()
    print("Finished deleting old files.")

    print("Moving files from guftemp to parent directory...")
    for fileordirectory2 in guftemp_path.iterdir():
        shutil.move(str(fileordirectory2), current_directory / fileordirectory2.name)
    print("Finished moving files.")

    print("Deleting guftemp folder...")
    shutil.rmtree(guftemp_path)
    print("Deleted guftemp folder.")

    print("Completed updates!")
    print("Deleting self...")
    os.remove(new_script_path)

if __name__ == "__main__":
    main()
