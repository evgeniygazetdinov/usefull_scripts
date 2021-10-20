# -*- coding: utf-8 -*-
import os

def get_current_terminal_language():
    """
        get current phrase for search
        depend on current terminal language
    """
    data = {
        'ru:en_US:en': 'изменено'
        #TODO ADD ENGLISH HERE
    }
    res = os.popen('echo $LANGUAGE')
    print(res)
    return data[res]
  
def python_file_finder():
    lines  = os.popen('git status | grep -i {}'.format(get_current_terminal_language())).readlines()
    # add check on py
    data = [line.split()[-1] for line in lines]
    print(data)

def check_on(corrector, file):
  return ""
    
def main():
  files = python_file_finder()
  map(check_on, files) # pylint
  map(check_on, files) # flake8
  map(check_on, files) # mypy

if __name__ == "__main__":
   main()
    
