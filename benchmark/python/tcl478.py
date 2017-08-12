import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 144
m = 16
o = 15
n = 15
p = 15
u = 15
v = 15
gflops = a*m*o*n*p*u*v*2/1e9
A = np.empty((a,u,v), order='f', dtype=np.float32)
B = np.empty((m,o,u,n,p,v), order='f', dtype=np.float32)
C = np.empty((a,n,o,m,p), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,u,v", B, "m,o,u,n,p,v", beta, C, "a,n,o,m,p" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("auv,mounpv->anomp", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC