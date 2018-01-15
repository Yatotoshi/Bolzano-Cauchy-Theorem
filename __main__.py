#!/usr/bin/env python3.6
from math import *
from decimal import *
import sys
import argparse

ex = 5
eps = round(pow(1/10, ex), ex)
partsize = 2


def main():
    stat = "sin(x)"

    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description='Proof of Bolzano-Cauchy Theorem calculator',
                                         usage="__main__.py STATEMENT [-h] [-a EX] [-p PARTSIZE]"
                                               "[-r SEG [SEG ...]] [-s STAT]")
        parser.add_argument('-a', action='store', default=3, type=int, dest='ex',
                            help='Accuracy of numbers (<= 4).')
        parser.add_argument('-p', action='store', default=2, type=float, dest='partsize',
                            help='Size of parts segment to be divided.')
        parser.add_argument('-r', action='store', default=(-32, 32), nargs='+', type=float, dest='seg',
                            help='Segment to be considered.')
        parser.add_argument('-s', action='store', default="sin(x)", type=str, dest='stat',
                            help='The statement.')

        args = parser.parse_args()
        global ex
        ex = args.ex
        if ex > 4:
            print("\033[91mUsing accuracy > 4 is highly not recommended!\033[0m")
        global partsize
        partsize = args.partsize

        seg = args.seg
        stat = args.stat

    global parts
    parts = round((seg[1] - seg[0]) / partsize)

    print("\033[92mLooking for roots f(x) = " + stat)
    print("on [" + str(seg[0]) + "; " + str(seg[1]) + "] segment" + "\033[0m")

    roots = find_roots(stat, seg)
    print("\t" + str(len(roots)) + " roots found.")

    i = 0
    for i in range(0, len(roots)):
        if roots[i] == 0:
            print(str(i + 1) + ". " + str(0))
        else:
            print(str(i + 1) + ". " + str(roots[i]))


def find_roots(stat, intseg, roots=[]):
    isfound = False
    segs = divide(intseg, parts)
    for seg in segs:
        left = calculate(stat, seg[0])
        right = calculate(stat, seg[1])
        if (left * right) <= 0:
            if calculate(stat, seg[1]) == 0:
                root = seg[1]
                isfound = True
            else:
                if seg[1] - seg[0] >= eps:
                    root = find_roots(stat, seg, roots)
                    isfound = True
                else:
                    return round((seg[0] + seg[1]) / 2, ex)
        if isfound:
            if type(root) is not list and not find(roots, root):
                roots.append(root)
            isfound = False
    return roots


def find(list, obj):
    for el in list:
        if el == obj:
            return True
    return False


def calculate(stat, arg):
    stat = stat.replace('x', '(' + str(arg) + ')')
    try:
        ans = eval(stat)
        return ans
    except Exception as msg:
        print("\033[91mCan't calculate \"f(x) = " + stat + "\"\033[0m")
        sys.exit()


def divide(seg, times):
    segs = []
    i = 0
    diff = seg[1] - seg[0]
    for i in range(0, times):
        if i == 0:
            left = seg[0]
        else:
            left = right
        right = diff * (i + 1) / times + seg[0]
        segs.append([left, right])
    return segs


if __name__ == "__main__":
    main()