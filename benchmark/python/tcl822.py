import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 27
c = 24
b = 27
m = 768
u = 27
v = 27
gflops = a*c*b*m*u*v*2/1e9
A = np.empty((c,v,u,a,b), order='f', dtype=np.float32)
B = np.empty((m,u,v), order='f', dtype=np.float32)
C = np.empty((c,b,m,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "c,v,u,a,b", B, "m,u,v", beta, C, "c,b,m,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("cvuab,muv->cbma", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC