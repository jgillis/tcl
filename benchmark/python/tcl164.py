import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 36
m = 40
b = 40
u = 1536
n = 40
gflops = a*m*b*u*n*2/1e9
A = np.empty((u,b,a), order='f', dtype=np.float32)
B = np.empty((m,n,u), order='f', dtype=np.float32)
C = np.empty((b,n,m,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,b,a", B, "m,n,u", beta, C, "b,n,m,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("uba,mnu->bnma", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC