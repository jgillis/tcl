import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 15
b = 16
m = 15
o = 16
n = 15
p = 15
u = 200
gflops = a*b*m*o*n*p*u*2/1e9
A = np.empty((u,b,a), order='f', dtype=np.float32)
B = np.empty((o,m,n,p,u), order='f', dtype=np.float32)
C = np.empty((b,o,n,m,a,p), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,b,a", B, "o,m,n,p,u", beta, C, "b,o,n,m,a,p" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("uba,omnpu->bonmap", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
