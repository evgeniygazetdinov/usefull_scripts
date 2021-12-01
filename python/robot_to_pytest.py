import argparse
import re
from typing import List
import os
import sys


VAR_PREFIX = '__var__'
result: List[str] = []
class_variables: List[str] = []


def write_test_file(file_name: str, file_path: str):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(os.path.join(file_path, 'test_' + file_name + '.py'), 'w') as file:
        for line in result:
            file.write(line + '\n')


def snake_to_camel(name):
    return ''.join(word.title() for word in name.split('_'))


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def generate_common_head(file_name: str):
    result.append('"""\n\n"""')
    result.append('from tests.api_pytest.common import BaseTestClass')
    result.append('\n')
    class_name = snake_to_camel(file_name)
    result.append(f'class Test{class_name}(BaseTestClass):')
    result.append('\t"""\n\n\t"""')


def clear_variable(variable:str, add_prefix: bool = True):
    variable = variable.strip()
    if '${' in variable or '&{' in variable:
        var_clear = (VAR_PREFIX if add_prefix else '') + variable.replace('${', '').replace('&{', '').replace('}', '')
        return var_clear.replace('none', 'None')
    return variable


def parse_to_key_value(line):
    key, value = line.split('=')
    value = clear_variable(value)
    val_cl = value.replace(VAR_PREFIX, '')
    if not val_cl.startswith('0') and val_cl.isdigit():
        value = int(val_cl)

    return key, value


def save_dict(d: dict, d_name: str, tabs: str = '\t'):
    dict_lines = ['{} = {}'.format(d_name, '{')]
    if tabs == '\t':
        class_variables.append(d_name)
    for key, value in d.items():
        if isinstance(value, int):
            dict_lines.append(f"\t'{key}': {value},")
        elif VAR_PREFIX in value:
            dict_lines.append(f"\t'{key}': {value.replace(VAR_PREFIX, '')},")
        else:
            dict_lines.append(f"\t'{key}': '{value}',")
    dict_lines.append('}')
    dict_lines = [tabs + i for i in dict_lines]
    return dict_lines


def when_request(line: str, method: str):
    line_parts = line.split(f'  when {method} request  ')
    result_line = clear_variable(line_parts[0], False)
    result_line += f' self.{method}('
    request_params = line_parts[1].split('  ')
    for part in request_params:
        part = part.strip()
        if part == '${sc_api_alias}':
            continue
        arg = part
        if '=' in part:
            arg_parts = part.split('=')
            result_line += arg_parts[0] + '='
            arg = arg_parts[1]
        arg_clear = clear_variable(arg)
        if VAR_PREFIX in arg_clear:
            arg = arg_clear.replace(VAR_PREFIX, '')
            arg_pref = 'self.' if arg in class_variables else ''
            result_line += arg_pref + arg + ', '
        else:
            result_line += f"'{arg}', "

    result_line += 'with_response_validation=True)'
    return result_line


def generate_func(func_name: str, func_lines: List[str], func_prop: dict):
    result.append('')
    arguments = func_prop.get('arguments')
    if arguments:
        arguments_line = ', '.join(arguments)
        result.append(f'\tdef {func_name}(self, {arguments_line}):')
    else:
        result.append(f'\tdef {func_name}(self):')
    result.append('\t\t"""')
    doc = func_prop.get('Documentation', '')
    result.append(f'\t\t{doc}')
    if arguments:
        for argument in arguments:
            arg_doc = argument
            if '=' in arg_doc:
                arg_doc = arg_doc.split('=')[0]
            result.append(f'\t\t:param {arg_doc}:')
    result.append('\t\t:return:')
    result.append('\t\t"""')
    result.append('')

    for line in func_lines:
        result.append(line)


def get_from_dictionary(line: str):
    line_parts = line.split('  get from dictionary  ')
    result_line = clear_variable(line_parts[0], False)
    d, key = line_parts[1].split('  ')
    result_line += f" {clear_variable(d, False)}['{key}']"
    return result_line


def dictionary_should_contain_key(line: str):
    line = line.replace('dictionary should contain key  ', '')
    parts = line.split('  ')
    result_line = f"assert '{parts[1]}' in {clear_variable(parts[0], False)}"
    if len(parts) > 2:
        result_line += f" '{parts[2]}'"
    return result_line


def set_to_dictionary(line: str):  # не обрабатывает все случаи
    try:
        line_sp = line.replace('set to dictionary  ', '')
        dict_name, pair = line_sp.split('  ')
        dict_name = clear_variable(dict_name, False)
        dict_name = ('self.' if dict_name in class_variables else '') + dict_name
        key, value = pair.split('=')
        return f"{dict_name}['{key}'] = {clear_variable(value, False)}"
    except:
        return line


def create_dictionary(line: str):
    var, pairs = line.split('create dictionary')

    d_name = clear_variable(var, False).replace('=', '').strip()
    pairs_list = pairs.strip().split('  ')
    d = {}
    for pair in pairs_list:
        key, value = parse_to_key_value(pair)
        d[key] = value
    return save_dict(d, d_name, '\t\t')


def generate_funcs(keywords: List[str], prefix: str = ''):

    current_func_properties = {}
    current_func_lines: List[str] = []
    current_func_name = ''
    for keyword in keywords:
        keyword_with_case = keyword
        keyword = keyword.lower().rstrip()
        if keyword.startswith(('  ', '\t')):
            keyword = keyword.lstrip()
            res_str = ''
            found = False
            for prop in ['Documentation', 'Tags']:
                prop_name = f'[{prop}]'
                if prop_name in keyword_with_case:
                    current_func_properties[prop] = keyword_with_case.replace(prop_name, '').strip()
                    found = True
                    continue
            if found:
                continue

            if '[arguments]' in keyword:
                parts = keyword.replace('[arguments]  ', '').split('  ')
                arguments = [clear_variable(i, False) for i in parts]
                current_func_properties['arguments'] = arguments
                continue

            if 'when get request' in keyword:
                res_str = when_request(keyword, 'get')

            if 'when post request' in keyword:
                res_str = when_request(keyword, 'post')

            matched = re.match('expect .* has status 200', keyword)
            if matched:
                continue  # предполагаем что статус при запросе проверяется

            if '[return]' in keyword:
                res_str = clear_variable(keyword.replace('[return]  ', 'return ')).replace(VAR_PREFIX, '')

            if 'get from dictionary' in keyword:
                res_str = get_from_dictionary(keyword)

            matched = re.match('dictionary (.*) should contain ([\d]*) keys', keyword)
            if matched:
                res_str = f'assert len({clear_variable(matched.group(1), False)}.keys()) == {matched.group(2)}'

            if 'dictionary should contain key' in keyword:
                res_str = dictionary_should_contain_key(keyword)

            if 'should be true' in keyword:  # не дописан! Надо будет вручную кавычки расставить где надо
                res_str = clear_variable(keyword.replace("should be true  '", 'assert '), False).replace("'", '')

            if 'set to dictionary' in keyword:
                set_to_dictionary(keyword)

            if 'create dictionary' in keyword:
                dict_lines = create_dictionary(keyword)
                current_func_lines += dict_lines
                continue

            if 'set test variable' in keyword:
                current_func_lines.append(f"\t\t'{keyword}'")  # по идее надо фикстуры делать, возможно слишком трудоемко
                continue

            if not res_str:  # скорее всего это вызов метода, тут тоже возможно придется кавычки расставить
                keyword = keyword.replace('when ', '').replace('then ', '').replace('and ', '')  # превратим в обычные функции
                parts = keyword.split('  ')
                if '=' in parts[0]:
                    res_str = clear_variable(parts.pop(0), False) + ' '  # присвоение переменной
                res_str += 'self.' + parts.pop(0).replace(' ', '_') + '('  # название метода

                for part in parts:
                    arg = part
                    if '=' in part:
                        arg_parts = part.split('=')
                        res_str += arg_parts[0] + '='
                        arg = arg_parts[1]
                    arg_clear = clear_variable(arg)
                    arg = arg_clear.replace(VAR_PREFIX, '')
                    arg_pref = 'self.' if arg in class_variables else ''
                    res_str += arg_pref + arg + ', '
                if parts:
                    res_str = res_str[:-2]
                res_str += ')'

            current_func_lines.append('\t\t' + res_str)
        else:
            if current_func_name:
                generate_func(current_func_name, current_func_lines, current_func_properties)
            current_func_name = f'{prefix + keyword.replace(" ", "_")}'
            current_func_properties.clear()
            current_func_lines.clear()
    if current_func_name:
        generate_func(current_func_name, current_func_lines, current_func_properties)


