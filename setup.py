try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'project description',
    'author': 'Siena Aguayo',
    'url': 'URL',
    'author_email': 'siena.aguayo@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['skills'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config)