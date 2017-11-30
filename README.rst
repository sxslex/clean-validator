======
clean-validator
======


.. image:: https://img.shields.io/badge/pypi-v0.0.2-orange.svg
    :target: https://pypi.python.org/pypi/clean-validator

.. image:: https://img.shields.io/badge/python-2.6%2C%202.7%2C%203.3+-blue.svg
    :target: https://travis-ci.org/sxslex/clean-validator.svg?branch=master

.. image:: https://travis-ci.org/sxslex/clean-validator.svg?branch=master
    :target: https://travis-ci.org/sxslex/clean-validator

.. image:: https://img.shields.io/badge/license--blue.svg
    :target: https://github.com/sxslex/capitalize-name/blob/master/LICENSE


Used to validate objects cleanly and simply.

Very good for testing implementation. ;)


Usage in python
=====

.. code-block:: pycon

    >>> import clean_validator
    >>> 
    >>> if clean_validator.assert_valid_object({"name": "SleX"}, {"name": str}):
    >>>     print('OK')
    >>> 
    >>> if clean_validator.assert_valid_object(
    >>>     [
    >>>         {"email": "sx.slex@gmail.com", "name": "SleX", "idade": 37},
    >>>         {"email": "slex@slex.com.br", "name": "Alexandre"},
    >>>     ],
    >>>     [{
    >>>         "email": lambda e: '@' in e and '.' in e,
    >>>         "name": str,
    >>>         "idade": (int, clean_validator.TypeNone,),
    >>>     }]
    >>> ):
    >>>     print('OK')
    >>> 

Installation
============

Use ``pip`` or ``easy_install``:

.. code::

    $ pip install clean-validator


Development
===========

Use py.test

.. code::
    $ py.test --cov=clean_validator tests/ -v

Use pep8

.. code::
    $ pycodestyle clean_validator
