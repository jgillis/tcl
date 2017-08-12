import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 12
c = 12
b = 8
m = 12
o = 12
n = 8
u = 12
w = 12
v = 8
gflops = a*c*b*m*o*n*u*w*v*2/1e9
A = np.empty((v,u,n,w,o,m), order='f', dtype=np.float32)
B = np.empty((b,v,c,w,a,u), order='f', dtype=np.float32)
C = np.empty((n,o,b,a,c,m), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "v,u,n,w,o,m", B, "b,v,c,w,a,u", beta, C, "n,o,b,a,c,m" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("vunwom,bvcwau->nobacm", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC