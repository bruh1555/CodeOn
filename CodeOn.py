codeonversion = "0.5"
import time
import os
import sys
import ctypes
import requests
from pathlib import Path
import checkinternet
import gnv as gnv

def set_console_title(title):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)
def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def getlatestversionfunc():
    current_script = Path(__file__).resolve()
    parent_dir = current_script.parent
    target_script_path = None
    
    for root, dirs, files in os.walk(parent_dir):
        if "updatecon.py" in files:
            target_script_path = Path(root) / "updatecon.py"
            break
    
    if target_script_path:
        os.system(f'python {target_script_path}')
        print("Welcome back! We are reloading CodeOn to receive the data retrieved from the updater.")
        script_path = os.path.abspath(__file__)
        os.execv(sys.executable, ['python'] + [script_path])
    else:
        print("ACTION REQUIRED: THE FILE 'updatecon.py' CANNOT BE FOUND. PLEASE REDOWNLOAD CODEON TO FIX THIS ISSUE.")
        sys.exit()

print("Starting CodeOn.......")
time.sleep(2)
print("Checking your internet connection...")
returncheck = checkinternet.check()
if returncheck == "False":
    print("Error: You are not connected to the internet. CodeOn requires an internet connection. Please try again later when you have one.")
    sys.exit()
time.sleep(2)
print("Checking for new versions...")
latest_version = gnv.gnv()
if "Error: " in latest_version:
    print(f"Error checking for updates. Manually check by going to https://raw.githubusercontent.com/bruh1555/CodeOn/main/latest_version.txt and checking if {codeonversion} is the version. CodeOn will not work if we cannot get the latest version.")
    sys.exit()
