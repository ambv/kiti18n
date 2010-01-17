# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

setup (
    name = 'langacore.kit.i18n',
    version = '0.1.0',
    author = 'LangaCore, Łukasz Langa',
    author_email = 'support@langacore.org, lukasz@langa.pl',
    description = "Various common i18n-related routines.",
    long_description = '',
    keywords = '',
    platforms = ['any'],
    license = 'GPL v3',
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'':'src'},
    namespace_packages = ['langacore', 'langacore.kit'],
    zip_safe = True,
    install_requires = [
        'setuptools',
        'polib',
        'Sphinx',
        ],

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
