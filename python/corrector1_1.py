import os
import sys

from git import Repo

PYLINT = 'pylint'
FLAKE = 'flake8'
MYPY = 'mypy'

STANDART_CALLS = [PYLINT, FLAKE]
STORECRAFT_CALLS = [PYLINT, FLAKE, MYPY]

BILLING_PATH = '/Users/ev/code/billing'
STORECRAFT_PATH = '/Users/ev/code/storecraft'

BILLING_CONFIG = {'calls': STANDART_CALLS, 'dir': BILLING_PATH}


def billing_calls(func):
    def wrapper():
        func(call_types=STANDART_CALLS)
    return wrapper

def storecraft(func):
    def wrapper():
        func(call_types=STANDART_CALLS)
    return wrapper 


@billing_calls
def call_linter(file=False, call_types=False):
    print(f'cal types from decorator {call_types}')

def get_files_from_diff(files_path):
    repo = Repo(files_path)
    return [ item.a_path for item in repo.index.diff(None)]

def make_string_for_linter_call(files_path):
    diff_files = get_files_from_diff(files_path)
    return ' '.join(diff_files)

def prepare_files(files_path):
    string_for_linter = make_string_for_linter_call(files_path)
    return string_for_linter

def run_linter(linter_type, files):
    os.system(f'{linter_type} {files}')

def linter_it(linter_list, string_with_files):
    for linter in linter_list:
        run_linter(linter, string_with_files)

def main():
    config = BILLING_CONFIG
    files = prepare_files(config['dir'])
    linter_it(config['calls'], files)


if __name__ == '__main__':
    main()
