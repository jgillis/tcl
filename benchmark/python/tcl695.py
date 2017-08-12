import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 25
b = 24
m = 24
n = 25
u = 25
w = 25
v = 25
gflops = a*b*m*n*u*w*v*2/1e9
A = np.empty((m,v,n,w,u), order='f', dtype=np.float32)
B = np.empty((b,u,w,v,a), order='f', dtype=np.float32)
C = np.empty((m,a,n,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "m,v,n,w,u", B, "b,u,w,v,a", beta, C, "m,a,n,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("mvnwu,buwva->manb", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
