from setuptools import setup, find_packages
from os import path

readme_path = path.join(path.abspath(path.dirname(__file__)), 'README.md')
with open(readme_path) as readme:
    long_description = readme.read()

setup(name='lkh',
    description='Super simple Python wrapper for LKH-3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ben Hudson',
    author_email='benhudson@fastmail.com',
    version='1.0.3',
    license='DBAD',
    packages=find_packages(),
    url='https://github.com/ben-hudson/pylkh',
    download_url='https://github.com/ben-hudson/pylkh',
    keywords=['TSP', 'CVRP', 'VRP', 'LKH', 'LKH-3'],
    python_requires='>=3.3',
    install_requires=[
        'tsplib95'
    ],
)
