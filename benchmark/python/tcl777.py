import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 27
c = 27
b = 24
m = 27
n = 24
u = 768
gflops = a*c*b*m*n*u*2/1e9
A = np.empty((n,u,m), order='f', dtype=np.float32)
B = np.empty((b,u,c,a), order='f', dtype=np.float32)
C = np.empty((n,m,c,b,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "n,u,m", B, "b,u,c,a", beta, C, "n,m,c,b,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("num,buca->nmcba", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC