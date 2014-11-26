#!/usr/bin/env python
"""
Trapeze App
-----------

Provides tools that automate processes in the Trapeze development workflow
via Django management commands. See README for more details.


Links
`````

* `readme (trunk) <https://office.trapeze.com/svnhtml/DjangoApps/trapeze/trunk/README>`_
* `releases <https://office.trapeze.com/svn/DjangoApps/trapeze/trunk/RELEASES>`_
* `svn repo <https://office.trapeze.com/svn/DjangoApps/trapeze/>`_


"""
from setuptools import setup

setup(
    name='trapeze',
    version='1.0.3STABLE',
    description='Trapeze Django Utility App',
    long_description=__doc__,
    packages=['trapeze', 'trapeze.management'],
    include_package_data=True,
    #install_requires=['django >= 1.3', ],
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)
