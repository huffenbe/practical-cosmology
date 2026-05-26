import camb
import os
import matplotlib.gridspec as gridspec
from pylab import *

with open("../plotstyle.py", "r") as f:
    exec(f.read())

print('Using CAMB %s installed at %s' % (camb.__version__, os.path.dirname(camb.__file__)))

close('all')


p = {'H0' : 67.5,
     'ombh2' : 0.022,
     'omch2' : 0.122,
     'mnu' : 0.06,
     'omk' : 0,
     'tau' : 0.06,
     'As' : 2.1e-9,
     'ns' : 0.965,
     'num_nu_massless' : 2.0293333333333337
     }

pars = camb.set_params(H0=p['H0'],
                       ombh2=p['ombh2'],
                       omch2=p['omch2'],
                       mnu=p['mnu'],
                       omk=p['omk'],
                       tau=p['tau'],
                       As=p['As'],
                       ns=p['ns'],
                       num_nu_massless=p['num_nu_massless'],
                       halofit_version='mead',
                       lmax=3000
                       )


# Now get matter power spectra and sigma8 at redshift 0 and 0.8
# parameters can all be passed as a dict as above, or you can call
# separate functions to set up the parameter object

# Note non-linear corrections couples to smaller scales than you want
pars.set_matter_power(redshifts=[0.0, 2,5], kmax=2.0)

# Linear spectra
pars.NonLinear = camb.model.NonLinear_none
results = camb.get_results(pars)
kh, z, pk = results.get_matter_power_spectrum(minkh=1e-4, maxkh=1, npoints=200)
s8 = np.array(results.get_sigma8())

# Non-Linear spectra (Halofit)
pars.NonLinear = camb.model.NonLinear_both
results.calc_power_spectra(pars)
kh_nonlin, z_nonlin, pk_nonlin = results.get_matter_power_spectrum(minkh=1e-4, maxkh=1, npoints=200)

print('sigma 8 values at the two redshifts:', results.get_sigma8())


h = p['H0']/100

figure()
plot(kh*h,pk[0,:])
plot(kh_nonlin*h,pk_nonlin[0,:], label=r"z=%.1f" % (z[0]) )

plot(kh*h,pk[1,:])
plot(kh_nonlin*h,pk_nonlin[1,:], label=r"z=%.1f" % (z[1]) )

plot(kh*h,pk[2,:])
plot(kh_nonlin*h,pk_nonlin[2,:], label=r"z=%.1f" % (z[2]) )

legend()
xlabel(r"Wavenumber $k$ (Mpc$^{-1}$)")
ylabel(r"Matter power spectrum $P(k)$ (Mpc$^{3}$)")


loglog()


savefig("Pk.pdf", bbox_inches='tight')
