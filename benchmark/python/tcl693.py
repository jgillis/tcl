import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 25
b = 24
m = 24
n = 24
u = 25
w = 25
v = 25
gflops = a*b*m*n*u*w*v*2/1e9
A = np.empty((m,n,w,u,v), order='f', dtype=np.float32)
B = np.empty((b,u,w,v,a), order='f', dtype=np.float32)
C = np.empty((n,a,m,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "m,n,w,u,v", B, "b,u,w,v,a", beta, C, "n,a,m,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("mnwuv,buwva->namb", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
