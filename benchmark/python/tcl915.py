import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 240
m = 18
o = 18
n = 18
p = 16
u = 18
v = 16
gflops = a*m*o*n*p*u*v*2/1e9
A = np.empty((v,a,u), order='f', dtype=np.float32)
B = np.empty((p,n,o,m,v,u), order='f', dtype=np.float32)
C = np.empty((a,n,m,o,p), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "v,a,u", B, "p,n,o,m,v,u", beta, C, "a,n,m,o,p" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("vau,pnomvu->anmop", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC