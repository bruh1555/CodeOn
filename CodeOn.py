codeonversion = "0.8.0"
codeonnew = True
noupdate = False
verboseoutput = False
import time
import os
import sys
import ctypes
import shutil
import itertools
import threading

# from now on, i will add comments to the code and put the date so people can see (for fun) - bruh1555 5/16/2025

def vbout(text):
    # im too lazy to copy paste - bruh1555 5/17/2025
    if verboseoutput == True:
        print(text)
    else:
        pass

def format_size(size, unit='Bytes'):
    units_in_bytes = {
        'Bytes': 1,
        'KB': 1024,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
        'TB': 1024 ** 4,
        'PB': 1024 ** 5,
        'EB': 1024 ** 6,
        'ZB': 1024 ** 7,
        'YB': 1024 ** 8
    }
    if unit not in units_in_bytes:
        raise ValueError(f"Unsupported unit '{unit}'.")
    size_in_bytes = size * units_in_bytes[unit]
    if size_in_bytes < 1024:
        return f"{size_in_bytes:.2f} Bytes"
    elif size_in_bytes < 1024 ** 2:
        return f"{size_in_bytes / 1024:.2f} KB"
    elif size_in_bytes < 1024 ** 3:
        return f"{size_in_bytes / (1024 ** 2):.2f} MB"
    elif size_in_bytes < 1024 ** 4:
        return f"{size_in_bytes / (1024 ** 3):.2f} GB"
    elif size_in_bytes < 1024 ** 5:
        return f"{size_in_bytes / (1024 ** 4):.2f} TB"
    elif size_in_bytes < 1024 ** 6:
        return f"{size_in_bytes / (1024 ** 5):.2f} PB"
    elif size_in_bytes < 1024 ** 7:
        return f"{size_in_bytes / (1024 ** 6):.2f} EB"
    elif size_in_bytes < 1024 ** 8:
        return f"{size_in_bytes / (1024 ** 7):.2f} ZB"
    else:
        return f"{size_in_bytes / (1024 ** 8):.2f} YB"


def remove_module_error(func, path, exc_info):
    exc_type, exc_value, exc_traceback = exc_info
    if exc_type == PermissionError:
        print(f"PermissionError: {path} - {exc_value}")
        try:
            os.chmod(path, 0o777)
            func(path)
        except Exception as e:
            print(f"Failed to delete {path}: {e}")
    else:
        print(f"Error: {path} - {exc_value}")
        raise

try:
    vbout("Importing CodeOn Modules...")
    import gnv as gnv
    import checkinternet
except Exception as e:
    print("CodeOn cannot continue.")
    print(f"Error while importing CodeOn Modules: {e}")
    exit()

def install_codeon_module_end(module, ModuleDir, url):
    import requests
    import pyotp
    import configparser
    from colored import fg
    from pathlib import Path
    if os.path.exists(ModuleDir):
        shutil.rmtree(ModuleDir)
    os.makedirs(ModuleDir, exist_ok=True)
    response = requests.get(url)
    if response.status_code == 200:
        for i, object in enumerate(response.json()):
            if object['type'] == 'file':
                download_url = object['download_url']
                path = str(object['path'])
                path = path.removeprefix(module + "/")
                path = path.replace('/', ' ')
                path = path.split()
                endedpath = ModuleDir
                for path2 in path:
                    endedpath = endedpath / path2
                response3 = requests.get(download_url)
                if response3.status_code == 200:
                    with open(endedpath, 'w') as fileopened:
                        fileopened.write(response3.text)
                        fileopened.close()
                else:
                    vb_clear_screen()
                    print(f"Failed to install module {module}.")
                    shutil.rmtree(ModuleDir)
            elif object['type'] == 'dir':
                path = str(object['path'])
                path = path.removeprefix(module + "/")
                path = path.replace('/', ' ')
                path = path.split()
                endedpath = ModuleDir
                for path2 in path:
                    endedpath = endedpath / path2
            else:
                vb_clear_screen()
                print("Error with file type.")
                print(f"Failed to install module {module}.")
                shutil.rmtree(ModuleDir)
        vb_clear_screen()
        print(f"Successfully installed module {module}.")
    else:
        vb_clear_screen()
        print(f"Failed to install module {module}.")
        shutil.rmtree(ModuleDir)

def get_codeon_module_size_end(url: str, module: str):
    import requests
    gitsize1 = requests.get(url)
    if gitsize1.status_code == 200:
        gitsize1json = gitsize1.json()
        gitsize = ''
        for object in gitsize1json:
            if object['type'] == 'file':
                gitsize = gitsize + str(object['size'])
            elif object['type'] == 'dir':
                url2 = object['url']
                get_codeon_module_size_end(url2, module)
            else:
                return 'fail'
        return gitsize
    else:
        return 'fail'

def get_codeon_module_size(url: str, module: str, formatfrom: str = 'Bytes'):
    import requests
    gitsize1 = requests.get(url)
    if gitsize1.status_code == 200:
        gitsize1json = gitsize1.json()
        gitsize = ''
        for object in gitsize1json:
            if object['type'] == 'file':
                gitsize = gitsize + str(object['size'])
            elif object['type'] == 'dir':
                url2 = object['url']
                test1 = get_codeon_module_size_end(url2, module)
                if test1 == 'fail':
                    print("Failed to get size")
                    break
                else:
                    gitsize = gitsize + test1
            else:
                print("Failed to get size")
                break
        try:
            gitsize = float(gitsize)
            print(f"Size of {module} is {format_size(gitsize, formatfrom)}.")
            return gitsize
        except:
            print("Failed to get size.")
    else:
        print("Failed to get size.")

