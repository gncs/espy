from distutils.util import convert_path
from typing import Dict

from setuptools import setup, find_packages


def readme() -> str:
    with open('README.md') as f:
        return f.read()


version_dict = {}  # type: Dict[str, str]
with open(convert_path('espy/version.py')) as file:
    exec(file.read(), version_dict)

setup(
    name='espy',
    version=version_dict['__version__'],
    description='Get Conjugation Tables of Spanish Verbs in Your Terminal',
    long_description=readme(),
    classifiers=['Programming Language :: Python :: 3.6'],
    author='Gregor Simm',
    author_email='',
    entry_points={
        'console_scripts': ['espy = espy.main:hook'],
    },
    python_requires='>=3.6',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'bs4',
    ],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
)
