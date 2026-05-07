from pylab import *
from astropy import units as u
from scipy.ndimage import gaussian_filter


with open("../../figs/plotstyle.py", "r") as f:
    exec(f.read())

close('all')

seed(1236234)

Dlmc = 50 * u.kpc

D = 0.8 * u.Mpc

Deltam = -2.5*log10( (D/Dlmc)**2 )


mmin = 16.2 - Deltam  # the brightest



t = linspace(0,4*pi,800)

pt = -0.40*pi #phase

mobs = (t+pt)/2/pi - floor((t+pt)/2/pi)



mobs = gaussian_filter(mobs, 0.25/4*len(t), mode='wrap')

mobs *= -0.6 / (amax(mobs)-amin(mobs))

mobs = mobs - amin(mobs) + mmin 

mobs += 0.05*normal(size=len(t))

figure(1,figsize=[8,2.5])
scatter(t/2/pi*10.5,mobs)
xlim(0,21)
ylim(23.0,22.0)

ylabel(r'I-band magnitude, $m_{I}$')
xlabel('time (days)')


savefig("fake_cepheidII_800kpc.pdf",bbox_inches='tight')
