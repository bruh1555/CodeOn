import os
import sys
import time

variables = {
}

file = input("What would you like to open to run in CodeOn commands: ")
f = open(file, 'r')
lines = f.readlines()
os.system("cls")
print("Reading file...")
time.sleep(0.5)
os.system("cls")

def exit():
    script_path2 = "C:\\Users\\royce\\OneDrive\\Desktop\\codinghacking stuff\\CodeOn\\CodeOn for windows.py"
    script_path = '"' + script_path2 + '"'
    os.system('python3 ' + script_path)
    sys.exit()


def main():
    for line_number, v in enumerate(lines, start=1):
        if v == "exit":
            print("file done reading, exiting file...")
            exit()
        elif v == "clear":
            os.system('cls')
            continue
        elif "print " in v:
            arguments = v.split()
            if not arguments[1] == "var":
                print(arguments[1])
            else:
                if arguments[2] in variables:
                    print(variables[arguments[2]])
                else:
                    print(f'Traceback: [Line {line_number}] no such variable as {arguments[2]}')
                    exit()
        elif "math " in v:
            arguments = v.split()
            if arguments[1] == "+":
                floatednum1 = float(arguments[2])
                floatednum2 = float(arguments[3])
                output = floatednum1 + floatednum2
                print(arguments[2] + " + " + arguments[3] + " = " + str(output))
            elif arguments[1] == "-":
                floatednum1 = float(arguments[2])
                floatednum2 = float(arguments[3])
                output = floatednum1 - floatednum2
                print(arguments[2] + " - " + arguments[3] + " = " + str(output))
            elif arguments[1] == "*":
                floatednum1 = float(arguments[2])
                floatednum2 = float(arguments[3])
                output = floatednum1 * floatednum2
                print(arguments[2] + " * " + arguments[3] + " = " + str(output))
            elif arguments[1] == "/":
                floatednum1 = float(arguments[2])
                floatednum2 = float(arguments[3])
                output = floatednum1 / floatednum2
                print(arguments[2] + " / " + arguments[3] + " = " + str(output))
        elif "variable " in v:
                arguments = v.split()
                if arguments[2] == "math":
                    if arguments[3] == "+":
                        floatednum1 = float(arguments[4])
                        floatednum2 = float(arguments[5])
                        output = floatednum1 + floatednum2
                        variables[str(arguments[1])] = output
                    elif arguments[3] == "-":
                        floatednum1 = float(arguments[4])
                        floatednum2 = float(arguments[5])
                        output = floatednum1 - floatednum2
                        variables[str(arguments[1])] = output
                    elif arguments[3] == "*":
                        floatednum1 = float(arguments[4])
                        floatednum2 = float(arguments[5])
                        output = floatednum1 * floatednum2
                        variables[str(arguments[1])] = output
                    elif arguments[3] == "/":
                        floatednum1 = float(arguments[4])
                        floatednum2 = float(arguments[5])
                        output = floatednum1 / floatednum2
                        variables[str(arguments[1])] = output
                    else:
                        variables[str(arguments[1])] = "math"
                else:
                    variables[str(arguments[1])] = str(arguments[2])


if __name__ == "__main__":
    main()

lastline3 = len(lines)
lastline2 = lastline3 - 1
lastline = lines[lastline2]
if not lastline == "exit":
    print("Traceback (no ext): Expected exit at line " + str(lastline2) + ", you can clear this error by adding an exit statement at the end of your code.")
    endfile = input("Would you like to add an exit line to clear the error? (y/n)")
    if endfile == "y":
        with open(file, "a") as file_write:
            file_write.write("\nexit")
        exit()
    else:
        exit()

