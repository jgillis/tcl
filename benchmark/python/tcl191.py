import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 120
m = 12
o = 12
n = 8
p = 12
u = 12
v = 12
gflops = a*m*o*n*p*u*v*2/1e9
A = np.empty((a,v,u), order='f', dtype=np.float32)
B = np.empty((n,m,u,v,p,o), order='f', dtype=np.float32)
C = np.empty((a,p,m,n,o), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,v,u", B, "n,m,u,v,p,o", beta, C, "a,p,m,n,o" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("avu,nmuvpo->apmno", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
