import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 24
b = 27
m = 24
o = 24
n = 27
u = 24
v = 27
gflops = a*b*m*o*n*u*v*2/1e9
A = np.empty((m,v,u,o,n), order='f', dtype=np.float32)
B = np.empty((u,a,v,b), order='f', dtype=np.float32)
C = np.empty((o,b,n,m,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "m,v,u,o,n", B, "u,a,v,b", beta, C, "o,b,n,m,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("mvuon,uavb->obnma", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
