import os
from pathlib import Path
import requests
import shutil
import sys
import time


print("Creating guftemp folder...")
guftemp_path = os.path.join(Path(__file__).resolve().parent, "guftemp")
os.makedirs(guftemp_path, exist_ok=True)
print("Created guftemp folder.")
print("Creating CodeOn file...")
codeonresponse = requests.get("https://raw.githubusercontent.com/bruh1555/CodeOn/main/CodeOn%20for%20windows.py")
if codeonresponse.status_code == 200:
    codeoncontents = codeonresponse.text
    codeonupdatefile_path = os.path.join(guftemp_path, "CodeOn for windows.py")
    with open(codeonupdatefile_path, "w") as codeonupdatefileopened:
        codeonupdatefileopened.write(codeoncontents)
    print("Finished writing CodeOn file.")
    print("Creating file runner file...")
    codeonfilerunnerresponse = requests.get("https://raw.githubusercontent.com/bruh1555/CodeOn/main/CodeOn%20for%20windows%20file%20runner.py")
    if codeonfilerunnerresponse.status_code == 200:
        codeonfilerunnercontents = codeonfilerunnerresponse.text
        codeonfilerunnerupdatefile_path = os.path.join(guftemp_path, "CodeOn for windows file runner.py")
        with open(codeonfilerunnerupdatefile_path, "w") as codeonfilerunnerupdatefileopened:
            codeonfilerunnerupdatefileopened.write(codeonfilerunnercontents)
        print("Finished writing CodeOn file runner file.")
        print("Creating update CodeOn file...")
        updateconfileresponse = requests.get("https://raw.githubusercontent.com/bruh1555/CodeOn/main/updatecon.py")
        if updateconfileresponse.status_code == 200:
            updateconfilecontents = updateconfileresponse.text
            updateconfile_path = os.path.join(guftemp_path, "updatecon.py")
            with open(updateconfile_path, "w") as updateconfileopened:
                updateconfileopened.write(updateconfilecontents)
            print("Finished writing update CodeOn file.")
            print("Creating gnv file...")
            gnvfileresponse = requests.get("https://raw.githubusercontent.com/bruh1555/CodeOn/main/gnv.py")
            if gnvfileresponse.status_code == 200:
                gnvfilecontents = gnvfileresponse.text
                gnvfile_path = os.path.join(guftemp_path, "gnv.py")
                with open(gnvfile_path, "w") as gnvfileopened:
                    gnvfileopened.write(gnvfilecontents)
                print("Finished writing gnv file.")
                print("Creating LICENSE file...")
                LICENSEfileresponse = requests.get("https://raw.githubusercontent.com/bruh1555/CodeOn/main/LICENSE")
                if LICENSEfileresponse.status_code == 200:
                    LICENSEfilecontents = LICENSEfileresponse.text
                    LICENSEfile_path = os.path.join(guftemp_path, "LICENSE")
                    with open(LICENSEfile_path, "w") as LICENSEfileopened:
                        LICENSEfileopened.write(LICENSEfilecontents)
                    print("Finished writing LICENSE file.")
                    print("Deleting old files...")
                    filesanddirectories = Path(__file__).resolve().parent.iterdir()
                    for fileordirectory in filesanddirectories:
                        if not fileordirectory.name == "updatecon.py" or fileordirectory.name == "guftemp":
                            if fileordirectory.is_dir():
                                shutil.rmtree(fileordirectory)
                            else:
                                fileordirectory.unlink()
                    print("Finished deleting old files.")
                    print("Putting guftemp folder's contents in parent directory...")
                    filesanddirectories2 = Path(__file__).resolve().parent / "guftemp".iterdir()
                    for fileordirectory2 in filesanddirectories2:
                        shutil.move(fileordirectory, Path(__file__).resolve().parent / fileordirectory2.name)
                    print("Finished changing files locations.")
                    time.sleep(2)
                    os.system('cls')
                    print("Completed updates!")
                    print("Deleting self...")
                    os.system(f"cmd /c del {Path(__file__).resolve()} /Q")
                else:
                    print("Failed to create LICENSE file. Please reload CodeOn to complete updates.")
                    shutil.rmtree(guftemp_path)
                    sys.exit()
            else:
                print("Failed to create gnv file. Please reload CodeOn to complete updates.")
                shutil.rmtree(guftemp_path)
                sys.exit()
        else:
            print("Failed to create update CodeOn file. Please reload CodeOn to complete updates.")
            shutil.rmtree(guftemp_path)
            sys.exit()
    else:
        print("Failed to create CodeOn file runner file. Please reload CodeOn to complete updates.")
        shutil.rmtree(guftemp_path)
        sys.exit()
else:
    print("Failed to create CodeOn file. Please reload CodeOn to complete updates.")
    shutil.rmtree(guftemp_path)
    sys.exit()


