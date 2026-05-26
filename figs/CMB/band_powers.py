from pylab import *
from healpy import *
import pymaster as nmt

with open("../plotstyle.py", "r") as f:
    exec(f.read())

close('all')

Dl = loadtxt("base_planck_lowl_lowLike_highL.bestfit_cl", usecols=[1])[:998]

Dl = hstack([[0,0],Dl])

l = arange(len(Dl))

lmax = l[-1]

llfac = l*(l+1)/2/pi

Cl = Dl / llfac
Cl[0]=Cl[1]=0

seed(12345)

nside = 512

planck857 = read_map("HFI_SkyMap_857-field-Int_2048_R3.00_full.fits")
planck857 = ud_grade(planck857,nside)

mask = smoothing(planck857,fwhm=4.0/180*pi,iter=0) < 5

mask = nmt.mask_apodization(mask, 2.5, apotype="C1")


alm0 = synalm(Cl)

cl0 = alm2cl(alm0)

m0 = alm2map(alm0,lmax=lmax,nside=nside)

#cl1 = anafast(m0,lmax=lmax,iter=0)

pcl = anafast(m0*mask,lmax=lmax,iter=0)


f_0 = nmt.NmtField(mask, [m0])
bins = nmt.NmtBin.from_nside_linear(nside, 30)

clobs = nmt.compute_full_master(f_0, f_0, bins).reshape(-1)

mollview(mask, title="Mask")

savefig("mask.pdf",bbox_inches='tight')

mollview(m0 * mask, title="Masked map", min=-400, max=400,unit=r"$\mu$K")

savefig("masked_map.pdf",bbox_inches='tight')

figure(figsize=[8,4])
plot(llfac*Cl,label="Theory $C_l$",zorder=1000)
plot(llfac*cl0,".",label=r"Unmasked $(2l+1)^{-1}\sum_m \ |a_{lm}|^2$", color='orange')
plot(llfac*pcl,".", label=r"Masked pseudo $\tilde C_l$", color='gray')
#plot(llfac[:len(cl1)]*cl1,".")

ell_arr = bins.get_effective_ells()

Nbin = bins.get_n_bands()
ell_min = zeros(Nbin)
ell_max = zeros(Nbin)

for b in range(Nbin):
    ell_min[b] = bins.get_ell_min(b)
    ell_max[b] = bins.get_ell_max(b)

ell_bin_xerr = vstack( [ ell_arr - ell_min, ell_max - ell_arr])
    
ell_arrfac = ell_arr*(ell_arr+1)/2/pi

errorbar(ell_arr,ell_arrfac*clobs,xerr=ell_bin_xerr, fmt='none', elinewidth=3, label=r"debiased, binned band powers $\mathcal{C}_b$", color="C2")

xlim(0,lmax)

xlabel("Multipole $l$")
ylabel(r"Power $l(l+1)/2\pi C_l$ ($\mu$K$^2$)")

legend()

savefig("band_powers.pdf",bbox_inches='tight')
