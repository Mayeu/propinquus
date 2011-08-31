#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <mayeu.tik@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Matthieu Maury
# ----------------------------------------------------------------------------

import math
import re
import numpy

# Extract muscles size from a SOFA dump file.
# The file is formated as :
# <step> <list of muscles size>
# <step> ...

name = 'data_worm.dat'
nout = 'tail_muscles_size_all.dat'

M = 48
P = 2*(M+1)

f = open(name, 'rb')
fout = open(nout, 'w')
for l in f:
    #if re.search('T=', l):
        #fout.write('## ' + l)
    if re.search('X=', l):
        worm = numpy.zeros((P,2))
        coordinate = l.strip(' \t\n\r').split(' ')
        coordinate.pop(0)
        i = 0
        flag = True
        pos = 0
        for c in coordinate:
            if i == 0:
                #print float(c)
            # x
                if flag == True:
                    worm[pos][0] = float(c)
                else:
                    worm[97-pos][0] = float(c)
            elif i == 1:
            # y
                if flag == True:
                    worm[pos][1] = float(c)
                else:
                    worm[97-pos][1] = float(c)

            elif i == 2:
            #don't care about z
                if flag == True:
                    flag = False
                else:
                    pos += 1
                    flag = True
            i = (i+1)%3
         # print in the file
        #for el in worm:
        #    for c in el:
        #        fout.write(str(c)+"\t")
        #    fout.write("\n")
        for i in range(P):
            fout.write(str(math.sqrt(
                math.pow((worm[(i+1)%P][0]-worm[(i)%P][0]),2) +
                math.pow((worm[(i+1)%P][1]-worm[(i)%P][1]),2))))
            if i != (P-1):
                fout.write(' ')
        fout.write('\n')
