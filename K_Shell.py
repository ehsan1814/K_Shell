import os
import sys
import shlex
import signal
import readline


bg_list = []

class MyCompleter(object):  

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options 
                                    if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try: 
            return self.matches[state]
        except IndexError:
            return None

completer = MyCompleter(['cd','pwd','exit','cd ..','ls','bg','bglist','bgkill','bgstop','bgstart','ping','ls -l','cat','clear'])
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')


def bg(ls):
    char = ls[0]

    if char == 'bgkill':
        process_index = int(ls[1]) - 1
        os.kill(bg_list[process_index][1],signal.SIGTERM)
        del bg_list[process_index]
    
    elif char == 'bgstop':
        process_index = int(ls[1]) - 1
        os.kill(bg_list[process_index][1],signal.SIGSTOP)
        bg_list[process_index][2] = 'Waiting'
    
    elif char == 'bgstart':
        process_index = int(ls[1]) - 1
        os.kill(bg_list[process_index][1],signal.SIGCONT)
        bg_list[process_index][2] = 'Running'
    
    elif char == 'bglist':
        print_bg(bg_list)
    
    elif char == 'bg' and len(ls)>1:
        pid = os.fork()
        if pid == 0:
            try:
                os.execvp(ls[1],ls[1:])
            except:
                if pid == 0:
                    os._exit(0)
                    raise Exception('command not work')
        else:
            bg_list.append([' '.join(ls[1:]),pid,'Running',os.getcwd()])
    else:
        raise Exception('command not found')


def check_bg():
    # os.waitpid() method returns a tuple 
    # first attribute represents child's pid 
    # while second one represents 
    # exit status indication

    #The waitpid function is used to request status information 
    #from a child process whose process ID is pid . ... You can 
    #use the WNOHANG flag to indicate that the parent process 
    #shouldn't wait

    try:
        for i in range(len(bg_list)) :
            st,st2 = os.waitpid(int(bg_list[i][1]),os.WNOHANG)
            a = os.WIFSIGNALED(st)
            if a:
                del bg_list[i]
    except:
        pass

def print_bg(ls):

    index = 0
    for a in ls :
        print(colored(0,0,255,"({})-({})-({})  {}\n".format(index+1,a[2],a[0],a[3])))
        index = index + 1
    print(colored(255,128,0,"Total Background jobs : {}\n".format(index)))

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

if __name__ == "__main__":
    while True:
        
        try:
            inp = input(colored(255,0,0,"{} ".format(os.getcwd())))
            #inp = input(colored(255, 0, 0, 'shell> '))
            ls = shlex.split(inp)
            
            if len(ls) == 0:
                continue
            
            char = ls[0]
            #we have quit and exit function
            if char == 'exit' :
                quit()
        
            if char == 'cd' or char == 'pwd':
                pwd = os.getcwd()
                if char == 'pwd':
                    print(colored(0,255,0,pwd))
                    continue

                os.chdir(ls[1])
            elif 'bg' in char:
                check_bg()
                bg(ls)
            else:
                pid = os.fork()
                if pid > 0:
                    os.wait()
                else:
                    os.execvp(char,ls)
                    
        except IndexError:
            print(colored(255,128,0,'Index not found'))
        except KeyboardInterrupt as e:
            print(colored(255,128,0,e))
            exit(0)
        except EOFError as e :
            print(colored(255,128,0,e))
            exit(0)
        except Exception as e:
            print(colored(255,128,0,e))