def install_codeon_module(module):
    import requests
    import pyotp
    import configparser
    from colored import fg
    from pathlib import Path
    current_script = Path(__file__).resolve()
    parent_dir = current_script.parent
    modules_dir = parent_dir / "Modules"
    ModuleDir = modules_dir / module
    os.makedirs(modules_dir, exist_ok=True)
    url = f"https://api.github.com/repos/bruh1555/CodeOnModules/contents/{module}"
    gitsize1 = get_codeon_module_size(url, module)
    testexpression = shutil.disk_usage("/").free - gitsize1
    if testexpression <= 10 * 1024 ** 3:
        print("You do not have enough storage left to download this module.")
        return
    confirm = input(f"Are you sure you'd like to install the module {module}? [y/n]: ")
    if confirm == 'y':
        installer = threading.Thread(target=install_codeon_module_end, args=(module,ModuleDir,url,))
        wheel = threading.Thread(target=ewheel)
        installer.start()
        wheel.start()
        installer.join()
        wheeldone.set()
        time.sleep(0.1)
        wheeldone.clear()
    else:
        vb_clear_screen()
        print("Canceled operation.")

def install_codeon_module_unofficial_end(repo_url, repository):
    import requests
    import pyotp
    import configparser
    from colored import fg
    from pathlib import Path
    from git import Repo
    current_script = Path(__file__).resolve()
    parent_dir = current_script.parent
    modules_dir = parent_dir / "Modules"
    ModuleDir = modules_dir / repository
    os.makedirs(modules_dir, exist_ok=True)
    if os.path.exists(ModuleDir):
        shutil.rmtree(ModuleDir)
    Repo.clone_from(repo_url, ModuleDir)
    vb_clear_screen()
    print(f"Successfully installed module {repository}.")

def install_codeon_module_unofficial(username, repository):
    import requests
    import pyotp
    import configparser
    from colored import fg
    from pathlib import Path
    url = f'https://api.github.com/repos/{username}/{repository}'
    response = requests.get(url)
    if response.status_code == 200:
        response2 = requests.get(f"https://raw.githubusercontent.com/{username}/{repository}/main/main.py")
        if response2.status_code == 200:
            from git import Repo
            
            repo_url = f'https://github.com/{username}/{repository}.git'
            repo_url2 = repo_url.removesuffix('.git')
            gitsize = response.json()['size']
            print(f"Would install from {repo_url}")
            print(f"Size of repository is {format_size(gitsize)}.")
            if gitsize >= shutil.disk_usage("/").free:
                print("You do not have enough storage left to download this module.")
                return
            testexpression = shutil.disk_usage("/").free - gitsize 
            if testexpression <= 10 * 1024 ** 3:
                print(f"You will have less than 10 GB ({format_size(testexpression)}) left if you install this module.")
                print("You cannot install this module.")
                return
            print(f"You have {format_size(shutil.disk_usage("/").free)} storage left.")
            confirm = input(f"Are you sure you'd like to install the module {repository}? [y/n]: ")
            if confirm == 'y':
                installer = threading.Thread(target=install_codeon_module_unofficial_end, args=(repo_url,repository,))
                wheel = threading.Thread(target=ewheel)
                installer.start()
                wheel.start()
                installer.join()
                wheeldone.set()
                time.sleep(0.1)
                wheeldone.clear()
            else:
                vb_clear_screen()
                print("Canceled operation.")
        else:
            vb_clear_screen()
            print("Error: Repository does not include a main.py file in the main tree, and in the main directory.")
    else:
        vb_clear_screen()
        print("Error: The github repository doesn't exist.")

def error(text):
    vbout("Printing error...")
    import requests
    import pyotp
    import configparser
    from colored import fg
    from pathlib import Path
    errorcolor = fg('light_red')
    print(f'{errorcolor}{text}{errorcolor}')
    sys.stdout.write(f"{fg('white')}{fg('white')}")
    sys.stdout.flush()

def warn(text):
    vbout("Printing warning...")
    import requests
    import pyotp
    import configparser
    from colored import fg
    from pathlib import Path
    errorcolor = fg('light_yellow')
    print(f'{errorcolor}{text}{errorcolor}')
    sys.stdout.write(f"{fg('white')}{fg('white')}")
    sys.stdout.flush()

def dwheel(duration=10):
    '''Used to make a command-line wheel.'''
    wheel_chars = itertools.cycle(['|', '/', '—', '\\'])
    end_time = time.time() + duration
    while time.time() < end_time:
        sys.stdout.write("\r" + next(wheel_chars))
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + '\033[K')
    sys.stdout.flush()

global wheeldone
wheeldone = threading.Event()
def ewheel():
    '''Used to make a command-line wheel. Waits for wheeldone to be set. You must manually clear the last wheel character.'''
    wheel_chars = itertools.cycle(['|', '/', '—', '\\'])
    while not wheeldone.is_set():
        sys.stdout.write("\r" + next(wheel_chars))
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + '\033[K')
    sys.stdout.flush()

def set_console_title(title):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)
def clear_screen():
    vbout("Clearing screen...")
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
def vb_clear_screen():
    if verboseoutput == True:
        vbout("not clearing screen because you have verbose output on")
    else:
        clear_screen()

def install_package(package_name):
    try:
        vbout("Checking if you have pip...")
        pip_version = os.system(f"{sys.executable} -m pip --version")
        if pip_version != 0:
            print("pip is not available. Please install pip first.")
            return
    except Exception as e:
        print(f"Error checking pip version: {e}")
        return
    try:
        vbout("Installing package...")
        print(f"Installing {package_name}...")
        ewheel()
        install_command = f"{sys.executable} -m pip install {package_name}"
        result = os.system(install_command)
        if result == 0:
            wheeldone.set()
            print(f"{package_name} installed successfully.")
            wheeldone.clear()
        else:
            wheeldone.set()
            print(f"Failed to install {package_name}. Exit code: {result}")
            wheeldone.clear()
    except Exception as e:
        print(f"Error installing package {package_name}: {e}")

