import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 3072
m = 15
o = 16
n = 15
u = 16
w = 15
v = 16
gflops = a*m*o*n*u*w*v*2/1e9
A = np.empty((v,o,n,m,w,u), order='f', dtype=np.float32)
B = np.empty((u,v,w,a), order='f', dtype=np.float32)
C = np.empty((o,a,m,n), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "v,o,n,m,w,u", B, "u,v,w,a", beta, C, "o,a,m,n" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("vonmwu,uvwa->oamn", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC