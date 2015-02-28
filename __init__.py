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


def gen_colwidth(data, *, key=None, val=None) -> [int]:
    '''
    generate width of columns from data
    '''
    from itertools import zip_longest

    if key is None:
        row_nums = max(map(len, data))
        cols = zip_longest(fillvalue='', *data)
    elif key=='delimiter':
        data = [row.split(val) for row in data]

def gen_rows(data, border):
    r'''
    >>> rows = gen_rows([['a','b','c'], ['aa','bbbb','ccc']], '|')
    >>> rows
    ['a |b   |c', 'aa|bbbb|ccc']
    >>> print(sep='\n', *rows)
    a |b   |c
    aa|bbbb|ccc
    '''
    from itertools import zip_longest

    cols = zip_longest(fillvalue='', *data)
    width_nums = (max(map(len, col)) for col in cols)
    form = border.join('{:%i}' % width for width in width_nums)
    rows = [form.format(*row).rstrip() for row in data]
    return rows


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

    '''
    # check parameters and generate process
    annotations = do.__annotations__
    if is_2dim:
        for k in annotations:
            if locals()[k] is not None:
                raise Exception
        cleaned_data = clean(data)
    else:
        paras = None
        for k, t in annotations.items():
            val = locals()[k]
            if val is None:
                continue
            if not isinstance(val, t):
                raise Exception
            if colwidth is not None:
                raise Exception
            paras = {'key':k, 'val':val}
        cleaned_data = clean(data, **paras)

    return gen_rows(cleaned_data, border=border)
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

