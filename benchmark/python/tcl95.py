import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 8
c = 8
b = 9
d = 10
m = 10
n = 10
u = 96
gflops = a*c*b*d*m*n*u*2/1e9
A = np.empty((a,b,u,d,c), order='f', dtype=np.float32)
B = np.empty((u,m,n), order='f', dtype=np.float32)
C = np.empty((c,d,n,m,b,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,b,u,d,c", B, "u,m,n", beta, C, "c,d,n,m,b,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("abudc,umn->cdnmba", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC