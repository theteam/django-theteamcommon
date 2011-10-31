from setuptools import setup, find_packages

setup(
    name = 'theteamcommon',
    version = '0.2',
    url = '',
    license = 'MIT',
    description = 'theTeam common libraries',
    author = 'theTeam',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)
