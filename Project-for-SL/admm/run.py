import time
import numpy as np
import admm
import math
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from sklearn.datasets import load_boston

print "First, we show our ADMM algorithm is correct on a simple Boston data."
boston = load_boston()
mean = np.mean(boston.data,axis=0)
std = np.std(boston.data,axis=0)
X = (boston.data -mean)/std
Y = boston.target
lasso = admm.ADMM(X, Y)
result = lasso.solve()
np.set_printoptions(formatter={'float': '{: 0.6f}'.format})
print lasso.x
lasso = Lasso()
lasso.fit(X, Y)
print lasso.coef_

print "We simulate data as the approach in the paper."
N = 100
p = 5000
rho = 0.5
k = 0.5
Expect = np.zeros(p)
Sigma = np.ones((p, p)) * rho + np.identity(p) * (1-rho)
X = np.random.multivariate_normal(Expect, Sigma, N)
beta = [((-1)**j) * math.exp(-2.0*(j-1)/20.0) for j in range(1, 50+1)]
print "Ground truth beta is", beta[:50]
for j in range(50, p):
	beta.append(0)
Y = np.random.randn(N) * k + X.dot(beta)
np.savetxt("X.txt", X)
np.savetxt("beta.txt", beta)
np.savetxt("Y.txt", Y)

print "We compare the running time of our ADMM and lasso package in python sklearn."
start = time.time()
lasso = admm.ADMM(X, Y)
lasso.solve(lamba = 0.1)
end = time.time()
np.set_printoptions(formatter={'float': '{: 0.6f}'.format})
print "After", end - start, "s get ADMM result"
print "Number of non-zero coef:", np.sum(abs(lasso.x) > 1e-6)
print lasso.x[:10]

start = time.time()
lasso = Lasso(0.1)
lasso.fit(X, Y)
end = time.time()
print "After", end - start, 's get Lasso result'
print "Number of non-zero coef:", np.sum(lasso.coef_ != 0)
print lasso.coef_[:10]

lower = -15.0
upper = 1.0
num = 100
print "We apply our algorithm for {} lambda values from exp({}) to exp({}).".format(num, lower, upper)
lamba_set = []
admm_result = np.zeros((num, p))
start = time.time()
lasso = admm.ADMM(X, Y)
for t in range(num):
    k = math.exp(upper - (upper - lower)*t/num)
    print "The {}th lambda is {}.".format(t, k)
    lasso.solve(lamba = k)
    lamba_set.append(k)
    admm_result[t] = lasso.x
end = time.time()
print "After", end - start, "s get ADMM results"
np.savetxt('results.txt', admm_result)
