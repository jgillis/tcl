import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 288
u = 300
m = 300
n = 288
gflops = a*u*m*n*2/1e9
A = np.empty((n,m,u), order='f', dtype=np.float32)
B = np.empty((a,u), order='f', dtype=np.float32)
C = np.empty((n,a,m), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "n,m,u", B, "a,u", beta, C, "n,a,m" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("nmu,au->nam", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
