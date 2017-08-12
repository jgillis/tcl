import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 1536
m = 8
o = 12
n = 12
u = 12
w = 12
v = 8
gflops = a*m*o*n*u*w*v*2/1e9
A = np.empty((v,n,w,o,m,u), order='f', dtype=np.float32)
B = np.empty((a,u,v,w), order='f', dtype=np.float32)
C = np.empty((m,a,n,o), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "v,n,w,o,m,u", B, "a,u,v,w", beta, C, "m,a,n,o" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("vnwomu,auvw->mano", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
