import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 12
c = 16
b = 12
d = 12
m = 12
n = 16
u = 144
gflops = a*c*b*d*m*n*u*2/1e9
A = np.empty((u,n,m), order='f', dtype=np.float32)
B = np.empty((c,u,b,a,d), order='f', dtype=np.float32)
C = np.empty((n,a,c,d,m,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,n,m", B, "c,u,b,a,d", beta, C, "n,a,c,d,m,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("unm,cubad->nacdmb", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
