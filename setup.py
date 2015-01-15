#!/usr/bin/env python
from setuptools import setup, Command
import subprocess


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call(['python -m py.test'])
        raise SystemExit(errno)

setup(
    name='HomicideReport',
    version='0.1',
    description='A publishing tool for Google spreadsheets',
    license='Apache',
    url='https://github.com/denverpost/homicide-report',
    author='Joe Murphy',
    author_email='joe.murphy@gmail.com',
    packages=['homicide-report'],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    )

