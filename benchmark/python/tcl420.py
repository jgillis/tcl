import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 16
c = 12
b = 12
m = 1800
u = 12
w = 12
v = 16
gflops = a*c*b*m*u*w*v*2/1e9
A = np.empty((v,m,u,w), order='f', dtype=np.float32)
B = np.empty((a,c,v,w,u,b), order='f', dtype=np.float32)
C = np.empty((m,c,a,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "v,m,u,w", B, "a,c,v,w,u,b", beta, C, "m,c,a,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("vmuw,acvwub->mcab", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
