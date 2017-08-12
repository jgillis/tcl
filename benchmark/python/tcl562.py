import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 15
c = 15
b = 16
d = 15
m = 16
n = 15
u = 15
v = 16
gflops = a*c*b*d*m*n*u*v*2/1e9
A = np.empty((v,m,n,u), order='f', dtype=np.float32)
B = np.empty((b,a,c,d,v,u), order='f', dtype=np.float32)
C = np.empty((m,c,a,n,b,d), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "v,m,n,u", B, "b,a,c,d,v,u", beta, C, "m,c,a,n,b,d" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("vmnu,bacdvu->mcanbd", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
