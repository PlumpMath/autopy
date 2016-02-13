try:
    from configparser import SafeConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser

import os
from os import path
from subprocess import check_output, CalledProcessError
from setuptools import setup, find_packages

readme_extensions = [
    '',
    '.md',
    '.rst',
    '.txt',
]

ignore_files = set([
    'setup.py',
])


def ends_with(fname, end):
    """Returns True if `fname` ends with `end`, False otherwise.

    Both `fname` and `end` should be
    """
    return fname[-len(end):] == end


def read_requirements_file(filename):
    try:
        with open(filename) as f:
            return f.read().strip().split()
    except IOError:
        return []


def infer_from_git(options):

    def git_config(key, default=None):
        try:
            return check_output(['git', 'config', key]).strip()
        except CalledProcessError:
            return default

    options['author'] = git_config('user.name')
    options['author_email'] = git_config('user.email')

    for key in 'author', 'author_email':
        if options[key] is None:
            del options[key]


def infer_from_vcs(options):
    if path.exists('.git'):
        infer_from_git(options)


def infer_setup_options():

    options = {}

    options['packages'] = find_packages()

    long_desc = None
    for ext in readme_extensions:
        fname = 'README' + ext
        if not path.exists(fname):
            continue
        with open(fname) as f:
            long_desc = f.read()
            break

    if long_desc is not None:
        options['long_description'] = long_desc
        options['description'] = long_desc[:long_desc.find('\n')]

    dir_contents = os.listdir(os.curdir)

    py_files = []
    for fname in dir_contents:
        if ends_with(fname, '.py') and fname not in ignore_files:
            py_files.append(fname[:-len('.py')])
    options['py_modules'] = py_files

    if len(options['packages']) == 1:
        options['name'] = options['packages'][0]
    elif len(py_files) == 1:
        options['name'] = py_files[0]

    infer_from_vcs(options)

    return options


def derive_setup_options():
    options = infer_setup_options()
    options['install_requires'] = read_requirements_file('requirements.txt')
    cfg = SafeConfigParser()
    cfg.read('setup.cfg')
    if cfg.has_option('autopy', 'console_scripts'):
        console_scripts = cfg.get('autopy', 'console_scripts').strip().split()
        options['entry_points'] = {
            'console_scripts': console_scripts,
        }
    string_metadata = [
        'name',
        'version',
        'author',
        'author_email',
        'url',
        'description',
        'license',
    ]
    for key in string_metadata:
        if cfg.has_option('autopy', key):
            options[key] = cfg.get('autopy', 'key')
    return options


def main():
    setup(**derive_setup_options())

if __name__ == '__main__':
    main()
