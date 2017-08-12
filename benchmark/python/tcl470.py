import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 16
b = 15
m = 15
o = 16
n = 15
p = 15
u = 160
gflops = a*b*m*o*n*p*u*2/1e9
A = np.empty((u,n,m,o,p), order='f', dtype=np.float32)
B = np.empty((a,b,u), order='f', dtype=np.float32)
C = np.empty((o,b,m,n,a,p), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,n,m,o,p", B, "a,b,u", beta, C, "o,b,m,n,a,p" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("unmop,abu->obmnap", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
