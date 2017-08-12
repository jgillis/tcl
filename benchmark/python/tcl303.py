import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 8
m = 16
o = 12
n = 12
q = 12
p = 12
u = 16
gflops = a*m*o*n*q*p*u*2/1e9
A = np.empty((u,m,q,o,n,p), order='f', dtype=np.float32)
B = np.empty((a,u), order='f', dtype=np.float32)
C = np.empty((m,o,p,q,n,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,m,q,o,n,p", B, "a,u", beta, C, "m,o,p,q,n,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("umqonp,au->mopqna", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
