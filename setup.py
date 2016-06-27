"""
Photo booth application for the Rapsberry Pi written in Python
"""
from setuptools import find_packages, setup

dependencies = [
        'click==6.6',
        'Pillow==3.2.0',
        'picamera==1.10',
        'RPi.GPIO==0.6.2'
    ]

setup(
    name='photoberry',
    version='0.1.0',
    url='https://github.com/briandilley/photoberry',
    license='BSD',
    author='Brian C. Dilley',
    author_email='briandilley@briandilley.com',
    description='Photo booth application for the Rapsberry Pi written in Python',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'photoberry = photoberry.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
