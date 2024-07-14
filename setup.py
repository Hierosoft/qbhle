# Based on https://packaging.python.org/en/latest/guides/single-sourcing-package-version/#single-sourcing-the-version

import os

# MODULE_DIR = os.path.realpath("qbhle")

# with open(os.path.join(MODULE_DIR, 'VERSION')) as version_file:
#     version = version_file.read().strip()

# version = {}
# with open("qbhle/version.py") as fp:
#     exec(fp.read(), version)
# later on we use: version['__version__']

import codecs
import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

#!/usr/bin/env python
import setuptools
import sys
import os

# versionedModule = {}
# versionedModule['urllib'] = 'urllib'
# if sys.version_info.major < 3:
#     versionedModule['urllib'] = 'urllib2'

install_requires = []

# if os.path.isfile("requirements.txt"):
#     with open("requirements.txt", "r") as ins:
#         for rawL in ins:
#             line = rawL.strip()
#             if len(line) < 1:
#                 continue
#             install_requires.append(line)
# ^ install_requires (pip install .) takes a different format for
#   git repos than requirements.txt (pip install -r requirements.txt)
#   (Hierosoft/hierosoft issue #9). So:
install_requires = [
  # https://github.com/dabeaz/sly.git
  'sly @ git+ssh://git@github.com/dabeaz/sly@master#egg=sly',
]
print("install_requires={}".format(install_requires), file=sys.stderr)
description = (
    "QB High Level Emulator."
)
long_description = description
if os.path.isfile("readme.md"):
    with open("readme.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
    name='qbhle',
    version=get_version("qbhle/__init__.py"),
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Programming Language :: Basic',
        'Programming Language :: YACC',
        ('License :: OSI Approved :: MIT License'),  # See also: license=
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows'
        'Operating System :: MacOS :: MacOS X'
        'Topic :: Software Development :: Interpreters',
    ],
    keywords=('QBASIC BASIC emulator interpreter compiler parser'),
    url="https://github.com/Poikilos/qbhle",
    author="Jake Gustafson",
    author_email='7557867+poikilos@users.noreply.github.com',
    license='MIT License',  # See also: license classifier above.
    # packages=setuptools.find_packages(),
    packages=['qbhle'],
    include_package_data=True,  # look for MANIFEST.in
    # scripts=['example'],
    # ^ Don't use scripts anymore (according to
    #   <https://packaging.python.org/en/latest/guides
    #   /distributing-packages-using-setuptools
    #   /?highlight=scripts#scripts>).
    # See <https://stackoverflow.com/questions/27784271/
    # how-can-i-use-setuptools-to-generate-a-console-scripts-entry-
    # point-which-calls>
    # entry_points={
    #     'console_scripts': [
    #         'qbhle-cli=qbhle:main_cli',
    #     ],
    # },
    install_requires=install_requires,
    #     versionedModule['urllib'],
    # ^ "ERROR: Could not find a version that satisfies the requirement
    #   urllib (from nopackage) (from versions: none)
    #   ERROR: No matching distribution found for urllib"
    test_suite='pytest',
    tests_require=['pytest', 'unittest'],
    zip_safe=False,  # It can't run zipped due to needing data files.
)
