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

completer = MyCompleter(['cd','pwd','exit','cd ..','ls','bg','bglist','bgkill','bgstop','bgstart','ping','ls -l','cat'])
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
    
    else:
        pid = os.fork()
        if pid == 0:
            try:
                os.execvp(ls[1],ls[1:])
            except Exception as e:
                print(e)
        bg_list.append([' '.join(ls[1:]),pid,'Running',os.getcwd()])
        

    return bg_list

def check_bg():
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
        print("({})-({})-({})  {}\n".format(index+1,a[2],a[0],a[3]))
        index = index + 1
    print("Total Background jobs : {}\n".format(index))


if __name__ == "__main__":
    while True:
        
        try:
            inp = input("shell> ")
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
                    print(pwd)
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
            print('Index not found')
        except KeyboardInterrupt as e:
            print(e)
            exit(0)
        except EOFError as e :
            #print(e)
            exit(0)
        except Exception as e:
            print(e)
