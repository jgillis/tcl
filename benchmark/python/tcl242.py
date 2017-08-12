import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 16
c = 18
b = 16
m = 324
u = 20
v = 16
gflops = a*c*b*m*u*v*2/1e9
A = np.empty((a,u,b,c,v), order='f', dtype=np.float32)
B = np.empty((v,u,m), order='f', dtype=np.float32)
C = np.empty((b,a,m,c), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,u,b,c,v", B, "v,u,m", beta, C, "b,a,m,c" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("aubcv,vum->bamc", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC