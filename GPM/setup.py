# -*- coding: utf-8 -*-

#   Proyecto GPM: Generic Project Manager
#   Revisado el 6 Abril de 2013, por Francisco Quiñonez (franqur17@gmail.com)
#   Controlado:
#      - Adolfo Salas
#      - Pablo Sanchez
r"""
Clase setup

Configuración básica del sistema y requisitos para utilizarla.
"""


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
