# -*- coding: utf-8 -*-

from setuptools import setup

project = "webapp"

setup(
    name=project,
    version='0.1',
    url='',
    description='',
    author='',
    author_email='',
    packages=["webapp"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'Flask-Script',
        'Flask-Babel',
        'Flask-Testing',
        'Flask-Mail',
        'Flask-Cache',
        'Flask-Login',
        'nose',
    ]
)
