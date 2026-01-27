from pylab import *
import pyccl
import astropy.units as u

close('all')

h0=0.7
H0 = h0 * 100 * u.km / u.s / u.Mpc
cosmo = pyccl.cosmology.Cosmology(Omega_c = 0.25, Omega_b = 0.05, h=h0, sigma8 = 0.9, n_s = 0.96)



MBfid = -19.3  # +/- 0.3  # fiducial B-band absolute magnitude

pMBfid = MBfid - 5*log10( H0 / (1 * u.km/u.s/u.Mpc)) + 25 # pMB for pseudo MB

alpha = 0.15
beta = 3.1

# Natural variation in x1 and c
sigx1_nat = 1.0
sigc_nat = 0.1


NSN = 4

seed(123456)

zmin = 0.3
zmax = 1.5

z = floor( sort(uniform(zmin,zmax,size=NSN)) *100)/100

a = 1/(1+z)

DL = pyccl.background.luminosity_distance(cosmo, a)*u.Mpc
mu = pyccl.background.distance_modulus(cosmo, a)

H0DL = H0 * DL

# Assign / find the true values that characterize the supernovae
x10 = sigx1_nat * normal(size=NSN)
c0 = sigc_nat * normal(size=NSN)

MB0 = MBfid - alpha*x10 + beta*c0
mB0 = MB0 + mu

# Add errors to the three data products, equal parts variance to each component
sigSN = 0.05

varSN = sigSN**2

sigmB = sqrt( varSN / 3) 
sigx1 = sqrt( varSN / 3 / alpha**2)
sigc = sqrt( varSN / 3 / beta**2 )

# Compute the data

mB = mB0 + sigmB * normal(size=NSN)
x1 = x10 + sigx1 * normal(size=NSN)
c = c0 + sigc * normal(size=NSN)

print("z",z)
print("mB",mB)
print("x1",x1)
print("c",c)

#####   Print latex data table for exercise

print("%%%%%%%%%%%%%%%%%%%%%%%")
print("\\begin{tabular}{l|c|c|c|c}")
print("  & $z$ & $m_B$ & $x_1$ & $c$ \\\\  \\hline")


for i in range(NSN):
    print(f"SN {i:d} & ", end='')
    print(z[i],"& ", end='')
    print(f"{mB[i]:.5g} & ", end='')
    print(f"{x1[i]:.4g} & ", end='')
    print(f"{c[i]:.4g} ", end='')
    print("\\\\")

print("\\hline")
print(f"$\\sigma$ uncertainty & 0.0 & {sigmB:.3g} & {sigx1:.3g} & {sigc:.3g} \\\\")


print("\\end{tabular}")
print("%%%%%%%%%%%%%%%%%%%%%%%")


#### Check the difference

test0 =   5*log10( H0DL / (1* u.km/u.s)) - (mB0 - pMBfid + alpha*x10 - beta*c0)

test = 5*log10( H0DL / (1* u.km/u.s)) - (mB - pMBfid + alpha*x1 - beta*c)

print("test0", test0  )
print("test", test  )

ztest = linspace(zmin,zmax,100)
H0DLtest = H0 * pyccl.background.luminosity_distance(cosmo, 1/(1+ztest)) * u.Mpc


figure(1)
scatter(z,(mB0 - pMBfid + alpha*x10 - beta*c0), marker="+" )
errorbar(z,(mB - pMBfid + alpha*x1 - beta*c), sigSN , fmt='.')

plot(ztest, 5*log10( H0DLtest / (1* u.km/u.s) ) )

for Omegamtest in arange(0.1,0.5,0.05) :
    
    cosmotest = pyccl.cosmology.Cosmology(Omega_c = Omegamtest - 0.05, Omega_b = 0.05, h=h0, sigma8 = 0.9, n_s = 0.96)
    H0DLtest = H0 * pyccl.background.luminosity_distance(cosmotest, 1/(1+ztest)) * u.Mpc
    plot(ztest, 5*log10( H0DLtest / (1* u.km/u.s) ), lw=0.5, color='k' )



xlabel('z')
ylabel('5 log10 (H0DL/1 km/s)')
show()

####  Start to calculate

def likelihood(Omegam,pMB,alpha,beta, mB, z, x1, c, sigSN) :

    cosmotest = pyccl.cosmology.Cosmology(Omega_c = Omegam - 0.05, Omega_b = 0.05, h=h0, sigma8 = 0.9, n_s = 0.96)
    H0DLtest = H0 * pyccl.background.luminosity_distance(cosmotest, 1/(1+z)) * u.Mpc

    test = 5*log10( H0DLtest / (1* u.km/u.s) ) - (mB - pMB + alpha*x1 - beta*c)
    
    # print(H0DLtest)
    # print(test)
   
    chi2 = sum(test**2/sigSN**2 )

    # print(chi2)
    
    Like = exp(-chi2/2)

    return(Like)

Ntest_alpha = 100

alphatest = linspace(0.05,0.25,Ntest_alpha)

Ltestalpha = zeros(Ntest_alpha)

for itest,alf in enumerate(alphatest) :
    Ltestalpha[itest] = likelihood(0.3,pMBfid,alf,beta, mB, z, x1, c, sigSN)

figure(4)
plot(alphatest,Ltestalpha)


Ntest_Omega = 100

Ltest = zeros(Ntest_Omega)
Omegamtest = linspace(0.15,0.40,Ntest_Omega)


for itest, Omegam in enumerate(Omegamtest) :

    Ltest[itest] = likelihood(Omegam,pMBfid,alpha,beta, mB, z, x1, c, sigSN)


figure(2)
plot(Omegamtest,Ltest)
xlabel('Omegam')
ylabel('likelihood')

Ntest=5

L2dtest = zeros([Ntest,Ntest])
pMBtest = linspace(-3.7,-3.4,Ntest)
Omegamtest = linspace(0.15,0.40,Ntest)


for jtest, pMB1 in enumerate(pMBtest) :
    for itest, Omegam in enumerate(Omegamtest) :

        L2dtest[jtest,itest] = likelihood(Omegam,pMB1,alpha,beta, mB, z, x1, c, sigSN)


figure(3)

imshow(L2dtest, extent=[amin(Omegamtest),amax(Omegamtest),amin(pMBtest),amax(pMBtest)], origin='lower')


#####################



