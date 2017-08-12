import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 16
b = 16
m = 16
n = 15
u = 16
w = 16
v = 16
gflops = a*b*m*n*u*w*v*2/1e9
A = np.empty((v,n,w,u,m), order='f', dtype=np.float32)
B = np.empty((v,u,a,b,w), order='f', dtype=np.float32)
C = np.empty((m,a,n,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "v,n,w,u,m", B, "v,u,a,b,w", beta, C, "m,a,n,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("vnwum,vuabw->manb", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
