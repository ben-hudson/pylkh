from setuptools import setup

setup(name='lkh',
    description='Super simple Python wrapper for LKH-3',
    author='Ben Hudson',
    author_email='benhudson@fastmail.com',
    version='1.0',
    license='DBAD',
    py_modules=['lkh'],
    url='https://github.com/ben-hudson/pylkh',
    download_url='https://github.com/ben-hudson/pylkh',
    keywords=['TSP', 'CVRP', 'VRP', 'LKH', 'LKH-3'],
    python_requires='>=3.3',
    install_requires=[
    	'tsplib95'
    ],
)
