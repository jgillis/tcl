import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 1152
u = 32
n = 24
m = 32
v = 32
gflops = a*u*n*m*v*2/1e9
A = np.empty((m,u,v,n), order='f', dtype=np.float32)
B = np.empty((a,v,u), order='f', dtype=np.float32)
C = np.empty((n,a,m), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "m,u,v,n", B, "a,v,u", beta, C, "n,a,m" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("muvn,avu->nam", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
