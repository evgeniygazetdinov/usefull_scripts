#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3
import os
import sys

from git import Repo

PYLINT = 'pylint'
FLAKE = 'flake8'
MYPY = 'mypy'
BILLING_FLAG = '-b'

STANDART_CALLS = [PYLINT, FLAKE]
STORECRAFT_CALLS = [PYLINT, FLAKE, MYPY]

BILLING_PATH = '/Users/ev/code/billing'
STORECRAFT_PATH = '/Users/ev/code/storecraft'

BILLING_CONFIG = {'calls': STANDART_CALLS, 'dir': BILLING_PATH}
STORECRAFT_CONFIG = {'calls': STORECRAFT_CALLS, 'dir': STORECRAFT_PATH}


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
    files = [ item.a_path for item in repo.index.diff(None)]
    only_py = [f for f in files if f.endswith('.py')]
    return only_py

def make_string_for_linter_call(files_path):
    diff_files = get_files_from_diff(files_path)
    # filter only py files
    print(diff_files)
    return ' '.join(diff_files)

def prepare_files(files_path):
    string_for_linter = make_string_for_linter_call(files_path)
    return string_for_linter

def run_linter(linter_type, files):
    os.system(f'{linter_type} {files}')

def linter_it(linter_list, string_with_files):
    for linter in linter_list:
        print(20 * '*', f'call {linter}', 20 * '*')
        run_linter(linter, string_with_files)

def find_config_by_path():
    pass

def run_configuration(config, file):
    if file:
        linter_it(config['calls'], file)
    else:
        files = prepare_files(config['dir'])
        linter_it(config['calls'], files)

def main(config, file=False):
    # TODO FIND CONFIG BY PATH
    print(config)
    run_configuration(config, file)


if __name__ == '__main__':
    print(os.path.dirname(os.path.realpath(__file__)))
    config = STORECRAFT_CONFIG
    if BILLING_FLAG in sys.argv:
        config = BILLING_CONFIG
        print('accepted billing config')
    if len(sys.argv) > 1 and sys.argv[1] != BILLING_FLAG:
        print('get logic for separated file')
        file = sys.argv[1]
        main(config, file)
    else:
       main(config)
