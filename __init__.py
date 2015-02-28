#!/usr/bin/env python

r'''
DocTest
=======

>>> p = lambda data, **kwargs : print(sep='\n', *do(data, **kwargs))
>>> one_dim_data = ['a','b','c','aaa','bbb','ccc']
>>> p(one_dim_data, cols=3)
a   b   c
aaa bbb ccc
>>> p(one_dim_data, width=8)
a   b
c   aaa
bbb ccc
>>> csv_data = ['a,b,c',',bbb,ccc']
>>> p(csv_data, delimiter=',')
a b   c
  bbb ccc
>>> two_dim_data = [
...     ['a', 'bb', 'ccc'],
...     ['aaaa', 'bbb', 'cc'],
...     ['aa', 'bbbbbb', 'cccc']
... ]
>>> p(two_dim_data)
a    bb     ccc
aaaa bbb    cc
aa   bbbbbb cccc
'''


import itertools
import builtins


def _to_2d (data, cols):
    ''' Change 1D list data into a 2D list according to cols '''
    return [ data[i:i+cols] for i in range(0, len(data), cols) ]


def _do_2d (data, border=' '):
    ''' Make 2D input data column-aligned '''
    widths = _colwidth_2d(data)
    return [ border.join( j[0].ljust(j[1]) for j in zip(i, widths) ).rstrip() for i in data]


def _colwidth_2d (data):
    ''' Calculate the width of every column of a 2D list'''
    print(data)
    l = max( len(i) for i in data )
    z = list( itertools.zip_longest(*data, fillvalue='') )
    return [max(len(j) for j in z[i]) for i in range(l)]


def do (data, width=None, cols=None, delimiter=None, border=' '):
    ''' Make input data column-aligned '''

    if any(not isinstance(i, str) for i in data ):
        return _do_2d(data, border=border)

    if width is not None:
        return _do_2d( [i.split() for i in data], border=border )
    elif cols is not None:
        return _do_2d( _to_2d(data, cols), border=border )
    elif delimiter is not None:
        return _do_2d( [i.split(delimiter) for i in data], border=border )
    else:
        ...


def colwidth (data, width=None, cols=None, delimiter=None):
    ''' Calculate the with of every column of input data '''
    if width is not None:
        # data should be in [str, str, str] format
        ...

    if cols is not None:
        # data should be in [str, str, str] format
        return _colwidth_2d( _to_2d(data, cols) )

    if delimiter is not None:
        # data should be in [str, str, str] format
        return _colwidth_2d( [i.split(delimiter) for i in data] )

    else:
        return _colwidth_2d( [i.split() for i in data] )

    if all( isinstance(i, str) for i in data ):
        # data should be in [str, str, str] format
        return None

    return _colwidth_2d(data)


def run_command ():
    import argparse, sys

    parser = argparse.ArgumentParser(description='A tool that makes text column-aligned.')
    parser.add_argument('-b', '--border',   type=str, dest='border',    default=' ')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--columns',  type=int, dest='cols')
    group.add_argument('-w', '--width',    type=int, dest='width')
    group.add_argument('-d', '--delimiter',type=str, dest='delimiter')

    kwargs = vars(parser.parse_args())
    rows = do([line.rstrip() for line in sys.stdin], **kwargs)
    sys.stdout.write('\n'.join(rows)+'\n')


if __name__ == '__main__':
   run_command()

