#!/usr/bin/env python
from os.path import join

from setuptools import setup, find_packages


MODULE_NAME = 'scrapedia'
REPO_NAME = 'scrapedia'


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(
    name=MODULE_NAME,
    description=('A scraper/crawler used for the extraction of brazilizan'
                 ' soccer historic data from the webpage futpedia.globo.com'),
    license=license,
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/LucasRGoes/{:s}'.format(REPO_NAME),
    author='Lucas Góes',
    author_email='lucas.rd.goes@gmail.com',
    packages=find_packages(exclude=('tests', 'docs')),
    version=open(join(MODULE_NAME, 'VERSION')).read().strip(),
    install_requires=['beautifulsoup4==4.7.1', 'cachetools==3.1.1',
                      'pandas==0.24.2', 'requests==2.22.0'],
    classifiers=['Programming Language :: Python :: 3.6']
)
