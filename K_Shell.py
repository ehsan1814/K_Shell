import shlex
import os
import sys


if __name__ == "__main__":
    while True:

        #print("shell>",end="")
        #inp = sys.stdin.readline()
        
        inp = input("shell> ")
        ls = shlex.split(inp)

        if len(ls) == 0:
            continue
        
        char = ls[0]
        print(ls)
        #we have quit and exit function
        if char == 'exit' :
            quit()
        
        try:
            if char == 'ls':
                pid = os.fork()
                if pid > 0:
                    os.wait()
                else:
                    #print(os.getpid(),os.getppid())
                    os.execvp(char,ls)
            elif char == 'cd' or char == 'pwd' or char == 'cd..':
                pwd = os.getcwd()
                if char == 'pwd':
                    print(pwd)
                    continue
                os.chdir(ls[1])
                
            else:
                print("Command not found")
        except Exception as e:
            print(e)
