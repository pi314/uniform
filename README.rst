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

:code:`uniform` module provide a function :code:`do`.
See the example below:

.. code:: python

   >>> from uniform import do
   >>> one_dim_data = ['a','b','c','aaa','bbb','ccc']
   >>> print( sep='\n', *do(one_dim_data, cols=3) )
   a   b   c
   aaa bbb ccc
   >>> print( sep='\n', *do(one_dim_data, width=8) )
   a   b
   c   aaa
   bbb ccc
   >>>
   >>> csv_data = ['a,b,c',',bbb,ccc']
   >>> print( sep='\n', *do(csv_data, delimiter=',') )
   a b   c
     bbb ccc
   >>> two_dim_data = [
   ...     ['a', 'bb', 'ccc'],
   ...     ['aaaa', 'bbb', 'cc'],
   ...     ['aa', 'bbbbbb', 'cccc']
   ... ]
   >>> print( sep='\n', *do(two_dim_data) )
   a    bb     ccc
   aaaa bbb    cc
   aa   bbbbbb cccc
