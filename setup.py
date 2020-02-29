'''
Created on 16/12/2015

@author: luisza
'''

from setuptools import setup, find_packages
import os

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
]

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Dynamically calculate the version based on django.VERSION.
version = __import__('async_notifications').get_version()

setup(
    author='Luis Zarate Montero',
    author_email='luis.zarate@solvosoft.com',
    name='async_notifications',
    version=version,
    description='Email async notifications with celery.',
    long_description=README,
    url='https://github.com/luisza/async_notifications',
    license='GNU General Public License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
	'celery>4.2',
	'django>2.0',
	'django-ajax-selects==1.9.1',
	'six',
	'django-classy-tags==0.8.0'
    ],
    packages=find_packages(exclude=["demo"]),
    include_package_data=True,
    zip_safe=False
)
