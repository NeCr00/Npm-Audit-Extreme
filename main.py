from audit_code import  audit_code
import sys


def getUserArguments():
    if  len(sys.argv) !=2:
        print("Please provide a path as an argument.")
        exit(1)
    
    return sys.argv[1]

def main ():
    project_path = getUserArguments()
    print(project_path)
    scan = audit_code(project_path)


if __name__ == '__main__':
    main()