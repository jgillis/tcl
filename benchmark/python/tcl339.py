import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 45
u = 45
c = 48
b = 45
m = 48
gflops = a*u*c*b*m*2/1e9
A = np.empty((m,u), order='f', dtype=np.float32)
B = np.empty((c,b,u,a), order='f', dtype=np.float32)
C = np.empty((m,b,a,c), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "m,u", B, "c,b,u,a", beta, C, "m,b,a,c" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("mu,cbua->mbac", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC