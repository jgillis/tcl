import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 32
m = 30
u = 32
o = 32
n = 32
gflops = a*m*u*o*n*2/1e9
A = np.empty((u,o,m,n), order='f', dtype=np.float32)
B = np.empty((a,u), order='f', dtype=np.float32)
C = np.empty((n,m,a,o), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,o,m,n", B, "a,u", beta, C, "n,m,a,o" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("uomn,au->nmao", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
