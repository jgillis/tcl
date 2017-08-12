import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 9
c = 10
b = 8
m = 972
u = 10
w = 8
v = 10
gflops = a*c*b*m*u*w*v*2/1e9
A = np.empty((w,v,b,u,c,a), order='f', dtype=np.float32)
B = np.empty((w,u,v,m), order='f', dtype=np.float32)
C = np.empty((b,a,m,c), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "w,v,b,u,c,a", B, "w,u,v,m", beta, C, "b,a,m,c" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("wvbuca,wuvm->bamc", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC