import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 16
c = 16
b = 15
d = 16
m = 200
u = 16
v = 16
gflops = a*c*b*d*m*u*v*2/1e9
A = np.empty((c,a,d,v,b,u), order='f', dtype=np.float32)
B = np.empty((u,v,m), order='f', dtype=np.float32)
C = np.empty((a,b,c,d,m), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "c,a,d,v,b,u", B, "u,v,m", beta, C, "a,b,c,d,m" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("cadvbu,uvm->abcdm", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
