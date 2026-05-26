from pylab import *
import camb
import os
import matplotlib.gridspec as gridspec

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

dp = {'H0' : 7.0,
     'ombh2' : 0.005,
     'omch2' : 0.03,
     'mnu' : 0.05,
     'omk' : 0.1,
     'tau' : 0.04,
     'As' : 2e-10,
     'ns' : 0.1,
     'num_nu_massless' : 1
     }

prettyname = {'H0' : r"$H_0$",
     'ombh2' : r"$\omega_b = \Omega_b h^2$",
     'omch2' : r"$\omega_c = \Omega_c h^2$",
     'mnu' : r"$m_\nu$ (eV)",
     'omk' : r"$\Omega_k$",
     'tau' : r"$\tau$",
     'As' : r"$A_s$",
     'ns' : r"$n_s$",
     'num_nu_massless' : r"$N_{\nu}(m=0) = N_{\nu,\rm eff} - 1$"
     }

'''
fig = figure(figsize=[15,10],layout='constrained')
gs = gridspec.GridSpec(3,3,figure=fig)

gss = {'H0' : gs[0,0],
     'ombh2' : gs[1,0],
     'omch2' : gs[0,1],
     'mnu' : gs[2,2],
     'omk' : gs[0,2],
     'tau' : gs[2,0],
     'As' : gs[1,1],
     'ns' : gs[1,2],
     'num_nu_massless' : gs[2,1]
     }
'''

fig = figure(figsize=[10,14],layout='constrained')
gs = gridspec.GridSpec(4,2,figure=fig)

gss = {'H0' : gs[0,1],
     'ombh2' : gs[1,1],
     'omch2' : gs[1,0],
     'mnu' : gs[3,1],
     'omk' : gs[0,0],
     'tau' : gs[3,0],
     'As' : gs[2,0],
     'ns' : gs[2,1],
     'num_nu_massless' : gs[3,1]
     }


axs = {}
for k in gss.keys() :
    axs[k] = fig.add_subplot(gss[k])



p1 = p
        
pars = camb.set_params(H0=p1['H0'],
                       ombh2=p1['ombh2'],
                       omch2=p1['omch2'],
                       mnu=p1['mnu'],
                       omk=p1['omk'],
                       tau=p1['tau'],
                       As=p1['As'],
                       ns=p1['ns'],
                       num_nu_massless=p1['num_nu_massless'],
                       halofit_version='mead',
                       lmax=3000
                       )

# calculate results for these parameters
results = camb.get_results(pars)

powers0 = results.get_cmb_power_spectra(pars, CMB_unit='muK')



for k in p.keys() :

    p1 = p.copy()

    p1[k] += dp[k]

    
    pars = camb.set_params(H0=p1['H0'],
                           ombh2=p1['ombh2'],
                           omch2=p1['omch2'],
                           mnu=p1['mnu'],
                           omk=p1['omk'],
                           tau=p1['tau'],
                           As=p1['As'],
                           ns=p1['ns'],
                           num_nu_massless=p1['num_nu_massless'],
                           halofit_version='mead',
                           lmax=3000
                           )

    # calculate results for these parameters
    results = camb.get_results(pars)

    pplus = p1.copy()
    powersplus = results.get_cmb_power_spectra(pars, CMB_unit='muK')

    p1 = p.copy()
    p1[k] -= dp[k]

    
    pars = camb.set_params(H0=p1['H0'],
                           ombh2=p1['ombh2'],
                           omch2=p1['omch2'],
                           mnu=p1['mnu'],
                           omk=p1['omk'],
                           tau=p1['tau'],
                           As=p1['As'],
                           ns=p1['ns'],
                           num_nu_massless=p1['num_nu_massless'],
                           halofit_version='mead',
                           lmax=3000
                           )

    # calculate results for these parameters
    results = camb.get_results(pars)

    pminus = p1.copy()
    powersminus = results.get_cmb_power_spectra(pars, CMB_unit='muK')


    
    print(p)
    print(pplus)
    print(pminus)
    

    axs[k].plot(powersplus['total'][2:,0],label=f"{pplus[k]:.3g}")
    axs[k].plot(powers0['total'][2:,0],label=f"{p[k]:.3g} (fid.)")
    axs[k].plot(powersminus['total'][2:,0],label=f"{pminus[k]:.3g}")

    axs[k].set_ylim(ymin=-50,ymax=6100)
    axs[k].legend(title=prettyname[k])
    
    show()
    
fig.supylabel(r"Power $D_l = l(l+1)/2\pi \ C_l$ ($\mu$K$^2$)")
fig.supxlabel(r"Multipole $l$")

savefig("cmb_params.pdf",bbox_inches='tight')
