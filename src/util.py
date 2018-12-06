import numpy as np

def linear_forward(A, W, b):
    Z = np.dot(W, A) + b
    cache = (A, W, b)  
    return Z, cache

def linear_backward(dZ, cache):
    A_prev, W, b = cache
    dW = np.dot(dZ, cache[0].T)
    db = np.sum(dZ, axis=1, keepdims=True)
    dA_prev = np.dot(cache[1].T, dZ)
    return dA_prev, dW, db

def relu(Z):
    A = np.maximum(0,Z)    
    cache = Z 
    return A, cache

def relu_backward(dA, cache):
    Z = cache
    dZ = np.array(dA, copy=True)
    dZ[Z <= 0] = 0
    return dZ