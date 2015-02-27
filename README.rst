=======
Uniform
=======

A data column-aligned tool
~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: π
:Copyright: WTFPL


Command Line Tool
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


Python Functions
================

:code:`uniform` module provides several functions.

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

