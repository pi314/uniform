=======
Uniform
=======

A data column-aligned tool
~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: π
:Copyright: WTFPL


Command line tool
=================

* :code:`uniform` will automatically detect screen`s width

  .. code:: sh

    $ uniform < data

* Set column numbers

  .. code:: sh

    $ uniform -c 5 < data
    $ uniform --columns 5 < data

* Set display width

  .. code:: sh

    $ uniform -w 80 < data
    $ uniform --width 80 < data

* Set delimiter 

  .. code:: sh

    $ uniform -d ',' < data.csv
    $ uniform --delimiter ',' < data.csv

* Set border 

  .. code:: sh

    $ uniform -b '|' < data
    $ uniform --border '|' < data


Python Module
=============

:code:`uniform` module provides several functions

* :code:`do()`, returns a :code:`list` of :code:`str` for programmers to use
* :code:`colwidth()`, returns a :code:`list` of :code:`int`, contains the width of every column
* :code:`print()`, output the result to the file desciptor given by programmer

These functions takes several arguments

* :code:`data`

  - 1- or 2-dimensional :code:`list` of :code:`str`

* :code:`cols=None`, indicates the number of columns you want

  - Note that if :code:`data` is already 2-dimensional, this argument shall not be passed in

* :code:`width=None`, limits the length of output string

  - Note that if :code:`data` is already 2-dimensional, this argument shall not be passed in

* :code:`delimiter=' '`

  - Used to seperate input data
  - Cannot be used for 2-dimensional :code:`data`

* :code:`border=' '` (:code:`print()` and :code:`do()` only)

  - Used to seperate columns in output

* :code:`file=sys.stdout` (:code:`print()` only)

  - Where to print the output

* :code:`Flush=False` (:code:`print()` only)

  - Whether to forcibly flush the stream

:code:`cols`, :code:`width`, and :code:`delimiter` are mutually exclusive

Examples
--------

* :code:`do()`

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

* :code:`colwidth()`

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

