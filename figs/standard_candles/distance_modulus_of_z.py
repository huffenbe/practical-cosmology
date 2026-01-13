from pylab import *

import pyccl

with open("../plotstyle.py", "r") as f:
    exec(f.read())

close("all")

h0 = 0.68
a = linspace(1e-4,.9999,1000)

z = 1/a - 1

cosmo = pyccl.cosmology.Cosmology(Omega_c = 0.25, Omega_b = 0.05, h=h0, sigma8 = 0.9, n_s = 0.96)
cosmo1 = pyccl.cosmology.Cosmology(Omega_c = 0.25, Omega_b = 0.05, Omega_k = 0.7, h=h0, sigma8 = 0.9, n_s = 0.96)
cosmo2 = pyccl.cosmology.Cosmology(Omega_c = 0.95, Omega_b = 0.05, h=h0, sigma8 = 0.9, n_s = 0.96)
cosmo3 = pyccl.cosmology.Cosmology(Omega_c = 1.95, Omega_b = 0.05, Omega_k = -1, h=h0, sigma8 = 0.9, n_s = 0.96)


mu = pyccl.background.distance_modulus(cosmo, a)
mu1 = pyccl.background.distance_modulus(cosmo1, a)
mu2 = pyccl.background.distance_modulus(cosmo2, a)
mu3 = pyccl.background.distance_modulus(cosmo3, a)

def cosmolabel(cosmo,pre="", post="") :
    label = r"%s$\Omega_m$=%.1f, $\Omega_\Lambda$=%.1f, $\Omega_k=%.1f$%s" % (pre,cosmo["Omega_m"], 1 - cosmo["Omega_m"] - cosmo["Omega_k"], cosmo["Omega_k"],post)
    return(label)


figure(1,figsize=[12,4])
plot(z,mu, label=cosmolabel(cosmo, pre=r"Flat $\Lambda$CDM: "))
plot(z,mu1, ls='--', label= cosmolabel(cosmo1, pre=r"Open low-mat.: "))
plot(z,mu2, ls='-.', label= cosmolabel(cosmo2, pre=r"Flat mat.-dom.: "))
plot(z,mu3, ls=':', label= cosmolabel(cosmo3, pre=r"Closed high-mat.: " ))

semilogx()
xlim(8e-4,2.5)
ylim(27,48)
yticks(arange(30,50,5))
gca().yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(5))

xlabel("Redshift $z$")
ylabel(r"Distance modulus $\mu$ (mag)")

legend()

savefig("distance_modulus_of_z.pdf",bbox_inches="tight")



figure(2,figsize=[12,4])
plot(z,mu-mu, label=cosmolabel(cosmo, pre=r"Flat $\Lambda$CDM: "))
plot(z,mu1-mu, ls='--', label= cosmolabel(cosmo1, pre=r"Open low-mat.: "))
plot(z,mu2-mu, ls='-.', label= cosmolabel(cosmo2, pre=r"Flat mat.-dom.: "))
plot(z,mu3-mu, ls=':', label= cosmolabel(cosmo3, pre=r"Closed high-mat.: " ))

semilogx()
xlim(8e-4,2.5)
ylim(-0.7,0.7)
#yticks(arange(30,50,5))
gca().yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(4))

xlabel("Redshift $z$")
ylabel(r"$\mu - \mu_{\rm \Lambda CDM}$ (mag)")

legend(loc='upper left')
savefig("distance_modulus_diff_of_z.pdf",bbox_inches="tight")
