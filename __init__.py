#!/usr/bin/env python

r'''
DocTest
=======

>>> p = lambda data, **kwargs : print(sep='\n', *do(data, **kwargs))

.. >>> one_dim_data = ['a','b','c','aaa','bbb','ccc']
.. >>> p(one_dim_data, cols=3)
.. a   b   c
.. aaa bbb ccc
.. >>> p(one_dim_data, width=8)
.. a   b
.. c   aaa
.. bbb ccc
.. >>> csv_data = ['a,b,c',',bbb,ccc']
.. >>> p(csv_data, delimiter=',')
.. a b   c
..   bbb ccc

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


def _to_2d (data, cols):
    ''' Change 1D list data into a 2D list according to cols '''
    return [ data[i:i+cols] for i in range(0, len(data), cols) ]


def _do_2d (data, border=' '):
    ''' Make 2D input data column-aligned '''
    widths = _colwidth_2d(data)
    return [ border.join( j[0].ljust(j[1]) for j in zip(i, widths) ).rstrip() for i in data]


def _colwidth_2d (data):
    import itertools

    l = max( len(i) for i in data )
    z = list( itertools.zip_longest(*data, fillvalue='') )
    L = [max(len(j) for j in z[i]) for i in range(l)]
    return L


def get_colwidth(cols):
    return tuple(max(map(len, col)) for col in cols)


def trans_2dim_cols(rows):
    from itertools import zip_longest
    return tuple(zip_longest(fillvalue='', *rows))


def arrange_seq(seq, length):
    return tuple(seq[start::length] for start in range(length))


def clean(data, *, key=None, val=None):
    r'''
    return cleaned columns

    >>> clean([['a','b'],['c','d']])
    ((('a', 'c'), ('b', 'd')), (1, 1))
    >>> clean(['a,b', 'c,d'], key='delimiter', val=',')
    ((('a', 'c'), ('b', 'd')), (1, 1))
    >>> clean(['a', 'b', 'c', 'd'], key='cols', val=3)
    ((('a', 'd'), ('b', ''), ('c', '')), (1, 1, 1))
    >>> clean(['a', 'b', 'c', 'd'], key='width', val=4)
    (('a','c'), ('b','d'))
    '''
    if key is None:
        cols = trans_2dim_cols(data)
        return cols, get_colwidth(cols)
    elif key=='delimiter':
        cols = trans_2dim_cols(row.split(val) for row in data)
        return cols, get_colwidth(cols)
    elif key=='cols':
        offset = val - len(data) % 3
        cols = arrange_seq(seq=tuple(data)+('',)*offset, length=val)
        return cols, get_colwidth(cols)
    elif key=='width':
        ...



def gen_combined_rows(cols, colwidth, border):
    r'''
    given columns, generate combined rows

    >>> cols = [['a','aa'], ['b','bbbb'], ['c','ccc']]
    >>> colwidth = (2, 4, 3)
    >>> c_rows = gen_combined_rows(cols, colwidth, '|')
    >>> c_rows
    ['a |b   |c', 'aa|bbbb|ccc']
    >>> print(sep='\n', *c_rows)
    a |b   |c
    aa|bbbb|ccc
    '''
    form = border.join('{:%i}' % width for width in colwidth)
    combined_rows = [form.format(*row).rstrip() for row in zip(*cols)]
    return combined_rows


def do (data, width:int=None, cols:int=None, delimiter:str=None, border=' '):
    '''
    Make input data column-aligned
    ['a', 'b', 'c', 'd'] -> ['a b', 'c d']
    ['a,b', 'c,d']       -> ['a b', 'c d']
    [['a','b'],['c','d'] -> ['a b', 'c d']
    '''

    # check data type
    if all(isinstance(item, str) for item in data):
        is_2dim = False
    elif all(all(isinstance(item, str) for item in row) for row in data):
        is_2dim = True
    else:
        raise Exception

    # check parameters and generate process
    annotations = do.__annotations__
    if is_2dim:
        for k in annotations:
            if locals()[k] is not None:
                raise Exception
        cols, colwidth = clean(data)
    else:
        paras = None
        for k, t in annotations.items():
            val = locals()[k]
            if val is None:
                continue
            if not isinstance(val, t):
                raise Exception
            if paras is not None:
                raise Exception
            paras = {'key':k, 'val':val}
        cols, colwidth = clean(data, **paras)

    return gen_combined_rows(cols, colwidth=colwidth, border=border)

    '''
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
    '''


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

