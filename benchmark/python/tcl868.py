import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 15
c = 16
b = 16
m = 16
o = 16
n = 16
u = 16
w = 16
v = 16
gflops = a*c*b*m*o*n*u*w*v*2/1e9
A = np.empty((u,b,a,v,c,w), order='f', dtype=np.float32)
B = np.empty((v,u,n,m,w,o), order='f', dtype=np.float32)
C = np.empty((b,n,a,o,m,c), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,b,a,v,c,w", B, "v,u,n,m,w,o", beta, C, "b,n,a,o,m,c" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("ubavcw,vunmwo->bnaomc", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
