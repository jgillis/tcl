import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 16
b = 16
m = 15
o = 16
n = 16
p = 16
u = 200
gflops = a*b*m*o*n*p*u*2/1e9
A = np.empty((p,m,o,u,n), order='f', dtype=np.float32)
B = np.empty((b,u,a), order='f', dtype=np.float32)
C = np.empty((n,m,b,p,a,o), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "p,m,o,u,n", B, "b,u,a", beta, C, "n,m,b,p,a,o" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("pmoun,bua->nmbpao", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC