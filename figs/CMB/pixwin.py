from pylab import *

import astropy.io.fits as fits

with open("../plotstyle.py", "r") as f:
    exec(f.read())


close('all')


nsides = [32,128, 512, 2048, 8192]

figure(1)

for nside in nsides:
    filename = f"/home/huffenbe/install/healpy-data/pixel_window_functions/pixel_window_n{nside:04d}.fits"

    print(filename)


    hdulist = fits.open(filename)

    wT = hdulist[1].data['TEMPERATURE']
    
    plot(wT,label=f"{nside}")


semilogx()
xlabel(r"Multipole $l$")
ylabel(r"Pixel window $w_l$")
legend(title=r"HEALPix $N_{\rm side}$")

savefig("healpix_pixwin.pdf",bbox_inches='tight')
