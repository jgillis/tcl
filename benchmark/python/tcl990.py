import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 18
c = 18
b = 16
e = 18
d = 18
m = 16
u = 16
gflops = a*c*b*e*d*m*u*2/1e9
A = np.empty((u,c,d,b,e,a), order='f', dtype=np.float32)
B = np.empty((u,m), order='f', dtype=np.float32)
C = np.empty((b,c,a,m,e,d), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,c,d,b,e,a", B, "u,m", beta, C, "b,c,a,m,e,d" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("ucdbea,um->bcamed", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
