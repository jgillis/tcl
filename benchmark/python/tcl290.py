import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 160
m = 162
u = 160
n = 160
gflops = a*m*u*n*2/1e9
A = np.empty((u,n,m), order='f', dtype=np.float32)
B = np.empty((u,a), order='f', dtype=np.float32)
C = np.empty((n,a,m), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,n,m", B, "u,a", beta, C, "n,a,m" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("unm,ua->nam", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
