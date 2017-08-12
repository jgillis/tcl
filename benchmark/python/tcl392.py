import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 24
b = 20
m = 432
u = 20
w = 20
v = 20
gflops = a*b*m*u*w*v*2/1e9
A = np.empty((a,v,u,b,w), order='f', dtype=np.float32)
B = np.empty((m,u,w,v), order='f', dtype=np.float32)
C = np.empty((a,m,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,v,u,b,w", B, "m,u,w,v", beta, C, "a,m,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("avubw,muwv->amb", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
