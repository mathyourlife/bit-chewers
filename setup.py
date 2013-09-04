
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os.path import abspath, dirname, join

path = abspath(dirname(__file__))

classifiers = (
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Unix',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: System :: Monitoring',
)

packages = [
    'BitChewers',
]

kw = {
    'name': 'BitChewers',
    'version': '0.0.1',
    'description': 'Analytics for your command line.  Filter/Map/Reduce from stdin.',
    'long_description': open(join(path, 'README.md')).read(),
    'author': 'Daniel Couture, Carlton Stedman',
    'license': 'MIT License',
    'classifiers': classifiers,
    'packages': packages,
    'package_data': {'BitChewers': ['*.md']},
}

setup(**kw)
