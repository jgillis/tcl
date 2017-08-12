import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 8
c = 9
b = 10
d = 8
m = 96
u = 10
v = 10
gflops = a*c*b*d*m*u*v*2/1e9
A = np.empty((a,d,b,u,v,c), order='f', dtype=np.float32)
B = np.empty((m,v,u), order='f', dtype=np.float32)
C = np.empty((d,a,c,m,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,d,b,u,v,c", B, "m,v,u", beta, C, "d,a,c,m,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("adbuvc,mvu->dacmb", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC