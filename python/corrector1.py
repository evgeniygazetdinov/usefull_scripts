#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import os
import subprocess
import sys

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
  
def is_python_file(file):
    if file.endswith('.py'):
        return True
    return False

def python_file_finder():
    lines  = os.popen('git status | grep -i изменено').readlines()
    # add check on py
    data =  [(line.split(' ')[-1]).split('\n') for line in lines]
    
    without_n = [line[0] for line in data]
    print(without_n)
    return without_n

def check_on(corrector, file):
    output = subprocess.getoutput("{} {}".format(corrector, file))
    print(output)

def correct_runner(files):
   for file in files:
      if file is not None:
    
        print("\t")
        print('*'*10,file,'*'*10) 
        print("*"*10 + pylint +"*"*10)
        check_on('pylint', file)
        print("*"*10 + flake8 +"*"*10)
        check_on('flake8', file)
        print("*"*10 + mypy +"*"*10)
        check_on('mypy', file)
        print("*"*10 + "-"*5 + "END" +"-"  +"*"*10)
        print("\t")

def main():
  if len(sys.argv) == 2:
     print(sys.argv)
     correct_runner([sys.argv[1]])    
  else:
     files = python_file_finder()
     correct_runner(files)

if __name__ == "__main__":
    main()
    
