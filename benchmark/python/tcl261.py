import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 40
b = 40
m = 8
o = 12
n = 8
u = 8
w = 12
v = 12
gflops = a*b*m*o*n*u*w*v*2/1e9
A = np.empty((n,w,m,u,o,v), order='f', dtype=np.float32)
B = np.empty((u,v,w,a,b), order='f', dtype=np.float32)
C = np.empty((m,o,b,a,n), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "n,w,m,u,o,v", B, "u,v,w,a,b", beta, C, "m,o,b,a,n" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("nwmuov,uvwab->moban", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
