import os

PYLINT = 'pylint'
FLAKE = 'flake8'
MYPY = 'mypy'

STANDART_CALLS = [PYLINT, FLAKE]
STORECRAFT_CALLS = [PYLINT, FLAKE, MYPY]


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
    # os.system(f'{linter_type} {file}')

def check_files_quantity(files):
    pass

def make_string_for_linter_call():
    pass

def prepare_files(files):
    quantity_generator = check_files_quantity(files)
    string_for_linter = make_string_for_linter_call(quantity_generator, files)
    return string_for_linter

if __name__ == '__main__':
    call_linter()
