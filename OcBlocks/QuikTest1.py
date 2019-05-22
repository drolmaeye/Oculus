from epics import *
import time
import timeit


pv = PV('16TEST1:scan1.D02NV')

ai = time.clock()
a = pv.value
af = time.clock() - ai

bi = time.clock()
b = caget('16TEST1:scan1.D01NV')
bf = time.clock() - bi

ci = time.clock()
c = pv.value
cf = time.clock() - ci

di = time.clock()
d = caget('16TEST1:scan1.D01NV')
df = time.clock() - di



print af, bf, cf, df

