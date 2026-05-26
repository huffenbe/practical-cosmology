from pylab import *
from healpy import *


close('all')

Dl = loadtxt("base_planck_lowl_lowLike_highL.bestfit_cl", usecols=[1])

Dl = hstack([[0,0],Dl])

l = arange(len(Dl))

lmax = l[-1]

Cl = 2*pi/l/(l+1)* Dl
Cl[0]=Cl[1]=0

seed(12345)

nside = 128

alm0 = synalm(Cl)


fwhm = array([1/60,1,10]) * pi/180

Nbeam = len(fwhm)

bl = array([gauss_beam(f, lmax) for f in fwhm])


alm = array([almxfl(alm0, b1) for b1 in bl])

clobs = array([alm2cl(a) for a in alm])

s = array([alm2map(a,nside) for a in alm])



fig = figure(figsize=(12, 8))

# Define a 4-row, 2-column grid
# width_ratios can adjust the relative width of the columns
gs = fig.add_gridspec(Nbeam, 2, width_ratios=[1, 2])

# Left Column: 4 individual plots
#axleft = [ fig.add_subplot(gs[i, 0]) for i in range(Nbeam) ]

# Right Column: 1 plot spanning all 4 rows
axright = fig.add_subplot(gs[0:Nbeam, 1])


for i in range(Nbeam):
    mollview(
        s[i], 
        sub=(Nbeam,3,i*3+1),              # <--- This is the key argument
        title=f"beam FWHM = {fwhm[i]*60*180/pi:0.0f} arcmin",
        cbar = False
    )

for i in range(Nbeam):
    axright.plot(l*(l+1)/2/pi*clobs[i], label=f"beam  FWHM = {fwhm[i]*60*180/pi:0.0f} arcmin")

axright.plot(Dl, label="Theory")

axright.set_ylim(40,6000)
axright.set_xlim(2,None)

axright.set_xlabel(r"Multipole $l$")
axright.set_ylabel(r"Power $l(l+1)/2\pi\ C_l$")

axright.loglog()

axright.legend()

# Clean up layout
plt.tight_layout()
plt.show()



fig.savefig("beam_demo.pdf")
