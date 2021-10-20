# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import os
import subprocess

pylint = "pylint"
mypy = "mypy"
flake8 = "flake8"


def get_current_terminal_language():
    """
        get current phrase for search
        depend on current terminal language
    """
    data = {
        'ru:en_US:en': 'изменено',
        'ru_RU.UTF-8': 'изменено'
        #TODO ADD ENGLISH HERE
    }
    output = subprocess.getoutput("echo $LANG")
    return data[output]
  
def python_file_finder():
    lines  = os.popen('git status | grep -i {}'.format(get_current_terminal_language())).readlines()
    # add check on py
    data = [line.split()[-1] for line in lines]
    return data

def check_on(corrector, file):
    output = subprocess.getoutput("{} {}".format(corrector, file))
    print(output)

    
def main():
  files = python_file_finder()
  print("*"*10 + pylint +"*"*10)
  [check_on(pylint, file) for file in files if file is not None]
  print("*"*10 + flake8 +"*"*10)
  [check_on(flake8, file) for file in files if file is not None]
  print("*"*10 + mypy +"*"*10)
  [check_on(mypy, file) for file in files if file is not None]
  print("*"*10 + "-"*5 + "END" +"-"  +"*"*10)

if __name__ == "__main__":
    main()

