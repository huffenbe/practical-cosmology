from pylab import *

import pyccl

with open("../plotstyle.py", "r") as f:
    exec(f.read())

close("all")

h0 = 0.68
a = linspace(1e-4,.9999,1000)

z = 1/a - 1

cosmo = pyccl.cosmology.Cosmology(Omega_c = 0.25, Omega_b = 0.05, h=h0, sigma8 = 0.9, n_s = 0.96)


tlb = pyccl.background.lookback_time(cosmo, a)

DM = pyccl.background.comoving_angular_distance(cosmo, a)
DA = pyccl.background.angular_diameter_distance(cosmo, a)
DL = pyccl.background.luminosity_distance(cosmo, a)

# DH = pyccl.background.hubble_distance(cosmo, a)
DH = 1/pyccl.background.h_over_h0(cosmo,a) # not normalized
DH = DH * DA[-1]/DH[-1]/z[-1]

figure(1,figsize=[8,4])
#
#xlim(0,6)
xlim(1e-2,1e3)
ylim(0,14000)
xlabel("Redshift $z$")
ylabel("Distance (Mpc)")

semilogx()

zcirc = exp(linspace(log(0.01),log(1000),30))
acirc = 1/(1+zcirc)

ycirc = 2500*ones(len(zcirc))

angcirc = 6*2000/pyccl.background.angular_diameter_distance(cosmo, acirc)


scatter(zcirc,ycirc,angcirc, c='orange', edgecolor="black", label='Angular size of fixed physical length')

plot(z,DA, c='orange', ls="--", label="Angular diameter distance $D_A$")

plot(z,DM, label=r"Tranverse comoving distance $D_M$ ($=\chi$ since flat)")
plot(z,DL, c='green', ls="-.", label=r"Luminosity distance $D_L$")
plot(z,z*DH, c='purple', ls=":", label=r"Line-of-sight Hubble distance $z \times D_H$")
legend(loc='upper left')

show()

savefig("DA_of_z.pdf",bbox_inches="tight")
