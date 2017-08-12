import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 12
c = 8
b = 12
e = 12
d = 12
m = 24
u = 12
gflops = a*c*b*e*d*m*u*2/1e9
A = np.empty((m,u), order='f', dtype=np.float32)
B = np.empty((c,b,d,u,e,a), order='f', dtype=np.float32)
C = np.empty((m,e,c,d,a,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "m,u", B, "c,b,d,u,e,a", beta, C, "m,e,c,d,a,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("mu,cbduea->mecdab", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
