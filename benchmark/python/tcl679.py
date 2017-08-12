import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 24
c = 24
b = 25
m = 600
u = 24
v = 25
gflops = a*c*b*m*u*v*2/1e9
A = np.empty((c,a,b,u,v), order='f', dtype=np.float32)
B = np.empty((u,m,v), order='f', dtype=np.float32)
C = np.empty((a,m,c,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "c,a,b,u,v", B, "u,m,v", beta, C, "a,m,c,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("cabuv,umv->amcb", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
