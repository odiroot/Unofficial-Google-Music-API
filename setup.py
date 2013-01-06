# Copyright (c) 2012, Simon Weber
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the
#       names of the contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from distutils.core import setup
from setuptools import find_packages

setup(
    name='gmusicapi',
    version='2013.01.05',
    author='Simon Weber',
    author_email='simon@simonmweber.com',
    url='http://pypi.python.org/pypi/gmusicapi/',
    packages=find_packages(),
    scripts=[],
    license='COPYING',
    description='An unofficial api for Google Play Music.',
    long_description="""\
gmusicapi is an unofficial api for Google Play Music. Please see the `project page <https://github.com/simon-weber/Unofficial-Google-Music-API>`_ for details.

This api is not supported nor endorsed by Google, and could break at any time.
""",
    install_requires=[
        "validictory == 0.7.2",
        'decorator == 3.3.2',
        'mutagen == 1.20',
        'protobuf == 2.4.1',
        'chardet == 2.1.1',
        #for testing album art:
        #'hachoir-core == 1.3.3',
        #'hachoir-parser == 1.3.4',
        #'hachoir-metadata == 1.3.3',
    ],
    classifiers = [
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Software Development :: Libraries :: Python Modules"
        ],
    include_package_data=True,
    zip_safe=False,
)
