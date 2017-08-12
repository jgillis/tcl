import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 24
b = 32
m = 10
o = 10
n = 10
u = 10
w = 8
v = 10
gflops = a*b*m*o*n*u*w*v*2/1e9
A = np.empty((a,u,v,w,b), order='f', dtype=np.float32)
B = np.empty((w,u,m,o,v,n), order='f', dtype=np.float32)
C = np.empty((b,o,a,n,m), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,u,v,w,b", B, "w,u,m,o,v,n", beta, C, "b,o,a,n,m" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("auvwb,wumovn->boanm", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
