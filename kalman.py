#! /usr/bin/env python2
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <mayeu.tik@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Matthieu Maury
# ----------------------------------------------------------------------------

# Kalman filter implementation
# Equations are taken from the following article :
# Rao, R. P. (1999). An optimal estimation approach to visual perception
# and learning. Vision research, 39(11), 1963-89. Retrieved from
# http://www.ncbi.nlm.nih.gov/pubmed/10343783.

import numpy as np
import sys
from optparse import OptionParser
from multiprocessing import Pool

# Extract vector from file
# one vector per line
def extract_data(line):
    #print 'In extract data'
    #print line
    el = line.rstrip('\n').split(' ')
   # print el
    #print el
    data = np.array([[]])
    #print data
    counter = 0
    for e in el:
        #print e
        if counter == 0:
            data = [[float(e)]]
        #print e
        #print np.array(float(e),ndmin=2)
        else:
            data = np.concatenate((data, np.array(float(e),ndmin=2)))
        counter += 1

    return data

# Export graph to file, heatmap or dot
def export_graph(heat, ct, data, f):
    if heat:
        i = 0
        for el in data:
            for e in el:
                f.write(str(ct) + ' ' + str(i) + ' ' + str(e) + "\n")
            i += 1
        f.write("\n")

    else:
        f.write(str(ct))
        for el in data:
            for e in el:
                f.write(' ' + str(e))
        f.write("\n")

def learning(n,k):
    # generate U and V orthonormal
    if n > k:
        a = np.random.random_sample((n,k))
    else:
        a = np.random.random_sample((k,n))

    (U_barre_t,r) = np.linalg.qr(a)
    if n > k :
        U_barre_t = U_barre_t.T

    (V_barre_t_1,r) = np.linalg.qr(np.random.random_sample((n,n)))

    #U_barre_t = np.random.random_sample((k,n)) #* 0.001
    print 'U_barre_t size:' + str(k) + 'x' + str(n)
    #V_barre_t_1 = np.random.random_integers(0, 1, (n,n)) #* 0.001
    print 'V_barre_t_1 size:' + str(n) + 'x' + str(n)

    # Initialize r to 0
    r_opt_t_1 = np.zeros((n,1))

    alpha = 0.8
    beta = 0.8

    # Number of training loop
    t = o.training_loop

    # Openning file for graphing error
    if o.graph_learning_error:
        # File for graphing error of U
        geu = open('graph_error_U_'+str(n)+'.dat', 'a')
        geu.write("\n# Dataset\n");
        # File for graphing error of V
        gev = open('graph_error_V_'+str(n)+'.dat', 'a')
        gev.write("\n# Dataset\n")

    c = 0

    print "==> Start learning phase: dim(r)="+str(r_opt_t_1.shape)+", dim(U)="+str(U_barre_t.shape)+", dim(V)="+str(V_barre_t_1.shape)

    for i in range(t):
        #if (i%10):
        #sys.stdout.write("Step " + str(i) + " on " + str(t) +"\r")
        f = open(training_file,'r')
        fc = 0
        #if i != 0:
        #    alpha = alpha / 1.0025
        #    beta = beta / 1.0025

        # Initial value of the error
        if o.graph_learning_error:
            print_error_U = 0
            print_error_V = 0

        for line in f:
            #print 'out of extract data'
            #print line
            I_t = extract_data(line)

            #print 'Loop ' + str((i+1) * (fc+1))

            # Update U, V and r
            if i != 0 or fc != 0 :
                U_barre_t = U_opt_t
                r_opt_t_1 = r_opt_t
                V_barre_t_1 = V_opt_t_1
                #alpha = alpha / 1.0025
                #beta = beta / 1.0025

            # If we go to NaN or Inf, reset everything, really
            # not ideal, but it will do it for now
            if np.isinf(U_barre_t).all() or np.isnan(U_barre_t).all() or np.isinf(V_barre_t_1).all() or np.isnan(V_barre_t_1).all():
                print "Step " + str(i) + " on " + str(t)
                return ([],[], True)

            # Filter equation for learning
            r_prime_t = np.dot(V_barre_t_1, r_opt_t_1) # eq 21

            r_opt_t = r_prime_t + K * np.dot(U_barre_t.T, ( I_t - np.dot(U_barre_t, r_prime_t))) # eq 20 

            # Learning equation (5.3)
            # U_opt -> Û
            # U_barre -> Ū
            error_U = alpha * np.dot((I_t - np.dot(U_barre_t , r_opt_t)), (r_opt_t.T)) 
            U_opt_t = U_barre_t + error_U # eq 18

            error_V = beta * np.dot((r_opt_t - r_prime_t), r_opt_t_1.T)
            V_opt_t_1 = V_barre_t_1 + error_V # eq 19

            # Colecting learning error
            if o.graph_learning_error:
                print_error_U += error_U
                print_error_V += error_V

            # Update counter
            fc += 1 
            c += 1

        f.close()

        # Writing learning error to a file
        if o.graph_learning_error:
            geu.write(str(i) + ' ' + str(print_error_U.mean()/k) + '\n')
            gev.write(str(i) + ' ' + str(print_error_V.mean()/k) + '\n')


    # Closing learning error file
    if o.graph_learning_error:
        geu.write("\n")
        geu.close()
        gev.write("\n")
        gev.close()

    print "==> Learning Done"

    return (U_opt_t, V_opt_t_1, False)

def predict(U,V):

    # Initial value of r_opt_t_1
    r_opt_t_1 = np.zeros((n,1))

    f = open(o.input_file,'r')
    fpg = open('predicting_graph_'+o.input_file.rstrip('.dat')+'_'+str(n)+'.dat','a')
    fpg.write('\n# Dataset')
    fig = open('input_graph_'+o.input_file.rstrip('.dat')+'_'+str(n)+'.dat','a')
    fig.write('\n# Dataset')
    fdg = open('error_graph_'+o.input_file.rstrip('.dat')+'_'+str(n)+'.dat','a')
    fdg.write('\n# Dataset')

    ct = 0

    print "==> Start predicting phase"

    for line in f:
        # Filter equation
        r_barre_t = np.dot(V, r_opt_t_1) # eq 15
        pred = np.dot(U, r_barre_t) # eq 1
        export_graph(o.heatmap, ct, pred, fpg)
        
        I_t = extract_data(line)
        export_graph(o.heatmap, ct, I_t, fig)

        # Update the internal state with the entry
        r_opt_t = r_barre_t + K * np.dot(U.T, (I_t - np.dot(U, r_barre_t))) # eq 14
        r_opt_t_1 = r_opt_t

        # Print error map
        error = np.absolute((pred - I_t)/I_t)
        export_graph(o.heatmap,ct,error,fdg)
        #export_graph(o.heatmap, ct, I_t - pred, fdg)

        ct += 1

    print "==> Predicting Done"

    f.close()
    fpg.close()
    fig.close()
    fdg.close()

def kalman(x):
    # Settings the matrix size
    f = open(training_file,'r')
    line = f.readline()
    f.close()
    k = len(line.strip("\n").split(' '))
    #n = o.n # get n from the given args
    n = x

    # Learning
    restart = True
    while restart: # This while is here to start over in case of NaN of Inf matrix
        (U,V,restart) = learning(n,k)

    # Saving U and V
    f = open('U_'+str(n)+'.dat','a')
    f.write("\n# Dataset\n")
    np.savetxt(f,U)
    f.close()
    f = open('V_'+str(n)+'.dat','a')
    f.write("\n# Dataset\n")
    np.savetxt(f,V)
    f.close()

    predict(U, V)

if __name__ == "__main__":
    # Option parser config
    p = OptionParser()
    p.add_option('-n', default=6, type=int, help='Set the dimension of r. shape(r) = n*1.')
    p.add_option('-t','--training-file', default='training.dat', help='Set the training file.')
    p.add_option('-i','--input-file', default='input.dat', help='Set the input file to filter.')
    p.add_option('-m','--heatmap', action='store_true', default=False, help='Graphical data of input and predicted sequence will be formated as heatmap.')
    p.add_option('-l','--training-loop', default=30, type=int, help='Number of loop of training.')
    p.add_option('-g','--graph-learning-error', default=False, action='store_true', help='Print in file the learning error.')
    #p.add_option('-p','--pool', default=2, type=int, help='Number of parallel thread to launch.')

    # Kalman Gain
    K = 0.2

    # Parse the args
    (o, args) = p.parse_args()

    training_file = o.training_file # get the training file from the given args
    
    # Parallel launch with different n value
    #pool = 5
    #p = Pool(pool)
    #p.map(kalman,[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])

    # Standart launch
    kalman(o.n)
