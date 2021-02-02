import shlex
import os


if __name__ == "__main__":
    while True:
        inp = input("shell> ")
        ls = shlex.split(inp)
        pid = os.fork()
        if pid > 0:
            os.wait()
        else:
            print(os.getpid(),os.getppid())
            os.execvp(ls[0],ls)
            
