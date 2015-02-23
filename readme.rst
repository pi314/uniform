=======
Uniform
=======

A tool that makes text column-aligned.

Usage
-----

Command line tool
~~~~~~~~~~~~~~~~~

* Quick start ::

    $ uniform < data

  - ``uniform`` will automatically detect screen`s width

* Set column numbers ::

    $ uniform -c 5 < data
    $ uniform --columns 5 < data

* Set display width ::

    $ uniform -w 80 < data
    $ uniform --width 80 < data

* Set delimiter ::

    $ uniform -d ',' < data.csv
    $ uniform --delimiter ',' < data.csv

Python Module
~~~~~~~~~~~~~

``uniform`` module provides several functions

* ``do()``, returns a ``list`` of ``str`` for programmers to use
* ``colwidth()``, returns a ``list`` of ``int``, contains the width of every column
* ``print()``, output the result to the file desciptor given by programmer

These functions takes several arguments

* ``data``

  - 1- or 2-dimensional ``list`` of ``str``

* ``cols=None``, indicates the number of columns you want

  - Note that if ``data`` is already 2-dimensional, this argument shall not be passed in

* ``width=None``, limits the length of output string

  - Note that if ``data`` is already 2-dimensional, this argument shall not be passed in

* ``delimiter=None``

  - Used to seperate input data
  - Cannot be used for 2-dimensional ``data``

* ``border=' '`` (``print()`` and ``do()`` only)

  - Used to seperate columns

* ``file=sys.stdout`` (``print()`` only)

  - Where to print the output

* ``Flush=False`` (``print()`` only)

  - Whether to forcibly flush the stream

``cols``, ``width``, and ``delimiter`` are mutually exclusive

Examples

* ``do()``

..  code :: python

    >>> import uniform
    >>> data = ['a', 'bb', 'ccc', 'aaa2', 'bb2', 'c2']
    >>> result = uniform.do(data, cols=3)
    >>> print(result)
    ['a    bb  ccc', 'aaa2 bb2 c2']
    >>> for i in result: print(i)
    a    bb  ccc
    aaa2 bb2 c2
    >>> result = uniform.do(data, width=8)
    >>> print(result)
    ['a   bb', 'ccc aaa2', 'bb2 c2']
    >>> for i in result: print(i)
    a   bb
    ccc aaa2
    bb2 c2
    >>> data = ['a;bb;ccc', ';bb2;c2']
    >>> result = uniform.do(data, delimiter=';')
    >>> print(result)
    ['a bb  ccc', '  bb2 c2']
    >>> for i in result: print(i)
    a bb  ccc
      bb2 c2

* ``colwidth()``

..  code :: python

    >>> import uniform
    >>> data = ['a', 'bb', 'ccc', 'aaa2', 'bb2', 'c2']
    >>> result = uniform.colwidth(data, cols=3)
    >>> print(result)
    [4, 3, 3]
    >>> result = uniform.colwidth(data, width=8)
    >>> print(result)
    [3, 4]
    >>> data = ['a;bb;ccc', ';bb2;c2']
    >>> result = uniform.colwidth(data, delimiter=';')
    >>> print(result)
    [1, 3, 3]

* 2-dimensional Data

..  code :: python

    >>> import uniform
    >>> data = [
    ...   ['a', 'bb', 'ccc'],
    ...   ['aaa2', 'bb2', 'c2'],
    ...   ['a3', 'bbbbb3', 'ccc3']
    ... ]
    >>> result = uniform.do(data)
    >>> print(result)
    ['a    bb     ccc', 'aaa2 bb2    c2', 'a3   bbbbb3 ccc3']
    >>> for i in result: print(i)
    a    bb     ccc
    aaa2 bb2    c2
    a3   bbbbb3 ccc3

