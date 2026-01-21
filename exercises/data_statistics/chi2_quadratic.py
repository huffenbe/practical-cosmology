from pylab import *
import scipy


close('all')
seed(124353)

x = arange(-3,4,1)

A = 3.2

s = A * x**2

sigma = array([4,2,4,1,2,2,6])

n = sigma * normal(size=7)

d = s + n

dround = rint(10 * d)/10

Atest = linspace(2.,4.,1000)

stest = outer(Atest, x**2)

dum, dtest = meshgrid(Atest, dround, indexing='ij')

dum, sigma2test = meshgrid(Atest, sigma**2, indexing='ij') 

chi2 = sum( (dtest-stest)**2/sigma2test , axis=1)

Amin = Atest[ argmin(chi2) ]

print("dround = ",dround)
print("sigma = ",sigma)

xSNmax = x[argmax(x**2/sigma)]

print("Amin=",Amin)

chi2min = amin(chi2)

p = scipy.stats.chi2.sf(chi2min, 6)

print("chi2min=",chi2min)
print("p=",p)

pA = scipy.stats.chi2.sf(chi2, 6)


figure(1)
scatter(x,s)
errorbar(x,d,sigma,ls='')
grid()

figure(2)
plot(Atest, chi2)

figure(3)
plot(Atest,pA)
axhline(0.05)
