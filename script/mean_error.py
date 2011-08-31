#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <mayeu.tik@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Matthieu Maury
# ----------------------------------------------------------------------------

import sys
import fileinput
import re

# Calculation of the mean of error matrix file. Kind of quick and dirty version...

f = open('mean_error.dat','w')
r = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,4,5,6,7,8,9] # idealy this value should be extracted from the filename
c = -1
cf = 0
 
args = sys.argv
args.pop(0)
args.sort()
print args

mean = 0
for line in fileinput.input(args):
    if fileinput.isfirstline():
        c += 1
        cf = 0
        if c > 0:
            f.write(str(r[c-1]) + ' ' + str(mean/(990*98)) + '\n')
            mean = 0
    if re.match('# Dataset',line):
        if cf != 0:
            f.write(str(r[c]) + ' ' + str(mean/(990*98)) + '\n')
            mean = 0
        continue
    if line == '\n':
        continue

    line = line.split(' ')
    #print line
    mean += float(line.pop())
    cf += 1

f.write(str(r[c]) + ' ' + str(mean/(990*98)) + '\n')
f.close()
