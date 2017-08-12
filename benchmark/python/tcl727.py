import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 256
u = 256
m = 256
n = 243
gflops = a*u*m*n*2/1e9
A = np.empty((m,n,u), order='f', dtype=np.float32)
B = np.empty((u,a), order='f', dtype=np.float32)
C = np.empty((m,a,n), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "m,n,u", B, "u,a", beta, C, "m,a,n" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("mnu,ua->man", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
