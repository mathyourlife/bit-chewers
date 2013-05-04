
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os.path import abspath, dirname, join

path = abspath(dirname(__file__))

classifiers = (
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 3.3',
    'License :: OSI Approved :: MIT License',
)

packages = [
    'BitChewers',
    'BitChewers.JSON',
]

required = [
]

kw = {
    'name': 'BitChewers',
    'version': '0.0.1',
    'description': 'A Python lib to turn log lines to analytics',
    'long_description': open(join(path, 'README.md')).read(),
    'author': 'Daniel Couture, Carlton Stedman',
    'license': 'MIT License',
    'classifiers': classifiers,
    'packages': packages,
    'package_data': {'BitChewers': ['*.md']},
    'install_requires': required,
}

setup(**kw)
