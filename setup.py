from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='gait-profile-score',
    author='Michael Jeffryes',
    author_email='mike.jeffryes@hotmail.com',
    url='',
    version='0.0.4',
    description='Calculates Gait Profile Score',
    #packages=['gpscalc'],
    py_modules=["gpscalculator",],
    package_dir={'':'gpscalc'},
    setup_requires=['wheel'],
    classifiers=[
        #"License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    #test_suite='tests'
    install_requires=requirements,
    long_description=open('README.md').read(),
)

# python setupy.py sdist bdist_wheel
# twine upload dist/* --skip-existing
