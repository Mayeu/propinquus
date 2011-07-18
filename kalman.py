#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Equations are taken from the following article :
# Rao, R. P. (1999). An optimal estimation approach to visual perception
# and learning. Vision research, 39(11), 1963-89. Retrieved from
# http://www.ncbi.nlm.nih.gov/pubmed/10343783.

import numpy as np

def extract_data(line):
    el = line.rstrip('\n').split(' ')
    #print el
    data = np.array([[]])
    #print data
    counter = 0
    for e in el:
        if counter == 0:
            data = [[float(e)]]
        #print e
        #print np.array(float(e),ndmin=2)
        else:
            data = np.concatenate((data, np.array(float(e),ndmin=2)))
        counter += 1

    return data


f = open('training_sequence.dat','r')
line = f.readline()

k = len(line.strip("\n").split(' '))
n = k
#print 'k:'
#print k
f.close()
#I_t = np.array([[[1],[1],[1],[1]],[[2],[2],[2],[2]],[[3],[3],[3],[3]],[[4],[4],[4],[4]],[[5],[5],[5],[5]]])
#I_t = np.array([
#    [[1],[0],[0]],
#    [[0],[1],[0]],
#    [[0],[0],[1]],
#    [[0],[1],[0]],
#    [[1],[0],[0]]
#    ])
#print I_t
U_barre_t = np.random.random_sample((k,n))
#print 'U_barre_t:'
#print U_barre_t
V_barre_t_1 = np.random.random_sample((n,n))
#print 'V_barre_t_1:'
#print V_barre_t_1
r_opt_t_1 = np.zeros((n,1))

alpha = 1
beta = 1

t = 60

for i in range(t):
    f = open('training_sequence.dat','r')
    fc = 0
    for line in f:
        I_t = extract_data(line)
        #print 'I_t:'
        #print I_t
        if i != 0 or fc != 0 :
            U_barre_t = U_opt_t
            V_barre_t_1 = V_opt_t_1
            r_prime_t = r_opt_t

            alpha = alpha / 1.0025
            beta = beta / 1.0025

    # Filter equation for learning
        r_prime_t = np.dot(V_barre_t_1, r_opt_t_1) # eq 21
        #print 'r_prime_t: '
        #print r_prime_t
        #print 'U_barre_t.r_prime_t: '
        #print np.dot(U_barre_t, r_prime_t)
        #print 'I_t - U_barre_t.r_prime_t: '
        #print I_t[i%5] - np.dot(U_barre_t, r_prime_t)

        r_opt_t = r_prime_t + 0.2 * np.dot(U_barre_t.transpose(), ( I_t - np.dot(U_barre_t, r_prime_t))) # eq 20 

        #print 'r_opt_t:'
        #print r_opt_t

    # Learning equation (5.3)
    # U_opt -> Û
    # U_barre -> Ū
        #print 'U.r: '
        #print np.dot(U_barre_t, r_opt_t)
        U_opt_t = U_barre_t + alpha * np.dot((I_t - np.dot(U_barre_t , r_opt_t)), (r_opt_t.transpose())) # eq 18
        V_opt_t_1 = V_barre_t_1 + beta * np.dot((r_opt_t - r_prime_t), r_opt_t_1.transpose()) # eq 19
        
        fc += 1 
    f.close()

print 'U_opt_t: '
print U_opt_t
print 'V_opt_t_1: '
print V_opt_t_1

U = U_opt_t
V = V_opt_t_1
r_opt_t_1 = np.zeros((k,1))


f = open('predicting_sequence.dat','r')
fpg = open('predicting_graph.dat','w')
fig = open('input_graph.dat','w')
ct = 0
for line in f:
    I_t = extract_data(line)
# Filter equation
    r_barre_t = np.dot(V, r_opt_t_1) # eq 14
    #print 'r_barre_t:'
    #print r_barre_t

    #print 'I_t: '
    #print I_t
    i = 0
    for el in I_t:
        for e in el:
            fig.write(str(ct) + ' ' + str(k-i-1) + ' ' + str(e) + "\n")
        i += 1
    fig.write("\n")

    r_opt_t = r_barre_t + np.dot(0.2 * U.transpose(), I_t - np.dot(U, r_barre_t))
    pred = np.dot(U, r_opt_t) # eq 1

    r_opt_t_1 = r_opt_t

    #print 'Prediction: '
    #print np.dot(U, r_opt_t)
    i = 0
    for el in pred:
        for e in el:
            fpg.write(str(ct) + ' ' + str(k-i-1) + ' ' + str(e) + "\n")
        i += 1
    fpg.write("\n")

    ct += 1

f.close()
fpg.close()
fig.close()
