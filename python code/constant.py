#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 10:25:14 2019

@author: sebw
"""

GRAVITY = 9.8
MASSCART = 1.0
MASSPOLE = 0.1
TOTAL_MASS = (MASSPOLE + MASSCART)
LENGTH = 0.5		  # actually half the pole's length
POLEMASS_LENGTH = (MASSPOLE * LENGTH)
FORCE_MAG = 10.0
TAU = 0.02		  # seconds between state updates
MU_C = 0.0005
MU_P = 0.000002

N_BOXES = 162
ALPHA = 1000
BETA = 0.5
GAMMA = 0.95
DELTA = 0.9
LAMBDA = 0.8
SIGMA = 0.01

MAX_FAILURES = 100
MAX_STEPS = 100000

RUNS = 10