else:
    latest_version = float(latest_version)
    if not float(codeonversion) == latest_version:
        print("You do not have the latest version.")
        print(f'Version of current CodeOn: {codeonversion}')
        print(f'Latest CodeOn Version: {latest_version}')
        print("Getting latest version...")
        getlatestversionfunc()
    else:
        time.sleep(3)
        set_console_title('CodeOn Command Line')
        print("Welcome to the CodeOn command line! Type in the command 'help' for help.")
        time.sleep(1)
        clear_screen()
        newcodeonversion = "0.5"

        def parse(program):
            tokens = program.split()
            if not tokens:
                return None
            command = tokens[0]
            if command == 'createfile':
                if len(tokens) == 2:
                    return ('createfile', tokens[1], None)
                elif len(tokens) > 2:
                    return ('createfile', tokens[1], ' '.join(tokens[2:]))
                else:
                    print("Invalid command syntax for createfile")
            elif command == 'createfolder':
                if len(tokens) == 3:
                    return ('createfolder', tokens[1], tokens[2])
                else:
                    print("Invalid command syntax for createfolder")
            elif command == 'editfile':
                if len(tokens) == 2:
                    return ('editfile', tokens[1])
                else:
                    print("Invalid command syntax for editfile")
            else:
                print("Unknown command: ", command)
            return None

        def create_file():
            filepath = input("Enter the path of the file to create (don't include quotation marks): ")
            filename = input("What should the file name be: ")
            content = input("What should the content be (notice this will only be one line so you must use the editfile command to do multiple lines): ")
            full_path = os.path.join(filepath, filename)
            with open(full_path, "w") as file:
                if content is not None:
                    file.write(content)
                    print(f"File '{filename}' created with content at '{filepath}'.")
                else:
                    print(f"File '{filename}' created at '{filepath}'.")

        def create_folder(folder_path, folder_name):
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
                            break
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
                    program = input("CodeOn>> ")
                    if program == "exit":
                        print("Exiting command line...")
                        break
                    elif program == "help":
                        print("Commands available:")
                        print("- 'exit': exit the command line")
                        print("- 'help': display this help message")
                        print("- 'help all': display all help commands")
                        print("- 'clear': clear your environment you are running CodeOn in.")
                        print("- 'createfile': create a file with the content, if the file has no content, it will be set to the default")
                        print("- 'createfolder': create a folder")
                        print("- 'editfile': edit a file")
                        print("- 'reload': reload CodeOn")
                        print("- 'read': read a file made of CodeOn commands (not finished)")
                        print("- 'helpread': display help to write a file for the read command")
                        print("- 'print <contents>': print the string you wrote")
                        print("- 'math <+ - * /> <num1> <num2>': do a math problem")
                        print(f"- 'info': get info about your current CodeOn version.")
                        print("To get more information, use the command 'help all'")
                        continue
                    elif program == "help all":
                        print("update notes: added 6 new commands -info -os -user -ncon -py -vmcon")
                        print("slowly working on this (will not be finished fast)")
                        print("Commands available:")
                        print("- 'exit': exit the command line")
                        print("- 'help': display the shortened help message (doesn't include all commands)")
                        print("- 'help all': display this help message")
                        print("- 'clear': clear your environment you are running CodeOn in.")
                        print("- 'createfile': create a file with the content, if the file has no content, it will be set to the default")
                        print("- 'createfolder': create a folder")
                        print("- 'editfile': edit a file")
                        print("- 'reload': reload CodeOn")
                        print("- 'read': read a file made of CodeOn commands (not finished)")
                        print("- 'helpread': display help to write a file for the read command")
                        print("- 'print <contents>': print the string you wrote")
                        print("- 'math <+ - * /> <num1> <num2>': do a math problem")
                        print(f"- 'info': get info about your current CodeOn version.")
                        print("- 'os': please type in 'os' to get information about this command. (i'm too lazy to type it all in here lol)")
                        print("- 'user': get the current logged in user")
                        print("- 'ncon': open another CodeOn console")
                        print("- 'py': open a python console")
                        print("- 'py <location>: open a python script")
                        print("- 'vmcon': open a CodeOn console within the current one (testing purposes, but can be used for stopping errors from closing the console)")
                        print("- 'rstcon': reset CodeOn (redownload using update service)")
                        continue
                    elif program == "clear":
                        clear_screen()
                        continue
                    if program == "":
                        continue
                    elif program == "editfile":
                        edit_file()
                    elif program == "createfile":
                        create_file()
                    elif program == "createfolder":
                        folder_name = input("Enter the name of the folder: ")
                        folder_path = input("Enter the path where the folder should be created (don't include quotation marks): ")
                        create_folder(folder_path, folder_name)
                    elif program == "reload":
                        clear_screen()
                        script_path = os.path.abspath(__file__)
                        os.execv(sys.executable, ['python'] + [script_path])
                    elif program == "read":
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
                            print("ACTION REQUIRED: THE FILE 'CodeOn file runner.py' CANNOT BE FOUND. PLEASE REDOWNLOAD CODEON TO FIX THIS ISSUE.")
                            sys.exit()
                    elif program == "helpread":
                        print("Commands available for reading a file:")
                        print("- 'exit': exit the file")
                        print("- 'clear': clear console")
                        print("- 'print <contents>': print the string you wrote")
                        print("- 'math <+ - * /> <num1> <num2>': do a math problem")
                    elif program == "info":
                        print("Info about CodeOn:")
                        print(f'CodeOn {newcodeonversion}')
                        print("Cross-platform Version")
                        print("CodeOn was made using Python.")
                        print("If you get any Python errors, please report them by emailing developerv0002@gmail.com and including the Python error.")
                        print("You may also submit a pull request on the GitHub repository you got the software from.")
                        print("We will fix it as soon as possible and return a version to fix your error.")
                    elif "print " in program:
                        arguments = program.split()
                        print(' '.join(arguments[1:]))
                    elif "math " in program:
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
                                program2 = program[9:]
                                os.system(program2)
                            elif arguments[1] == "shutdown":
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
                                    print("Usage:")
                                    print("s - shutdown the device")
                                    print("r - restart the device")
                                    print("l - logoff (Windows only)")
                        else:
                            print("Usage:")
                            print("syscmd - call a command on your system.")
                            print("shutdown <s, r, l> - shutdown your system using a specific method")
                    elif program == "user":
                        if os.name == 'nt':
                            os.system('whoami')
                        else:
                            os.system('id -un')
                    elif program == "py":
                        os.system("python3")
                    elif "py" in program:
                        program2 = program[3:]
                        os.system(f'python3 {program2}')
                    elif program == "ncon":
                        script_path = os.path.abspath(__file__)
                        if os.name == 'nt':
                            os.system(f'start cmd /K python {script_path}')
                        else:
                            os.system(f'gnome-terminal -- python {script_path}')
                    elif "cmdtitle" in program:
                        if os.name == 'nt':
                            program2 = program[9:]
                            set_console_title(f'{program2} - CodeOn')
                    elif program == "vmcon":
                        script_path = os.path.abspath(__file__)
                        os.system(f'python {script_path}')
                    elif program == "rstcon":
                        getlatestversionfunc()
                    else:
                        print("Traceback: Unknown Command")
                    
                    if os.name == 'nt':
                        buffer = ctypes.create_unicode_buffer(1024)
                        ctypes.windll.kernel32.GetConsoleTitleW(buffer, 1024)
                        current_title = buffer.value
                        if not current_title.endswith(" - CodeOn"):
                            set_console_title(f'{current_title} - CodeOn')

                except EOFError:
                    print("Python Error Occurred.")
                    break

if __name__ == "__main__":
    main()
