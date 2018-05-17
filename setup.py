#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import subprocess
import sys
from distutils.command.build import build
from shutil import rmtree, copy2

from setuptools import find_packages, setup, Command
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    bdist_wheel = None

# Package meta-data.
NAME = 'pyhtml2text'
DESCRIPTION = 'Python wrapper of the C++ Linux tool html2text'
URL = 'https://github.com/carsonip/pyhtml2text'
EMAIL = 'carsonip715@gmail.com'
AUTHOR = 'Carson Ip'
REQUIRES_PYTHON = '>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*'
VERSION = None

REQUIRED = [
    'cffi>=1.0.0, six',
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec (f.read(), about)
else:
    about['__version__'] = VERSION

cmdclass = {}


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


def build_dep():
    command = './configure && make'
    process = subprocess.Popen(command, shell=True, cwd=os.path.join(here, 'c', 'html2text'))
    process.wait()
    copy2(os.path.join(here, 'c', 'html2text', 'libhtml2text.so'), os.path.join(here, NAME))


class CustomInstall(install):
    def run(self):
        build_dep()
        install.run(self)


class CustomBuildExt(build_ext):
    def run(self):
        build_dep()
        build_ext.run(self)


class CustomBuild(build):
    def get_sub_commands(self):
        # Force "build_ext" invocation.
        commands = build.get_sub_commands(self)
        for c in commands:
            if c == 'build_ext':
                return commands
        return ['build_ext'] + commands


cmdclass.update({'build': CustomBuild,
                 'build_ext': CustomBuildExt,
                 'install': CustomInstall,
                 })

# https://github.com/numba/llvmlite/blob/master/setup.py
if bdist_wheel:
    class CustomBDistWheel(bdist_wheel):
        def run(self):
            build_dep()
            # Run wheel build command
            bdist_wheel.run(self)


    cmdclass.update({'bdist_wheel': CustomBDistWheel})

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    license='GPLv2',
    classifiers=[],
    package_data={NAME: ['libhtml2text.so']},
    cmdclass=cmdclass,
)
