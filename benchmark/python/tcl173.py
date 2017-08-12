import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 16
b = 18
m = 20
o = 20
n = 16
u = 324
gflops = a*b*m*o*n*u*2/1e9
A = np.empty((a,b,u), order='f', dtype=np.float32)
B = np.empty((n,o,u,m), order='f', dtype=np.float32)
C = np.empty((a,m,n,b,o), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,b,u", B, "n,o,u,m", beta, C, "a,m,n,b,o" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("abu,noum->amnbo", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
