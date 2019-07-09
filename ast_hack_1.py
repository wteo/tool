# -*- coding:utf-8 -*-
# Author: woootao@gmail.com
# Date  : 2019/7/8
# Note  :

import ast
import os
import textwrap


def _extract_scripts_from_project(setup_filename='setup.py'):
    """Parse setup.py and return scripts"""
    if not os.path.isfile(setup_filename):
        return ''
    mock_setup = textwrap.dedent('''\
    def setup(*args, **kwargs):
        __setup_calls__.append((args, kwargs))
    ''')
    parsed_mock_setup = ast.parse(mock_setup, filename=setup_filename)
    with open(setup_filename, 'rt') as setup_file:
        parsed = ast.parse(setup_file.read())
        for index, node in enumerate(parsed.body[:]):
            if (not isinstance(node, ast.Expr) or
                    not isinstance(node.value, ast.Call) or
                    node.value.func.id != 'setup'):
                continue
            parsed.body[index:index] = parsed_mock_setup.body
            break
    fixed = ast.fix_missing_locations(parsed)
    codeobj = compile(fixed, setup_filename, 'exec')
    local_vars = {}
    global_vars = {'__setup_calls__': []}
    exec(codeobj, global_vars, local_vars)
    _, kwargs = global_vars['__setup_calls__'][0]
    return ','.join([os.path.basename(f) for f in kwargs.get('scripts', [])])