def generate_variables(variables: List[str]):
    global result
    variable_type = ''
    current_dict = {}
    current_dict_name = ''
    for variable in variables:
        if variable.startswith('&'):
            variable_type = 'dict'
            if current_dict:
                dict_list = save_dict(current_dict, current_dict_name)
                result += dict_list
                current_dict = {}

        elif variable.startswith('$'):
            variable_type = 'str'
            if current_dict:
                dict_list = save_dict(current_dict, current_dict_name)
                result += dict_list
                current_dict = {}

        if variable_type == 'str':
            variable_parts = variable.split('  ')
            variable_name = clear_variable(variable_parts[0], False)
            variable_value = variable_parts[-1].strip()
            if variable_value.isdigit():
                result.append(f'\t{variable_name} = {variable_value}')
            else:
                result.append(f"\t{variable_name} = '{variable_value}'")
            class_variables.append(variable_name)
            continue

        if variable_type == 'dict':
            if variable.startswith('...'):  # продолжение словаря
                variable = variable.replace('...', '').strip()
                key, value = parse_to_key_value(variable)
                current_dict[key] = value
            else:
                variable_parts = variable.split('  ')
                current_dict_name = variable_parts[0].replace('&{', '').replace('}', '').replace('=', '').strip()
                variable_first_value = variable_parts[-1].strip()
                key, value = parse_to_key_value(variable_first_value)
                current_dict[key] = value
    if current_dict:
        dict_list = save_dict(current_dict, current_dict_name)
        result += dict_list


def collect_group(line: str, group: list, collect: bool = False):
    if line.startswith("***"):
        return True
    if collect and '...' in line:
        group[-1] = group[-1] + '  ' + line.replace('...', '').strip()
    else:
        group.append(line)


paths = [
    # './tests/api/scenarios/billing/lbs_tariff_info.robot',
    # './tests/api/scenarios/address/address_edit.robot',
    # './tests/api/scenarios/apiv1/api_get_pdfmarks.robot'
]
paths += sys.argv[1:]

for path in paths:
    tests = []
    keywords = []
    variables = []
    result = []
    with open(path) as file:
        first_search = True

        file_name = path[path.rfind('/')+1: -6]
        new_file_path = os.path.dirname(path).replace('api/scenarios', 'api_pytest')
        tests_end = False
        keywords_end = False
        variables_end = False
        for line in file:
            # Пропускаем всё до группы тестов
            if first_search and '*** Test Cases ***' not in line or not line.strip():
                continue
            first_search = False

            # Начинается группа тестов
            if '*** Test Cases ***' in line:
                continue

            if not tests_end:
                tests_end = collect_group(line, tests, True)
                continue

            # Начинается группа общих методов
            if not keywords_end:
                keywords_end = collect_group(line, keywords, True)
                continue

            # Начинается группа тестов
            if not variables_end:
                variables_end = collect_group(line, variables)

if __name__ == '__main__':
    generate_common_head(file_name)
    generate_variables(variables)
    generate_funcs(keywords)
    generate_funcs(tests, 'test_')
    write_test_file(file_name, new_file_path)
