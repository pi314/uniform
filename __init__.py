#!/usr/bin/env python
import itertools
import sys
import builtins
import argparse

def strlen (s):
    ''' Calculate the **visual** width of string s '''
    return len(s)

def _to_2d (data, cols):
    ''' Change 1D list data into a 2D list according to cols '''
    return [ data[i:i+cols] for i in range(0, len(data), cols) ]

def _do_2d (data, border=' '):
    ''' Make 2D input data column-aligned '''
    widths = _colwidth_2d(data)
    return [ border.join( j[0].ljust(j[1]) for j in zip(i, widths) ).rstrip() for i in data]

def do (data, width=None, cols=None, delimiter=' ', border=' '):
    ''' Make input data column-aligned '''
    if width != None:
        # data should be in [str, str, str] format
        ...

    if cols != None:
        # data should be in [str, str, str] format
        return _do_2d( _to_2d(data, cols), border=border )

    if delimiter != None:
        # data should be in [str, str, str] format
        return _do_2d( [i.split(delimiter) for i in data], border=border )

    if all( isinstance(i, str) for i in data ):
        # data should be in [str, str, str] format
        return None

    return _do_2d(data, border=border)

def _colwidth_2d (data):
    ''' Calculate the width of every column of a 2D list'''
    l = max( len(i) for i in data )
    z = list( itertools.zip_longest(*data, fillvalue='') )
    return [max(strlen(j) for j in z[i]) for i in range(l)]

def colwidth (data, width=None, cols=None, delimiter=' '):
    ''' Calculate the with of every column of input data '''
    if width != None:
        # data should be in [str, str, str] format
        ...

    if cols != None:
        # data should be in [str, str, str] format
        return _colwidth_2d( _to_2d(data, cols) )

    if delimiter != None:
        # data should be in [str, str, str] format
        return _colwidth_2d( [i.split(delimiter) for i in data] )

    if all( isinstance(i, str) for i in data ):
        # data should be in [str, str, str] format
        return None

    return _colwidth_2d(data)

def print (data, width=None, cols=None, delimiter=' ', border=' ', file=sys.stdout, flush=False):
    for i in do(data, width=width, cols=cols, delimiter=delimiter, border=border):
        builtins.print(i, file=file, flush=flush)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool that makes text column-aligned.')
    parser.add_argument('-c', '--columns',  type=int, dest='columns')
    parser.add_argument('-w', '--width',    type=int, dest='width')
    parser.add_argument('-d', '--delimiter',type=str, dest='delimiter', default=' ')
    parser.add_argument('-b', '--border',   type=str, dest='border',    default=' ')
    args = parser.parse_args()

    data = [i.rstrip() for i in sys.stdin.readlines()]

    builtins.print(args)
    print(data, width=args.width, cols=args.columns, delimiter=args.delimiter, border=args.border)

