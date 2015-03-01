#!/usr/bin/env python

r'''
DocTest
=======

>>> p = lambda data, **kwargs : print(sep='\n', *do(data, **kwargs))
>>> one_dim_data = ['a','b','c','aaa','bbb','ccc']
>>> p(one_dim_data, cols=3)
a   b   c
aaa bbb ccc

.. >>> p(one_dim_data, width=8)
.. a   b
.. c   aaa
.. bbb ccc

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


def get_colwidth(cols):
    '''
    >>> cols = (('a', 'aa'), ('bbbb', 'b'))
    >>> get_colwidth(cols)
    (2, 4)
    '''
    return tuple(max(map(len, col)) for col in cols)


def trans_2dim_cols(rows):
    '''
    >>> rows = ((1, 2), (3,))
    >>> trans_2dim_cols(rows)
    ((1, 3), (2, ''))
    '''
    from itertools import zip_longest
    return tuple(zip_longest(fillvalue='', *rows))


def arrange_seq_cols(seq, length):
    '''
    >>> seq = (0,1,2,3,4,5)
    >>> arrange_seq_cols(seq, 3)
    ((0, 3), (1, 4), (2, 5))
    >>> arrange_seq_cols(seq, 2)
    ((0, 2, 4), (1, 3, 5))
    '''
    return tuple(seq[start::length] for start in range(length))


def find_colwidth(seq, offset, max_length):
    '''
    >>> find_colwidth((1,2,2,1,1), 1, 6)
    (2, 2)
    >>> find_colwidth((1,2,1,1,2), 1, 6)
    (1, 2, 1)
    '''
    # shorten test values
    num_cols = 1
    sorted_seq = sorted(seq, reverse=True)
    while 1:
        if sum(sorted_seq[:num_cols+1]) + offset*num_cols <= max_length:
            num_cols += 1
        else:
            break

    # try more columns



def clean(data, *, key=None, val=None, border=' '):
    r'''
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
        remainder = len(data) % 3
        offset = val - remainder if remainder else 0
        cols = arrange_seq_cols(seq=tuple(data)+('',)*offset, length=val)
        return cols, get_colwidth(cols)
    elif key=='width':
        widths = tuple(map(len, data))
        print('widths:', widths)
        colwidth = find_colwidth(widths, offset=len(border), max_length=val)
        print('colwidth', colwidth)



def gen_combined_rows(cols, colwidth, border):
    r'''
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
        raise AssertionError

    # check parameters and generate process
    vars_ = vars()
    annos = do.__annotations__
    ex_args = tuple((k,t,vars_[k]) for k,t in annos.items())
    if is_2dim:
        assert sum(v is None for k,t,v in ex_args)==3
        cols, colwidth = clean(data)
    else:
        assert sum(v is None for k,t,v in ex_args)==2
        key, type_, val = next(a for a in ex_args if a[2] is not None)
        assert isinstance(val, type_), (key, type_, val)
        cols, colwidth = clean(data, border=border, key=key, val=val)

    return gen_combined_rows(cols, colwidth=colwidth, border=border)


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

