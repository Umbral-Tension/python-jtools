from setuptools import setup, find_packages

setup(
    name= 'jtools',
    description='Some personal programming tools',
    author='Jeremy',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'progress',
        'colorama',
    ],
)