import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-mediaman',
    version = '0.1',
    packages = ['mediaman'],
    include_package_data = True,
    license = 'BSD License',
    description = 'A simple Django app to help bulk uploading/managing images.',
    long_description = README,
    url = 'https://github.com/omad/django-mediaman/',
    author = 'Damien Ayers',
    author_email = 'd.ayers@uq.edu.au',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
