from pylab import *
import pyccl
import astropy.units as u
from astropy.constants import c

H0ref = 100*u.km/u.s/u.Mpc
z = 5.
a = 1/(1+z)

H0 = array([65,70,75])*u.km/u.s/u.Mpc

chiflat =  zeros(len(H0))*u.Mpc
chiopen =  zeros(len(H0))*u.Mpc

DLflat = zeros(len(H0))*u.Mpc
DLopen = zeros(len(H0))*u.Mpc

R0 = zeros(len(H0))*u.Mpc

#pyccl.gsl_params['INTEGRATION_DISTANCE_EPSREL'] = 1e-4
#pyccl.gsl_params['N_ITERATION'] = 4000

for i in range(len(H0)) :

    cosmoflat = pyccl.cosmology.Cosmology(Omega_c = 0.25, Omega_b = 0.05, h=(H0[i]/H0ref).value, sigma8 = 0.9, n_s = 0.96)
    cosmoopen = pyccl.cosmology.Cosmology(Omega_c = 0.25, Omega_b = 0.05, Omega_k = 0.7, h=(H0[i]/H0ref).value, sigma8 = 0.9, n_s = 0.96)

    R0[i] = c/H0[i]/sqrt(fabs(cosmoopen["Omega_k"]))
    
    chiflat[i] = pyccl.background.comoving_radial_distance(cosmoflat, a)*u.Mpc
    chiopen[i] = pyccl.background.comoving_radial_distance(cosmoopen, a)*u.Mpc
 
    DLflat[i] = pyccl.background.luminosity_distance(cosmoflat, a)*u.Mpc
    DLopen[i] = pyccl.background.luminosity_distance(cosmoopen, a)*u.Mpc


print("Flat: H0=",H0,"\tchi=",chiflat,"\tH0chi=", H0*chiflat, "\trel=", H0*chiflat/H0[1]/chiflat[1])
print("Open: H0=",H0,"\tchi=",chiopen,"\tH0chi=", H0*chiopen, "\trel=", H0*chiopen/H0[1]/chiopen[1])


print("Flat: H0=",H0,"\tDL=",DLflat,"\tH0DL=", H0*DLflat, "\trel=", H0*DLflat/H0[1]/DLflat[1])
print("Open: H0=",H0,"\tDL=",DLopen,"\tH0DL=", H0*DLopen, "\trel=", H0*DLopen/H0[1]/DLopen[1])

