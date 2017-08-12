import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 16
c = 15
b = 16
m = 60
n = 60
u = 16
w = 16
v = 16
gflops = a*c*b*m*n*u*w*v*2/1e9
A = np.empty((a,b,u,c,v,w), order='f', dtype=np.float32)
B = np.empty((u,m,v,n,w), order='f', dtype=np.float32)
C = np.empty((a,n,m,b,c), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,b,u,c,v,w", B, "u,m,v,n,w", beta, C, "a,n,m,b,c" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("abucvw,umvnw->anmbc", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
