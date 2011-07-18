#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Equations are taken from the following article :
# Rao, R. P. (1999). An optimal estimation approach to visual perception
# and learning. Vision research, 39(11), 1963-89. Retrieved from
# http://www.ncbi.nlm.nih.gov/pubmed/10343783.

import numpy as np

k = 3
#I_t = np.array([[[1],[1],[1],[1]],[[2],[2],[2],[2]],[[3],[3],[3],[3]],[[4],[4],[4],[4]],[[5],[5],[5],[5]]])
I_t = np.array([
    [[1],[0],[0]],
    [[0],[1],[0]],
    [[0],[0],[1]],
    [[0],[1],[0]],
    [[1],[0],[0]]
    ])
#print I_t
U_barre_t = np.random.random_sample((k,k))
print 'U_barre_t:'
print U_barre_t
V_barre_t_1 = np.random.random_sample((k,k))
print 'V_barre_t_1:'
print V_barre_t_1
r_opt_t_1 = np.zeros((k,1))

alpha = 1
beta = 1

t = 200

for i in range(t):
    if i != 0 :
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

    r_opt_t = r_prime_t + 0.2 * np.dot(U_barre_t.transpose(), ( I_t[i%5] - np.dot(U_barre_t, r_prime_t))) # eq 20 

    #print 'r_opt_t:'
    #print r_opt_t

# Learning equation (5.3)
# U_opt -> Û
# U_barre -> Ū
    #print 'U.r: '
    #print np.dot(U_barre_t, r_opt_t)
    U_opt_t = U_barre_t + alpha * np.dot((I_t[i%5] - np.dot(U_barre_t , r_opt_t)), (r_opt_t.transpose())) # eq 18
    V_opt_t_1 = np.dot(np.dot(V_barre_t_1 * beta, (r_opt_t - r_prime_t)), r_opt_t_1.transpose()) # eq 19

print 'U_opt_t: '
print U_opt_t
print 'V_opt_t_1: '
print V_opt_t_1
print 'r_opt_t: '
print r_opt_t

U = U_opt_t
V = V_opt_t_1
r_opt_t_1 = np.zeros((k,1))

t = 5

for i in range(t):

# Filter equation
    r_barre_t = np.dot(V, r_opt_t_1) # eq 14
    print 'I_t: '
    print I_t[i%5]
    r_opt_t = r_barre_t + np.dot(0.2 * U.transpose(), I_t[i%5] - np.dot(U, r_barre_t))

    print 'Prediction: '
    print np.dot(U, r_opt_t)
