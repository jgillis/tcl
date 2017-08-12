import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 108
m = 120
b = 108
u = 120
gflops = a*m*b*u*2/1e9
A = np.empty((u,m), order='f', dtype=np.float32)
B = np.empty((u,b,a), order='f', dtype=np.float32)
C = np.empty((m,a,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,m", B, "u,b,a", beta, C, "m,a,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("um,uba->mab", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
