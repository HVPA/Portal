# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2011 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

root_dir = "/usr/share/"

data_files = {}


def add_data_file(prefix, path, files):
    for f in files:
        relative_path = os.path.join(path, f)
        if prefix:
            filepath = os.path.join(root_dir, prefix, relative_path)
        else:
            filepath = os.path.join(root_dir, relative_path)
        base = os.path.dirname(filepath)
        if os.path.isdir(relative_path):
            continue
        if not base in data_files:
            data_files[base] = []
        data_files[base].append(relative_path)

setup(
    name='HVPA Portal',
    version='0.3',
    license='Apache 2.0',
    description="The HVPA portal website to view genomic variant data.",
    #long_description=read('Readme.txt'),
    author='V3 Alliance',
    author_email='as@v3.org.au',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'local']),
    data_files=data_files.items(),
    install_requires=[''],
    zip_safe=False,
    classifiers=[
        'Development Status :: 0 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
