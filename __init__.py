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

def typechecking(func):
    annotations = func.__annotations__
    assertion_form = "type of argument '{}' should be {}".format
    def func_(*args, **kwargs):
        for arg_name in annotations:
            if kwargs[arg_name] is None:
                continue
            assert isinstance(kwargs[arg_name], annotations[arg_name]) or \
                   assertion_form(arg_name, annotations[arg_name])
        return func(*args, **kwargs)
    return func_


def gen_columns_and_widths(rows):
    from itertools import zip_longest

    def transpose(rows):
        return tuple(zip_longest(fillvalue='', *rows))

    def compute_widths(columns):
        return tuple(max(map(len, col)) for col in columns)

    columns = transpose(rows)
    widths = compute_widths(columns)
    return columns, widths


def gen_columns_and_widths_with_delimiter(data, delimiter):
    rows = tuple(line.split(delimiter) for line in data)
    return gen_columns_and_widths(rows)


def gen_columns_and_widths_with_cols(data, cols):
    rows = tuple(data[i:i+cols] for i in range(0,len(data),cols))
    return gen_columns_and_widths(rows)


def gen_columns_and_widths_with_width(data, width, border):
    from itertools import count, takewhile

    def choose(cond, iterobj):
        obj = next(iterobj)
        for obj in takewhile(cond, iterobj):
            pass
        return obj

    def width_condition(obj):
        columns, widths = obj
        return sum(widths)+(len(widths)-1)*len(border) <= width

    candidates = (gen_columns_and_widths_with_cols(data, cols) for cols in count(1))
    return choose(width_condition, candidates)


@typechecking
def do (data, *, width:int=None, cols:int=None, delimiter:str=None, border=' '):
    '''
    Make input data column-aligned
    ['a', 'b', 'c', 'd'] -> ['a b', 'c d']
    ['a,b', 'c,d']       -> ['a b', 'c d']
    [['a','b'],['c','d'] -> ['a b', 'c d']
    '''
    discriminant = sum(para is None for para in (delimiter, cols, width))
    if all(isinstance(item, str) for item in data):
        assert discriminant==2
        if delimiter is not None:
            process_func = gen_columns_and_widths_with_delimiter
            args = (delimiter,)
        elif cols is not None:
            process_func = gen_columns_and_widths_with_cols
            args = (cols,)
        elif width is not None:
            process_func = gen_columns_and_widths_with_width
            args = (width, border)
    elif all(all(isinstance(item, str) for item in row) for row in data):
        assert discriminant==3
        process_func = gen_columns_and_widths
        args = ()
    else:
        raise AssertionError

    columns, widths = process_func(data, *args)
    form = border.join('{:%i}' % width for width in widths)
    lines = [form.format(*row).rstrip() for row in zip(*columns)]
    return lines


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

