from setuptools import setup, find_packages

setup(
    name='NoseGrowl',
    version='0.4',
    author='Victor Ng',
    author_email = 'crankycoder@gmail.com',
    description = 'nose plugin for Growl notifications',
    install_requires=['nose>=0.10', 'py-growl'],
    url = "http://bitbucket.org/crankycoder/nosegrowl",
    license = 'GNU LGPL',
    packages = find_packages(exclude=['tests']),
    zip_safe = False,
    include_package_data = True,
    package_data = { 
        '': ['*.png'], 
    },
    entry_points = {
        'nose.plugins': [
            'growl = nosegrowl.growler:NoseGrowl'
            ]
        }
    )

