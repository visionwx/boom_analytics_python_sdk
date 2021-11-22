#!/usr/bin/env python3

import os
from setuptools import setup

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'boom_analytics', '__version__.py')) as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=['boom_analytics'],
    include_package_data=True,
    python_requires=">=3.7.*",
    install_requires=['SensorsAnalyticsSDK', 'analytics-python'],
    zip_safe=False,
    keywords='boom analytics'
)