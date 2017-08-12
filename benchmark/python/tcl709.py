import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 15
c = 15
b = 15
d = 16
m = 16
n = 15
u = 16
v = 16
gflops = a*c*b*d*m*n*u*v*2/1e9
A = np.empty((u,b,v,c,a,d), order='f', dtype=np.float32)
B = np.empty((v,m,n,u), order='f', dtype=np.float32)
C = np.empty((d,a,b,m,c,n), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,b,v,c,a,d", B, "v,m,n,u", beta, C, "d,a,b,m,c,n" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("ubvcad,vmnu->dabmcn", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC