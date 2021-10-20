# -*- coding: utf-8 -*-
import os
import subprocess

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
    print(data)

def check_on(corrector, file):
  return ""

def main():
  files = python_file_finder()
#  map(check_on, 'pylint', files) # pylint
#  map(check_on, 'flake8', files) # flake8
#  map(check_on, 'mypy', files) # mypy

if __name__ == "__main__":
   main()

