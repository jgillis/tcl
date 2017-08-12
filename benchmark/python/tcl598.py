import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 72
m = 54
b = 64
u = 3240
n = 64
gflops = a*m*b*u*n*2/1e9
A = np.empty((a,u,b), order='f', dtype=np.float32)
B = np.empty((n,u,m), order='f', dtype=np.float32)
C = np.empty((b,m,n,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,u,b", B, "n,u,m", beta, C, "b,m,n,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("aub,num->bmna", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC