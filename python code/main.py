#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 10:27:23 2019

@author: sebw
"""

import numpy as np
import matplotlib.pyplot as plt
import constant

def sim(action, x, x_dot, theta, theta_dot):
    theta_ddot = (constant.GRAVITY * np.sin(theta) + np.cos(theta) * (- action * constant.FORCE_MAG - constant.MASSPOLE * constant.LENGTH * theta_dot ** 2 * np.sin(theta) + constant.MU_C * np.sign(x_dot)) / constant.TOTAL_MASS - (constant.MU_P * theta_dot) / (constant.MASSPOLE * constant.LENGTH)) / (constant.LENGTH * (4/3 - (constant.MASSPOLE * (np.cos(theta)) ** 2) / constant.TOTAL_MASS))
    x_ddot = (action * constant.FORCE_MAG + constant.MASSPOLE * constant.LENGTH * (theta ** 2 * np.sin(theta) - theta_ddot * np.cos(theta)) - constant.MU_C * np.sign(x_dot)) / constant.TOTAL_MASS
    x += constant.TAU * x_dot
    x_dot += constant.TAU * x_ddot
    theta += constant.TAU * theta_dot
    theta_dot += constant.TAU * theta_ddot
    return x, x_dot, theta, theta_dot

def get_box(x,x_dot,theta,theta_dot):
    if x < -2.4 or x > 2.4  or theta < - 12/180 * np.pi or theta > 12/180 * np.pi:
        return(-1)

    if x < -0.8:
        box = 0
    elif x < 0.8:
        box = 1
    else:
        box = 2

    if x_dot < -0.5:
        pass
    elif x_dot < 0.5:
        box += 3
    else:
        box += 6

    if theta < - 6/180 * np.pi:
        pass
    elif theta < - 1/180 * np.pi:
        box += 9
    elif theta < 0:
        box += 18
    elif theta < 1/180 * np.pi:
        box += 27
    elif theta < 6/180 * np.pi:
        box += 36
    else:	    			       
        box += 45

    if theta_dot < - 50/180 * np.pi:
        pass
    elif theta_dot < 50/180 * np.pi:
        box += 54
    else:
        box += 108
    
    return box

fig1 = plt.figure(num = 1, figsize = (10, 7.5))
plt.ylim(0, constant.MAX_STEPS)
plt.xlim(0, constant.MAX_FAILURES)
plt.xlabel('TRIALS')
plt.ylabel('TIME STEPS UNTIL FAILURE')

list_of_list = []

for i in range(constant.RUNS):
    w = np.zeros(constant.N_BOXES) 
    v = np.zeros(constant.N_BOXES)
    xbar = np.zeros(constant.N_BOXES)
    e = np.zeros(constant.N_BOXES)
    
    x = 0.0
    x_dot = 0.0
    theta = 0.0
    theta_dot = 0.0
    
    box = get_box(x, x_dot, theta, theta_dot)
    
    list_steps = []

    steps = 0
    failures = 0
    while steps < constant.MAX_STEPS and failures < constant.MAX_FAILURES:
        steps += 1
    
        a = w[box] + np.random.normal(0.0, constant.SIGMA)
    #    print("a = {}".format(a))
        
        y = np.sign(a)
        if y == 0:
            y = 1
            
        e[box] += (1 - constant.DELTA) * y
        '''
        The C code effectively has a "* 0.5" at the end of the equation but this is not mentioned in the paper.
        '''
        xbar[box] += 1 - constant.LAMBDA
    
        
        oldp = v[box]
            
        x, x_dot, theta, theta_dot = sim(y, x, x_dot, theta, theta_dot)
    #    print(x)
    #    print(x_dot)
    #    print(theta)
    #    print(theta_dot)
        
        box = get_box(x, x_dot, theta, theta_dot)
    #    print(box)
        
        if box < 0:
            failed = 1
            failures += 1
            print("Trial {} was {} steps.".format(failures, steps))
            list_steps.append(steps)
            steps = 0
            
            x = x_dot = theta = theta_dot = 0.0
            box = get_box(x, x_dot, theta, theta_dot)
            
            r = -1
            p = 0
        else:
            failed = 0
            r = 0
            p = v[box]
        
        
        rhat = r + constant.GAMMA * p - oldp
        
        w += constant.ALPHA * rhat * e
        v += constant.BETA * rhat * xbar
        
        if failed:
            e = np.zeros(constant.N_BOXES)
            xbar = np.zeros(constant.N_BOXES)
        else:
            e *= constant.DELTA
            xbar *= constant.LAMBDA
    
    print("Run {}:".format(i + 1))       
    if failures == constant.MAX_FAILURES:
        print("Pole not balanced. Stopping after {} failures.".format(failures))
    else:
        print("Pole balanced successfully for at least {} steps.".format(steps))
        for j in range(constant.MAX_FAILURES - failures):
            list_steps.append(constant.MAX_STEPS)
    list_of_list.append(list_steps)
    plt.plot(list_steps)



avg = np.mean(list_of_list, axis = 0)

fig2 = plt.figure(num = 2, figsize = (10, 7.5))
plt.ylim(0, constant.MAX_STEPS)
plt.xlim(0, constant.MAX_FAILURES)
plt.xlabel('TRIALS')
plt.ylabel('TIME STEPS UNTIL FAILURE')
plt.plot(avg)

# plt.show()
fig1.savefig("individual.pdf")
fig2.savefig("average.pdf")







