import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 16
c = 16
b = 16
d = 16
m = 16
n = 15
u = 16
v = 16
gflops = a*c*b*d*m*n*u*v*2/1e9
A = np.empty((m,u,v,n), order='f', dtype=np.float32)
B = np.empty((v,b,a,d,u,c), order='f', dtype=np.float32)
C = np.empty((m,c,a,n,d,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "m,u,v,n", B, "v,b,a,d,u,c", beta, C, "m,c,a,n,d,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("muvn,vbaduc->mcandb", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