def getlatestversionfunc():
    import requests
    import pyotp
    import configparser
    from colored import fg
    from pathlib import Path
    current_script = Path(__file__).resolve()
    parent_dir = current_script.parent
    target_script_path = None
    
    for root, dirs, files in os.walk(parent_dir):
        if "updatecon.py" in files:
            target_script_path2 = Path(root) / "updatecon.py"
            break
    
    if target_script_path2:
        target_script_path = f'"{target_script_path2}"'
        os.system(f'python {target_script_path}')
        print("Welcome back! We are reloading CodeOn to receive the data retrieved from the updater.")
        script_path2 = os.path.abspath(__file__)
        script_path = f'"{script_path2}"'
        os.execv(sys.executable, ['python'] + [script_path])
        sys.exit()
    else:
        error("ACTION REQUIRED: THE FILE 'updatecon.py' CANNOT BE FOUND. PLEASE REDOWNLOAD CODEON TO FIX THIS ISSUE.")
        sys.exit()

print("Starting CodeOn.......")
dwheel(2)
print("Checking your internet connection...")
returncheck = checkinternet.check()
dwheel(2)
if returncheck == "False":
    print("Error: You are not connected to the internet. CodeOn requires an internet connection. Please try again later when you have one.")
    print("You may continue without WiFi.")
    load = input("Would you like to load CodeOn without your WiFi connection? (y/n): ")
    if load == "n":
        sys.exit()
    else:
        print("Continuing.")
        print("You will be asked the question again.")
print("Checking for new versions...")
latest_version = gnv.gnv()
dwheel(2)
if "Error: " in latest_version:
    print(f"Error checking for updates. Manually check by going to https://raw.githubusercontent.com/bruh1555/CodeOn/main/latest_version.txt and checking if {codeonversion} is the version. CodeOn will not work if we cannot get the latest version.")
    print("You may load CodeOn without WiFi.")
    load = input("Would you like to load CodeOn without your WiFi connection? (y/n): ")
    if load == "n":
        sys.exit()
    else:
        print("Continuing.")
        print("Ignore the module errors.")
else:
    if codeonversion == "testing":
        print("Continuing because you are in the testing environment...")
    elif noupdate == True:
        print("Continuing because you have disabled updates...")
    elif not str(codeonversion.strip()) == str(latest_version.strip()): # are you actually serious? i had to use str? - bruh1555 5/18/2025
        print("You do not have the latest version.")
        print(f'Version of current CodeOn: {repr(codeonversion)}')
        print(f'Latest CodeOn Version: {repr(latest_version)}')
        print("Getting latest version...")
        getlatestversionfunc()

def reporterror(e):
    try:
        vbout("Reporting error...")
        import requests
        wheeldone.set()
        request = requests.post("https://codeon.glitch.me/autoreporterror", data={"error": str(e)})
        if request.status_code == 200:
            print("Error reported successfully.")
        else:
            print("Error reporting the issue to our web server. The web server had an issue.")
            wheeldone.clear()
    except:
        wheeldone.set()
        print("Error reporting the issue to our web server. It is due to something in this code or on your PC.")
        wheeldone.clear()

def main2():
    try:
        import requests
        import pyotp
        import configparser
        from colored import fg
        from pathlib import Path
        import psutil
    except:
        internet = checkinternet.check()
        if internet == "True":
            print("Installing modules...")
            vbout("requests")
            install_package('requests')
            vbout("pyotp")
            install_package('pyotp')
            vbout("configparser")
            install_package('configparser')
            vbout("pathlib")
            install_package('pathlib')
            vbout("colored")
            install_package('colored')
            vbout("psutil")
            install_package('psutil')
            vb_clear_screen()
        else:
            print("You do not have all modules installed, and you have no internet, so you cannot install the modules.")
            print("CodeOn cannot continue without the required modules.")
            sys.exit()
    import requests
    import pyotp
    import configparser
    from colored import fg
    from pathlib import Path
    current_script = Path(__file__).resolve()
    parent_dir = current_script.parent
    mdl_temp_files_dir = parent_dir / "mdl_temp_files"
    mdl_temp_files_note = mdl_temp_files_dir / "note-for-module-creators.txt"
    modules_dir = parent_dir / "Modules"
    modulesecret = modules_dir / "main.py"
    os.makedirs(modules_dir, exist_ok=True)
    os.makedirs(mdl_temp_files_dir, exist_ok=True)
    with open(modulesecret, 'w') as modulesecretopen:
        modulesecretopen.write("""import time
import os
import sys
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')
def write(text, f=False, speed=0.037):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if f:
            time.sleep(0.0007)
        else:
            time.sleep(speed)
write('''Well looks like you found the easter egg!
''')
time.sleep(0.4)
write('''Fun fact: this was supposed to be added in version 0.6 Alpha but was instead added in version 0.6!
''')
time.sleep(0.3)
write('''That was so hard to find, right? I mean, using the modules function, loading a module, putting in nothing for the next two inputs.
''')
time.sleep(0.3)
write('''Anyways I don't really have much to talk about here..
''')
time.sleep(0.3)
write('''So I'm going to finish this here...
''')
time.sleep(0.3)
write('''By the way, if you're reading the code for the main CodeOn file, all you have to do to access this is
''')
write('''Put in the mdl command, then put in 4, then leave the next 2 inputs blank, and there you go, you'll see the easter egg!
''')
""")
        modulesecretopen.close()
    # yes there's an easter egg. well at least i'm not the only one who opens code and reads it..
    vbout("writing module creator rules...")
    with open(mdl_temp_files_note, 'w') as mdl_temp_files_note_opened:
        mdl_temp_files_note_opened.write("""When you create a module, you must include a main.py file, as that is what will be ran when a user loads a module.
You are not allowed to write files outside of your module's directory, or cause any damage to the pc.
The ONLY exception to this, you may write to parent directory of this file, as if you want to keep that info when the user updates your module,
You can do this. But you must have your code create a directory in this scripts parent directory as the name of your module,
otherwise it is not permitted for you to write to the parent directory of this script.
I will create a check for this one day.
If you break these rules, we will add you to a ban list, and users will not be able to install modules from your user.
Sorry for my bad grammer and stupid stuff like that.
""")
    vb_clear_screen()
    set_console_title('CodeOn Command Line')
    print("Welcome to the CodeOn command line! Type in the command 'help' for help.")
    dwheel(1)
    vb_clear_screen()
    vbout("checking if you're new to CodeOn")
    if codeonnew == True:
        print("Hey, It looks like you just installed CodeOn!")
        noupdate2 = input("Would you like to disable automatic updates? (y/n): ")
        if noupdate2 == "y":
            print("Writing data...")
            current_script = Path(__file__).resolve()
            with open(current_script, 'r') as noupdatewrite:
                noupdatewritedata = noupdatewrite.readlines()
            noupdatewritedata[2] = "noupdate = True\n"
            noupdatewritedata[1] = "codeonnew = False\n"
            with open(current_script, 'w') as noupdatewrite2:
                noupdatewrite2.writelines(noupdatewritedata)
            noupdatewrite.close()
            noupdatewrite2.close()
            vb_clear_screen()
        else:
            print("Writing data...")
            current_script = Path(__file__).resolve()
            with open(current_script, 'r') as noupdatewrite:
                noupdatewritedata = noupdatewrite.readlines()
            noupdatewritedata[1] = "codeonnew = False\n"
            with open(current_script, 'w') as noupdatewrite2:
                noupdatewrite2.writelines(noupdatewritedata)
            noupdatewrite.close()
            noupdatewrite2.close()
            vb_clear_screen()

    def parse(program):
        tokens = program.split()
        if not tokens:
            return None
        command = tokens[0]
        if command == 'cfile':
            if len(tokens) == 2:
                return ('cfile', tokens[1], None)
            elif len(tokens) > 2:
                return ('cfile', tokens[1], ' '.join(tokens[2:]))
            else:
                print("Invalid command syntax for cfile")
        elif command == 'cfolder':
            if len(tokens) == 3:
                return ('cfolder', tokens[1], tokens[2])
            else:
                print("Invalid command syntax for cfolder")
        elif command == 'efile':
            if len(tokens) == 2:
                return ('efile', tokens[1])
            else:
                print("Invalid command syntax for efile")
        else:
            print("Unknown command: ", command)
        return None

    def create_file():
        filepath = input("Enter the path of the file to create (don't include quotation marks): ")
        filename = input("What should the file name be: ")
        content = input("What should the contents be (notice this will only be one line so you must use the efile command to do multiple lines): ")
        full_path = os.path.join(filepath, filename)
        with open(full_path, "w") as file:
            if content is not None:
                vbout("Writing content to file...")
                file.write(content)
                print(f"File '{filename}' created with content at '{filepath}'.")
            else:
                vbout("finishing file")
                print(f"File '{filename}' created at '{filepath}'.")
    def mv_file():
        source_path = input("Enter the path of the file to move (don't include quotation marks): ")
        vbout("Checking if the file exists...")
        if not os.path.isfile(source_path):
            print("The file does not exist.")
            return
        dest_path = input("Enter the destination path (including the filename): ")
        try:
            vbout("Moving file...")
            shutil.move(source_path, dest_path)
            print(f"File moved successfully to {dest_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
    def remove_file():
        file_path = input("Enter the path of the file to edit (don't include quotation marks): ")
    
        if os.path.exists(file_path):
            try:
                vbout("Removing file...")
                os.remove(file_path)
                print(f"The file '{file_path}' has been removed successfully.")
            except Exception as e:
                print(f"An error occurred while removing the file: {e}")
        else:
            print(f"The file '{file_path}' does not exist.")
    
    def move_folder():
        source_folder = input("Enter the path of the folder (don't include quotation marks): ")
        if not os.path.isdir(source_folder):
            print("The folder does not exist.")
            return
        dest_folder = input("Enter the destination path (including the folder name): ")
        try:
            vbout("Moving folder...")
            shutil.move(source_folder, dest_folder)
            print(f"Folder moved successfully to {dest_folder}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    
    def remove_folder(folder_path):
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            try:
                vbout("Removing folder...")
                shutil.rmtree(folder_path)
                print(f"The folder '{folder_path}' has been removed successfully.")
            except Exception as e:
                print(f"An error occurred while removing the folder: {e}")
        else:
            print(f"The folder '{folder_path}' does not exist or is not a directory.")

    def create_folder(folder_path, folder_name):
        vbout("Creating folder...")
        full_path = os.path.join(folder_path, folder_name)
        os.makedirs(full_path, exist_ok=True)
        print(f"Folder '{folder_name}' created at '{folder_path}'.")

    def edit_file():
        try:
            file_path = input("Enter the path of the file to edit (don't include quotation marks): ")
            with open(file_path, "r+") as file:
                contents = file.read()
                print("Current content of the file:")
                print(contents)
                print("Enter new content. Press Enter on an empty line to finish. (THIS WILL REWRITE THE FILE. IF YOU MAKE A MISTAKE, PRESS CTRL+C, IT WILL CLOSE THE PYTHON PROGRAM.)")
                new_contents = []
                while True:
                    line = input()
                    if not line:
                        vbout("Empty line detected, finishing file...")
                        break
                    vbout("Writing content to file...")
                    new_contents.append(line)
                    new_contents = "\n".join(new_contents)
                    file.seek(0)
                    file.write(new_contents)
                    file.truncate()
                    print(f"File '{file_path}' has been edited successfully.")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    variables = {}

    def main():
        environment = {}
        while True:
            try:
                if os.name == 'nt':
                    buffer = ctypes.create_unicode_buffer(1024)
                    ctypes.windll.kernel32.GetConsoleTitleW(buffer, 1024)
                    current_title = buffer.value
                    if not current_title.endswith(" - CodeOn"):
                        set_console_title(f'{current_title} - CodeOn')
                program = input("CodeOn>> ")
                if program == "exit":
                    print("Exiting command line...")
                    break
                elif program == "help":
                    vbout("Displaying help...")
                    print("Commands available:")
                    print("- 'exit': exit the command line")
                    print("- 'help': display this help message")
                    print("- 'help all': display all help commands")
                    print("- 'clear': clear your environment you are running CodeOn in.")
                    print("- 'cfile': create a file with the content, if the file has no content, it will be set to the default")
                    print("- 'cfolder': create a folder")
                    print("- 'efile': edit a file")
                    print("- 'reload': reload CodeOn")
                    print("- 'read': read a file made of CodeOn commands (not finished)")
                    print("- 'helpread': display help to write a file for the read command")
                    print("- 'print <contents>': print the string you wrote")
                    print("- 'math <+ - * /> <num1> <num2>': do a math problem")
                    print(f"- 'info': get info about your current CodeOn version.")
                    print("To get more information, use the command 'help all'")
                    continue
                elif program == "help all":
                    vbout("Displaying all help...")
                    print("slowly working on this (will not be finished fast)")
                    print("Commands available:")
                    print("- 'exit': exit the command line")
                    print("- 'help': display the shortened help message (doesn't include all commands)")
                    print("- 'help all': display this help message")
                    print("- 'clear': clear your environment you are running CodeOn in.")
                    print("- 'cfile': create a file with the content, if the file has no content, it will be set to the default")
                    print("- 'cfolder': create a folder")
                    print("- 'efile': edit a file")
                    print("- 'mvfile': move a file")
                    print("- 'mvfolder': move a folder")
                    print("- 'read': read a file made of CodeOn commands (not finished)")
                    print("- 'helpread': display help to write a file for the read command")
                    print("- 'print <contents>': print the string you wrote")
                    print("- 'math <+ - * /> <num1> <num2>': do a math problem")
                    print("- 'info': get info about your current CodeOn version.")
                    print("- 'os': please type in 'os' to get information about this command. (i'm too lazy to type it all in here lol)")
                    print("- 'user': get the current logged in user")
                    print("- 'ncon': open another CodeOn console")
                    print("- 'py': open a python console")
                    print("- 'py <location>: open a python script")
                    print("- 'vmcon': open a CodeOn console within the current one (testing purposes, but can be used for stopping errors from closing the console)")
                    print("- 'rstcon': reset CodeOn (redownload using update service)")
                    print("- 'rstartcon': restart CodeOn (reopen codeon)")
                    print("- 'dwheel <duration>': create a command line wheel for the amount of provided seconds")
                    print("- 'kill <pname>: kill a process by name (must be with extension)")
                    print("- 'inspypackage <pname>: use pip to install a python package by name")
                    print("- 'uninscon: uninstall CodeOn")
                    print("- 'settings': set settings for CodeOn")
                    if noupdate == True:
                        print("- 'manupdate': manually check for updates and update")
                    continue
                elif program == "clear":
                    vbout("clearing because you said so")
                    clear_screen()
                    continue
                elif program == "":
                    vbout("continuing because no value")
                    continue
                elif program == "efile":
                    edit_file()
                elif program == "settings":
                    vbout("Opening settings...")
                    print("Settings available:")
                    print("- 'noupdate': disable automatic updates")
                    print("- 'verboseoutput': send output for everything that runs")
                    print("- 'exit': exit this area")
                    print("Select an option.")
                    setting = input("CodeOn Settings>> ")
                    if setting == "noupdate":
                        noupdate2 = input("Would you like to disable automatic updates? (y/n): ")
                        if noupdate2 == "y":
                            print("Writing data...")
                            current_script = Path(__file__).resolve()
                            with open(current_script, 'r') as noupdatewrite:
                                noupdatewritedata = noupdatewrite.readlines()
                            noupdatewritedata[2] = "noupdate = True\n"
                            with open(current_script, 'w') as noupdatewrite2:
                                noupdatewrite2.writelines(noupdatewritedata)
                                noupdatewrite.close()
                                noupdatewrite2.close()
                                vb_clear_screen()
                        else:
                            print("Writing data...")
                            current_script = Path(__file__).resolve()
                            with open(current_script, 'r') as noupdatewrite:
                                noupdatewritedata = noupdatewrite.readlines()
                            with open(current_script, 'w') as noupdatewrite2:
                                noupdatewrite2.writelines(noupdatewritedata)
                            noupdatewrite.close()
                            noupdatewrite2.close()
                            vb_clear_screen()
                    elif setting == "verboseoutput":
                        noupdate2 = input("Would you like to enable verbose output? (y/n): ")
                        if noupdate2 == "y":
                            print("Writing data...")
                            current_script = Path(__file__).resolve()
                            with open(current_script, 'r') as noupdatewrite:
                                noupdatewritedata = noupdatewrite.readlines()
                            noupdatewritedata[3] = "verboseoutput = True\n"
                            with open(current_script, 'w') as noupdatewrite2:
                                noupdatewrite2.writelines(noupdatewritedata)
                                noupdatewrite.close()
                                noupdatewrite2.close()
                                vb_clear_screen()
                        else:
                            print("Writing data...")
                            current_script = Path(__file__).resolve()
                            with open(current_script, 'r') as noupdatewrite:
                                noupdatewritedata = noupdatewrite.readlines()
                                noupdatewritedata[3] = "verboseoutput = False\n"
                            with open(current_script, 'w') as noupdatewrite2:
                                noupdatewrite2.writelines(noupdatewritedata)
                            noupdatewrite.close()
                            noupdatewrite2.close()
                            vb_clear_screen()
                elif program == "manupdate":
                    if codeonversion == "testing":
                        print("You are in the testing environment, so you cannot update.")
                    else:
                        vbout("Checking for updates...")
                        getlatestversionfunc()
                elif program == "uninscon":
                    if codeonversion == "testing":
                        print("You are in the testing environment, so you cannot uninstall. You msut manually uninstall CodeOn.")
                    else:
                        print("Please note that this command removes the whole parent directory of this script.")
                        current_script = Path(__file__).resolve()
                        parent_dir = current_script.parent
                        print(f"Would remove: {parent_dir}")
                        confirm = input("Are you sure you would like to uninstall CodeOn? [y/n]: ")
                        if confirm == "y":
                            print("Uninstalling CodeOn...")
                            ewheel()
                            shutil.rmtree(parent_dir)
                            wheeldone.set()
                            print("CodeOn uninstalled.")
                            wheeldone.clear()
                            sys.exit()
                elif "inspypackage " in program:
                    arguments = program.split()
                    install_package(''.join(arguments[1:]))
                elif "kill " in program:
                    arguments = program.split()
                    exe_name = ''.join(arguments[1:])
                    killed = False
                    for proc in psutil.process_iter(['pid', 'name']):
                        try:
                            if proc.info['name'].lower() == exe_name.lower():
                                print(f"Killing {proc.info['name']} (PID {proc.pid})")
                                proc.kill()
                                killed = True
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                    if not killed:
                        print(f"No running process found with executable name: {exe_name}")
                elif program == "cfile":
                    create_file()
                elif program == "cfolder":
                    folder_name = input("Enter the name of the folder: ")
                    folder_path = input("Enter the path where the folder should be created (don't include quotation marks): ")
                    create_folder(folder_path, folder_name)
                elif program == "rfile":
                    remove_file()
                elif program == "rfolder":
                    folder_path = input("Enter the path of the folder (don't include quotation marks): ")
                    remove_folder(folder_path)
                elif program == "mvfile":
                    mv_file()
                elif program == "mvfolder":
                    move_folder()
                elif program == "rstartcon":
                    vb_clear_screen()
                    vbout("Restarting CodeOn...")
                    script_path2 = os.path.abspath(__file__)
                    script_path = f'"{script_path2}"'
                    os.system(f'{sys.executable} {script_path}')
                    sys.exit()
                elif program == "read":
                    vbout("Checking if you have the interpreter...")
                    current_script = Path(__file__).resolve()
                    parent_dir = current_script.parent
                    target_script_path = None
                    for root, dirs, files in os.walk(parent_dir):
                        if "CodeOn file runner.py" in files:
                            target_script_path = Path(root) / "CodeOn file runner.py"
                            break
                    if target_script_path:
                        os.system(f'python {target_script_path}')
                    else:
                        error("ACTION REQUIRED: THE FILE 'CodeOn file runner.py' CANNOT BE FOUND. PLEASE REDOWNLOAD CODEON TO FIX THIS ISSUE.")
                        sys.exit()
                elif program == "helpread":
                    vbout("Getting help for the read command...")
                    print("Commands available for reading a file:")
                    print("- 'exit': exit the file")
                    print("- 'clear': clear console")
                    print("- 'print <contents>': print the string you wrote")
                    print("- 'math <+ - * /> <num1> <num2>': do a math problem")
                elif program == "info":
                    vbout("Getting info...")
                    print("Info about CodeOn:")
                    print(f'CodeOn {codeonversion}')
                    print("Cross-platform Version")
                    print("CodeOn was made using Python.")
                    print("If you get any Python errors, please report them by emailing developerv0002@gmail.com and including the Python error.")
                    print("You may also submit a pull request on the GitHub repository you got the software from.")
                    print("We will fix it as soon as possible and return a version to fix your error.")
                    print("Dev note: 1200 lines of code! 2x what we had in the last version. I'm so proud of this.")
                elif "print " in program:
                    vbout("Printing...")
                    arguments = program.split()
                    print(' '.join(arguments[1:]))
                elif "math " in program:
                    vbout("Doing math (lol)...")
                    arguments = program.split()
                    if len(arguments) == 4:
                        try:
                            num1 = float(arguments[2])
                            num2 = float(arguments[3])
                            if arguments[1] == "+":
                                output = num1 + num2
                            elif arguments[1] == "-":
                                output = num1 - num2
                            elif arguments[1] == "*":
                                output = num1 * num2
                            elif arguments[1] == "/":
                                output = num1 / num2
                            else:
                                raise ValueError("Invalid operator")
                            print(f"{num1} {arguments[1]} {num2} = {output}")
                        except ValueError as ve:
                            print(f"Error: {ve}")
                        else:
                            print("Usage: math <operator> <num1> <num2>")
                elif "variable " in program:
                        vbout("Creating variable...")
                        arguments = program.split()
                        if not arguments[2] == "math":
                            variables[str(arguments[1])] = str(arguments[2])
                        else:
                            try:
                                if arguments[3] == "+":
                                    output = float(arguments[5]) + float(arguments[6])
                                elif arguments[3] == "-":
                                    output = float(arguments[5]) - float(arguments[6])
                                elif arguments[3] == "*":
                                    output = float(arguments[5]) * float(arguments[6])
                                elif arguments[3] == "/":
                                    output = float(arguments[5]) / float(arguments[6])
                                else:
                                    output = "math"
                                variables[str(arguments[2])] = output
                            except ValueError as ve:
                                print(f"Error: {ve}")
                elif "os" in program:
                    arguments = program.split()
                    if len(arguments) >= 2:
                        if arguments[1] == "syscmd":
                            vbout("Running system command...")
                            program2 = program[9:]
                            os.system(program2)
                        elif arguments[1] == "shutdown":
                            vbout("Shutting down...")
                            if len(arguments) == 3:
                                if os.name == 'nt':
                                    if arguments[2] == "r":
                                        os.system("shutdown -r -t 0")
                                    elif arguments[2] == "s":
                                        os.system("shutdown -s -t 0")
                                    elif arguments[2] == "l":
                                        os.system("shutdown -l")
                                else:
                                    if arguments[2] == "r":
                                        os.system("sudo shutdown -r now")
                                    elif arguments[2] == "s":
                                        os.system("sudo shutdown -h now")
                            else:
                                vbout("Displaying usage...")
                                print("Usage:")
                                print("s - shutdown the device")
                                print("r - restart the device")
                                print("l - logoff (Windows only)")
                        elif arguments[1] == "sapt":
                            if os.name == 'nt':
                                print("This command is not available on Windows.")
                            else:
                                vbout("Running apt command...")
                                os.system("sudo apt " + ''.join(arguments[2:]))
                        elif arguments[1] == "alaunch":
                            vbout("Relaunching CodeOn with admin privileges...")
                            print("""this may glitch out your admin cmd prompt at the start with a "←[K" whenever it starts. i can't fix that""")
                            if os.name == 'nt':
                                current_script = Path(__file__).resolve()
                                cmd_command = f'"{sys.executable}" \\"{current_script}""'
                                print(cmd_command)
                                powershell_command = (f'powershell -Command "Start-Process cmd -ArgumentList \'/k {cmd_command}\' -Verb RunAs"')
                                os.system(powershell_command)
                                sys.exit()
                            else:
                                current_script = Path(__file__).resolve()
                                os.system(f'sudo "{sys.executable} {current_script}" ' + current_script)
                                sys.exit()
                    else:
                        print("Usage:")
                        print("syscmd - call a command on your system.")
                        print("shutdown <s, r, l> - shutdown your system using a specific method")
                        print("sapt <command (like install blank or update)> - run a command using apt (Linux only and requires admin)")
                        print("alaunch - relaunch CodeOn with admin privileges")
                elif program == "user":
                    vbout("Getting user...")
                    if os.name == 'nt':
                        os.system('whoami')
                    else:
                        os.system('id -un')
                elif program == "py":
                    vbout("Opening python console...")
                    os.system("python3")
                elif "py" in program:
                    vbout("Running python script...")
                    program2 = program[3:]
                    os.system(f'python3 "{program2}"')
                elif program == "ncon":
                    vbout("Opening new CodeOn console...")
                    script_path = os.path.abspath(__file__)
                    if os.name == 'nt':
                        os.system(f'start cmd /K python "{script_path}"')
                    else:
                        os.system(f'gnome-terminal -- python "{script_path}"')
                elif "cmdtitle" in program:
                    if os.name == 'nt':
                        vbout("Setting console title...")
                        program2 = program[9:]
                        set_console_title(f'{program2} - CodeOn')
                elif program == "vmcon":
                    vbout("Opening new CodeOn console within the current one...")
                    script_path = os.path.abspath(__file__)
                    os.system(f'{sys.executable} "{script_path}"')
                elif program == "rstcon":
                    if codeonversion == "testing":
                        print("You are in the testing environment, so you cannot reset CodeOn.")
                    else:
                        vbout("Resetting CodeOn...")
                        getlatestversionfunc()
                elif program == "mdl":
                    vbout("Opening module command line...")
                    print("Welcome to the module command line!")
                    print("Choose an option:")
                    print("1. Download Official Module")
                    print("2. Download UnOfficial Module")
                    print("3. Remove a Module")
                    print("4. Load a Module")
                    print("5. Update an Official Module (removes and then redownloads)")
                    print("6. Update an UnOfficial Module (removes and then redownloads)")
                    print("7. Exit")
                    option = input("Option: ")
                    if option == "1":
                        module = input("Module name (case sensitive): ")
                        install_codeon_module(module)
                    elif option == "2":
                        warn("WARNING: Only install modules you trust, and if you've reviewed the code.")
                        print("Note: The owner is not responsible for any damage caused by any unofficial CodeOn module.")
                        time.sleep(2)
                        print("You can only install from GitHub currently.")
                        username = input("Username of the owner of the repository you'd like to install (case sensitive): ")
                        repository = input("Repository name of the repository you'd like to install (case sensitive): ")
                        print("Getting gitpython module..")
                        install_package("gitpython")
                        vb_clear_screen()
                        warn("WARNING: Only install modules you trust, and if you've reviewed the code.")
                        print("Note: The owner is not responsible for any damage caused by any unofficial CodeOn module.")
                        try:
                            from git import Repo
                        except:
                            print("Error getting gitpython. You might not have internet.")
                            break
                        vb_clear_screen()
                        warn("WARNING: Only install modules you trust, and if you've reviewed the code.")
                        print("Note: The owner is not responsible for any damage caused by any unofficial CodeOn module.")
                        vbout("starting unofficial download")
                        install_codeon_module_unofficial(username, repository)
                    elif option == "3":
                        module = input("Module name (case sensitive): ")
                        current_script = Path(__file__).resolve()
                        parent_dir = current_script.parent
                        modules_dir = parent_dir / "Modules"
                        if os.path.exists(modules_dir):
                            ModuleDir = modules_dir / module
                            if os.path.exists(ModuleDir):
                                print(f"Would remove {ModuleDir}" + "\\" + "*")
                                confirm = input(f"Are you sure you would like to remove the module {module}? [y/n]: ")
                                if confirm == "y":
                                    vbout("removing module")
                                    shutil.rmtree(ModuleDir, onerror=remove_module_error)
                                    vb_clear_screen()
                                    print("If you got a ton of output, or errors, sorry. Thats just because when importing from GitHub, it locks the files. Meaning we can't delete it without giving ourselves permission.")
                                    print(f"Successfully removed module {module}.")
                            else:
                                print(f"Module {module} is not downloaded.")
                        else:
                            print("No modules are downloaded.")
                    elif option == "4":
                        module = input("Module name (case sensitive): ")
                        args = input("Arguments (leave blank for none): ")
                        vbout("loading lol")
                        current_script = Path(__file__).resolve()
                        parent_dir = Path(current_script.parent).resolve()
                        modules_dir = Path(parent_dir / "Modules").resolve()
                        ModuleDir = Path(modules_dir / module).resolve()
                        modulemainfile = Path(ModuleDir / "main.py").resolve()
                        if os.path.exists(modules_dir):
                            if os.path.exists(ModuleDir):
                                if ModuleDir not in sys.path:
                                    sys.path.insert(0, ModuleDir)
                                if os.path.exists(modulemainfile):
                                    if args == '':
                                        print(f'{sys.executable} "{modulemainfile}"')
                                        os.system(f'{sys.executable} "{modulemainfile}"')
                                    else:
                                        args = args.split()
                                        print(f'{sys.executable} "{modulemainfile}" {args}')
                                        os.system(f'{sys.executable} "{modulemainfile}" {args}')
                                else:
                                    print("The module does not include a main.py file. This is not your fault.")
                            else:
                                print(f"Module {module} is not installed.")
                        else:
                            print("No modules are installed.")
                    elif option == "5":
                        module = input("Module name (case sensitive): ")
                        current_script = Path(__file__).resolve()
                        parent_dir = current_script.parent
                        modules_dir = parent_dir / "Modules"
                        if os.path.exists(modules_dir):
                            ModuleDir = modules_dir / module
                            if os.path.exists(ModuleDir):
                                print(f"Would remove and reinstall {ModuleDir}" + "\\" + "*")
                                confirm = input(f"Are you sure you would like to update the module {module}? [y/n]: ")
                                if confirm == 'y':
                                    shutil.rmtree(ModuleDir, onerror=remove_module_error)
                                    vb_clear_screen()
                                    print("If you got a ton of output, or errors, sorry. Thats just because when importing from GitHub, it locks the files. Meaning we can't delete it without giving ourselves permission.")
                                    print(f"Successfully removed module {module}.")
                                    print("Downloading module...")
                                    install_codeon_module(module)
                            else:
                                print(f"Module {module} is not downloaded.")
                        else:
                            print("No modules are downloaded.")
                    elif option == "6":
                        module = input("Module name (just repository name and case sensitive): ")
                        username = input("Username of the owner of the repository you'd like to update (case sensitive): ")
                        current_script = Path(__file__).resolve()
                        parent_dir = current_script.parent
                        modules_dir = parent_dir / "Modules"
                        if os.path.exists(modules_dir):
                            ModuleDir = modules_dir / module
                            if os.path.exists(ModuleDir):
                                print(f"Would remove {ModuleDir}" + "\\" + "*")
                                confirm = input(f"Are you sure you would like to update the module {module}? [y/n]: ")
                                if confirm == 'y':
                                    vbout("removing module")
                                    shutil.rmtree(ModuleDir, onerror=remove_module_error)
                                    vb_clear_screen()
                                    print("If you got a ton of output, or errors, sorry. Thats just because when importing from GitHub, it locks the files. Meaning we can't delete it without giving ourselves permission.")
                                    print(f"Successfully removed module {module}.")
                                    print("Downloading module...")
                                    vbout("starting unofficial download")
                                    install_codeon_module_unofficial(username, module)
                            else:
                                print(f"Module {module} is not downloaded.")
                        else:
                            print("No modules are downloaded.")
                    elif option == "7":
                        continue
                    else:
                        print("Invalid option.")
                elif "dwheel " in program:
                    duration = program.removeprefix("dwheel ")
                    try:
                        duration = float(duration)
                        dwheel(duration)
                    except:
                        print("Traceback: Duration is not written in seconds.")
                else:
                    print("Traceback: Unknown Command")

            except Exception as e:
                print("There was a python error, most likely due to me.")
                print("Please send an email to developerv0002@gmail.com with the error.")
                print("You can also submit a pull request on the GitHub repository you got the software from.")
                print("We will fix it as soon as possible and return a version to fix your error.")
                print("Error: ", e)
                print("Please wait while we report the issue to our web server...")
                wheel = threading.Thread(target=ewheel)
                report = threading.Thread(target=reporterror, args=[e])
                wheel.start()
                report.start()
                break

    if __name__ == "__main__":
        main()
main2()
