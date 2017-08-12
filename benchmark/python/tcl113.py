import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 15
b = 16
m = 16
n = 16
u = 16
w = 16
v = 16
gflops = a*b*m*n*u*w*v*2/1e9
A = np.empty((v,u,a,b,w), order='f', dtype=np.float32)
B = np.empty((v,n,w,u,m), order='f', dtype=np.float32)
C = np.empty((b,a,n,m), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "v,u,a,b,w", B, "v,n,w,u,m", beta, C, "b,a,n,m" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("vuabw,vnwum->banm", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
