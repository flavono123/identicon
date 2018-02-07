from setuptools import setup, find_packages
from os.path import isfile

import Identicon

def read(*names):
    values = dict()
    extensions = ['.txt', '.rst']
    for name in names:
        value = ''
        for extension in extensions:
            filename = name + extension
            if isfile(filename):
                with open(filename) as f:
                     value = f.read()
                break
        values[name] = value
    return values

long_description = '''
%(README)s
===
%(CHANGES)s
''' % read('README', 'CHANGES')

setup(
    name='Identicon',
    version=Identicon.__version__,
    description='A Python library for generating Github-like identicons',
    long_description=long_description,
    keywords='identicon image profile render github',
    author='Hansuk Hong',
    author_email='flavono123@gmail.com',
    maintainer='Hansuk Hong',
    maintainer_email='flavono123@gmail.com',
    url='https://github.com/flavono123/identicon',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'pillow',  
    ],
)
