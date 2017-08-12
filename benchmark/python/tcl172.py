import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 16
b = 20
m = 16
o = 18
n = 16
u = 324
gflops = a*b*m*o*n*u*2/1e9
A = np.empty((n,o,u,m), order='f', dtype=np.float32)
B = np.empty((a,b,u), order='f', dtype=np.float32)
C = np.empty((m,o,n,b,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "n,o,u,m", B, "a,b,u", beta, C, "m,o,n,b,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("noum,abu->monba", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
