from setuptools import setup

import os

# Put here required packages
packages = ['Django==1.6.3',
            'PIL==1.1.7',
            'Paste==1.7.5.1',
            'beautifulsoup4==4.3.2',
            'choice==0.1',
            'decorator==3.4.0',
            'djangosaml2==0.10.0',
            'httplib2==0.9',
            'pysaml2==0.4.3',
            'python-memcached==1.48',
            'repoze.who==1.0.18',
            'virtualenv==1.11.4',
            'wsgiref==0.1.2',
            'zope.interface==4.1.1',
            'pytz',
            'html5lib',
            'requests',
            'virtualenv',
]

if 'REDISCLOUD_URL' in os.environ and 'REDISCLOUD_PORT' in os.environ and 'REDISCLOUD_PASSWORD' in os.environ:
    packages.append('django-redis-cache')
    packages.append('hiredis')

setup(name='kalandar',
      version='1.0',
      description='Oregon State University Faculty Scheduling Tool',
      author='Austin Dubina',
      author_email='austin.dubina@gmail.com',
      url='https://pypi.python.org/pypi',
      install_requires=packages,
)

