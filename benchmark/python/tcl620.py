import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 600
m = 25
o = 24
n = 24
u = 24
v = 25
gflops = a*m*o*n*u*v*2/1e9
A = np.empty((o,m,u,n,v), order='f', dtype=np.float32)
B = np.empty((u,v,a), order='f', dtype=np.float32)
C = np.empty((n,o,a,m), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "o,m,u,n,v", B, "u,v,a", beta, C, "n,o,a,m" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("omunv,uva->noam", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
