# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 13:54:35 2024

@author: osman
"""

import numpy as np
import matplotlib.pyplot as plt

def correlated_normals(rho, size):
    """
    Generates two sets of correlated standard normal variables.
    rho: correlation coefficient
    size: tuple (steps, N) for the output matrix size
    """
    L = np.linalg.cholesky([[1, rho], [rho, 1]])
    normals = np.random.normal(size=(2, *size))
    return np.tensordot(L, normals, axes=([0],[0]))

def geo_paths(S1, S2, T, r1, r2, q1, q2, sigma1, sigma2, rho, steps, N):
    """
    Inputs:
    S1, S2 = Initial stock Prices for each GBM
    T = Time to maturity (1 year = 1, 1 month = 1/12)
    r1, r2 = risk-free interest rates for each GBM
    q1, q2 = dividend yields for each GBM
    sigma1, sigma2 = volatilities for each GBM
    rho = correlation coefficient between the two assets
    steps = number of time steps
    N = number of trials

    Output:
    Tuple of two [steps+1, N] matrices of asset paths
    """
    dt = T/steps
    # Simulate two sets of correlated Brownian motions
    dW = correlated_normals(rho, (steps, N)) * np.sqrt(dt)
    # Initialize paths
    paths1 = np.zeros((steps + 1, N))
    paths2 = np.zeros((steps + 1, N))
    paths1[0] = S1
    paths2[0] = S2
    
    for t in range(1, steps + 1):
        paths1[t] = paths1[t - 1] * np.exp((r1 - q1 - 0.5 * sigma1**2) * dt + sigma1 * dW[0, t-1])
        paths2[t] = paths2[t - 1] * np.exp((r2 - q2 - 0.5 * sigma2**2) * dt + sigma2 * dW[1, t-1])
    
    return paths1, paths2

# Set parameters for each GBM
S1, S2 = 100, 120
r1, r2 = 0.05, 0.06
q1, q2 = 0.02, 0.03
sigma1, sigma2 = 0.25, 0.20
rho = 0.9  # Correlation coefficient
T = 0.5  # Time to maturity
steps = 100  # Time steps
N = 1000  # Number of trials

paths1, paths2 = geo_paths(S1, S2, T, r1, r2, q1, q2, sigma1, sigma2, rho, steps, N)
product_paths = paths1 * paths2


K=S1*S2 #strike 



payoffs = np.maximum(product_paths[-1, :]-K, 0)

discount=r2


option_price = np.mean(payoffs)*np.exp(-discount*T) #discounting back to present value

