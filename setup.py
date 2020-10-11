from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='gpscalc-mjeffryes',
    author='Michael Jeffryes',
    author_email='mike.jeffryes@hotmail.com',
    url='',
    version='0.0.1',
    description='Calculates Gait Profile Score',
    #packages=['gpscalc'],
    py_modules=["calculator", 'calculations'],
    package_dir={'':'gpscalc'},
    setup_requires=['wheel'],
    classifiers=[
        "License :: ",
        "Programming Language :: Python :: 3",
    ],
    install_requires=requirements,
    long_description=open('README.md').read(),
)