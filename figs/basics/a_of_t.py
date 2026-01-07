from pylab import *

import pyccl

with open("../plotstyle.py", "r") as f:
    exec(f.read())



close("all")

h = 0.68
a = linspace(1e-4,.9999,1000)

cosmo = pyccl.cosmology.Cosmology(Omega_c = 0.25, Omega_b = 0.05, h=h, sigma8 = 0.9, n_s = 0.96)
tlb = pyccl.background.lookback_time(cosmo, a)

cosmo1 = pyccl.cosmology.Cosmology(Omega_c = 0.25, Omega_b = 0.05, Omega_k = 0.7, h=h, sigma8 = 0.9, n_s = 0.96)
tlb1 = pyccl.background.lookback_time(cosmo1, a)

cosmo2 = pyccl.cosmology.Cosmology(Omega_c = 0.95, Omega_b = 0.05, h=h, sigma8 = 0.9, n_s = 0.96)
tlb2 = pyccl.background.lookback_time(cosmo2, a)

cosmo3 = pyccl.cosmology.Cosmology(Omega_c = 1.95, Omega_b = 0.05, Omega_k = -1, h=h, sigma8 = 0.9, n_s = 0.96)
tlb3 = pyccl.background.lookback_time(cosmo3, a)

def cosmolabel(cosmo,pre="", post="") :
    label = r"%s$\Omega_m$=%.1f, $\Omega_\Lambda$=%.1f, $\Omega_k$=%.1f%s" % (pre,cosmo["Omega_m"], 1 - cosmo["Omega_m"] - cosmo["Omega_k"], cosmo["Omega_k"],post)
    return(label)

figsize = [9,6]

figure(1, figsize = figsize)
#plot(-tlb,a, label=r"$\Omega_m$=%.1f, $\Omega_\Lambda$=%.1f, $\Omega_k$=%.1f" % (cosmo["Omega_m"],
#                                                                  1 - cosmo["Omega_m"] - cosmo["Omega_k"],
#                                                                  cosmo["Omega_k"]))
plot(-tlb,a, label=cosmolabel(cosmo, pre=r"Flat $\Lambda$CDM: "))
plot(-tlb1,a, ls='--', label= cosmolabel(cosmo1, pre=r"Open low-mat.: ") )
plot(-tlb2,a, ls='-.', label= cosmolabel(cosmo2, pre=r"Flat mat.-dom.: ") )
plot(-tlb3,a, ls=':', label= cosmolabel(cosmo3, pre=r"Closed high-mat.: " ) )
ylabel(r"scale factor $a$")
xlabel(r"time before present $t-t_{\rm now}$ (Gyr)")

def z_of_a(a):
    return(1/a - 1)

def a_of_z(z):
    return(1/(1+z))


ax2 = gca().secondary_yaxis("right", functions=(z_of_a,a_of_z))
ax2.set_ylabel(r'redshift $z$')
ax2.set_yticks([20,10.,5.,2.,1.,0.5,0.1, 0.0])


legend()
savefig("a_of_t.pdf", bbox_inches='tight')

show()
'''
figure(2)
cosmo4 = pyccl.cosmology.Cosmology(Omega_c = 0.25, Omega_b = 0.05, h=.74, sigma8 = 0.9, n_s = 0.96)
tlb4 = pyccl.background.lookback_time(cosmo4, a)
plot(-tlb,a)
plot(-tlb4,a)
ylabel(r"scale factor $a$")
xlabel(r"time before present $t-t_{\rm now}$ (Gyr)")

'''



h_over_h0 = pyccl.background.h_over_h0(cosmo, a)

h_over_h0_1 = pyccl.background.h_over_h0(cosmo1, a)
h_over_h0_2 = pyccl.background.h_over_h0(cosmo2, a)
h_over_h0_3 = pyccl.background.h_over_h0(cosmo3, a)

figure(2, figsize=figsize)
plot(-tlb,a*h_over_h0, ls='-', label=cosmolabel(cosmo, pre=r"Flat $\Lambda$CDM: "))
plot(-tlb1,a*h_over_h0_1, ls='--', label=cosmolabel(cosmo1, pre=r"Open low-mat.: "))
plot(-tlb2,a*h_over_h0_2, ls='-.', label=cosmolabel(cosmo2, pre=r"Flat mat.-dom.: "))
plot(-tlb3,a*h_over_h0_3, ls=':', label=cosmolabel(cosmo3, pre=r"Closed high-mat.: " ))
ylabel(r"Expansion rate $\dot a/H_0 = aH/H_0$")
xlabel(r"time before present $t-t_{\rm now}$ (Gyr)")



legend()
ylim(ymin=0.5, ymax=3)

#ax3 = gca().secondary_xaxis("top", functions=(z_of_t,t_of_z))

axhline(1.0, c = "gray", ls=":")

#semilogy()

savefig("expansion_rate.pdf", bbox_inches='tight')


'''

figure(3, figsize=[9,4])
plot(a,h_over_h0, label=cosmolabel(cosmo, pre=r"Flat $\Lambda$CDM: "))
plot(a,h_over_h0_1, label=cosmolabel(cosmo1, pre=r"Flat $\Lambda$CDM: "))
plot(a,h_over_h0_2, label=cosmolabel(cosmo2, pre=r"Flat $\Lambda$CDM: "))
plot(a,h_over_h0_3, label=cosmolabel(cosmo3, pre=r"Flat $\Lambda$CDM: "))
semilogy()
'''
