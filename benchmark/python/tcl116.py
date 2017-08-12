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
n = 8
u = 10
w = 10
v = 10
gflops = a*b*m*o*n*u*w*v*2/1e9
A = np.empty((a,u,v,w,b), order='f', dtype=np.float32)
B = np.empty((n,u,o,m,w,v), order='f', dtype=np.float32)
C = np.empty((b,o,n,m,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,u,v,w,b", B, "n,u,o,m,w,v", beta, C, "b,o,n,m,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("auvwb,nuomwv->bonma", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
