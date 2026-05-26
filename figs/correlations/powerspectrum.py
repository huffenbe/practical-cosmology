from pylab import *
import sys
from scipy import ndimage

sys.path.append("/home/huffenbe/projects/timeseries_masked_powerspectrum")

from timeseries_masked_powerspectrum import *

with open("../plotstyle.py", "r") as f:
    exec(f.read())


L = 6000. # Mpc
Nsamples = 768

Nreal = 100000
Nbands = 15


seed(1234123)
close('all')

Deltax = L/Nsamples
x = Deltax * arange(Nsamples)

k, Deltak = fourier_frequencies(Nsamples,Deltax)

Nfreq = len(k)

kc = 0.003
Pth = 500*(1+k/kc)**-3

#############
#
#  Compute the mask and modecoupling matrix
#
######################
w = 0.0 + (800 < x)*(x < 2340) + (2600 < x)*(x < 3990) + (4200 < x)*(x < 5400)
w  = ndimage.gaussian_filter1d(w, 2.0)

fsky = sum(w)/Nsamples

bins = binning(k,Nbands,weights=ones(Nfreq),funcdep=ones(Nfreq),binning='log')
Wkwork = mode_coupling_workspace(w,Deltax,Deltak,bins)

WPth = array(Wkwork['modecoupling']*matrix(Pth).T).flatten()




######
#
# Make space for the realizations
#
#####
ak = zeros([Nreal,len(k)],dtype=complex)
Prandom = zeros([Nreal,len(k)],dtype=float)
a = zeros([Nreal,Nsamples],dtype=float)

wa = zeros([Nreal,Nsamples],dtype=float)

wak = zeros([Nreal,len(k)],dtype=complex)
wPrandom = zeros([Nreal,len(k)],dtype=float)

pseudo_binned_Pk = zeros([Nreal,Nbands])
unbiased_binned_Pk = zeros([Nreal,Nbands])



for i in range(Nreal) :

    ak[i] = Pom_to_fourier_coefs(Pth,k)
    Prandom[i] = fourier_coefs_to_powerspec(ak[i], Deltak)

    a[i] = fourier_coefs_to_timeseries(ak[i],Deltak)

    wa[i] = w*a[i]   #(a[i] - average(a[i]))
    wak[i] = timeseries_to_fourier_coefs(wa[i],Deltax)
    wPrandom[i] = fourier_coefs_to_powerspec(wak[i], Deltak)


    pseudo_binned_Pk[i] = bin_Pom(wPrandom[i],bins)

    unbiased_binned_Pk[i] = unbias_power_spectrum(pseudo_binned_Pk[i], Wkwork)


#########################
#
#  Plotting!
#
##########################
 
fsize = [12,9]

figure(1,figsize=fsize)  
subplot(211)
plot(k,Pth, lw=3, label=r'Theory $P(k)$')
plot(k,Prandom[0],'.', label=r'Random $|a(k_q)|^2 \Delta k /2\pi$')

loglog()

ylim()
legend(loc="upper right")
xlabel(r"Wavenumber $k$ (Mpc$^{-1}$)")
ylabel(r"Power ([signal]$^{2}$)")


subplot(212)
skip = 2.0

for i in range(5) :
    plot(x,a[i]+skip*i)
    axhline(skip*i,c='k',ls=":")
xlabel(r"Comoving position $x$ (Mpc)")
ylabel(r"Signal")
xlim(0,L)

savefig("Pk_randoms.pdf",bbox_inches='tight')

########################
########################
########################

figure(2,figsize=[12,12])

subplot(311)
i = 4

plot(x,w,label=r"mask $w(x)$")
plot(x,a[i], ls=":", lw=0.75) #, label=r"signal $a(x)$")
plot(x,wa[i], label=r"masked signal $w(x)a(x)$")

xlabel(r"Comoving position $x$ (Mpc)")
ylabel(r"Signal")

legend(loc='upper right')


####
subplot(312)
plot(k,array(Wkwork['modecoupling'][:,0]).flatten(), label=r"$W_{q0} = |w_q|^2$")
#plot(k,array(diag(Wkwork['modecoupling'])).flatten(), label=r"$W_{pp}$")
#axhline(fsky,c='k',ls=":",label='mask fraction $f$')

loglog()
ylabel(r'Mode coupling $W$')
legend()

#####
subplot(313)

plot(k,average(wPrandom,axis=0)/Pth,'.',c='C2', label=r"Average pseudo-spectrum $ \tilde P(k)/P(k)$")
plot(k,WPth/Pth, label=r'mode-coupled theory $(WP)(k)/P(k)$')

axhline(1.0,c='gray',ls="-",lw=0.5)#,label='unbiased')

axhline(fsky,c='k',ls=":",label='mask fraction $f$')

#ylim(ymin=1e-6)
#loglog()
semilogx()
xlabel(r"Wavenumber $k$ (Mpc$^{-1}$)")
ylabel(r"pseudo-power ratio $\tilde P(k)/P(k)$")

annotate('unbiased', xy=(0.3,1.03), color='gray',zorder=0)

legend()



savefig("mask_pseudoPk.pdf",bbox_inches='tight')



##############
##############
##############

figure(3,figsize=[12,12])
subplot(311)

plot(k,Pth, lw=3, label=r'Theory $P(k)$')

errorbar(bins['ombins'],mean(pseudo_binned_Pk,axis=0),yerr=None,xerr=bins['xerr'],label=r'mean binned  $\tilde \mathcal{P}(k)$',ls='none',c='gray',lw=3,alpha=0.8)

errorbar(bins['ombins'],mean(unbiased_binned_Pk,axis=0),
         yerr=None, #std(unbiased_binned_Pk),
         xerr=bins['xerr'],
         label=r'mean debiased $\mathcal{P}^{obs}(k)$',ls='none',c='C2')

errorbar(bins['ombins'],-mean(unbiased_binned_Pk,axis=0),yerr=None,xerr=bins['xerr'],ls='none',c='C2',alpha=0.25)

loglog()
legend()

ylabel(r"Power")


subplot(312)
#plot(k,array(Wkwork['bpwf'][1,:]).flatten())
#plot(k,array(Wkwork['bpwf'][5,:]).flatten())
plot(k,array(Wkwork['bpwf'][4,:]).flatten(), label=r"$b=4$")
plot(k,array(Wkwork['bpwf'][7,:]).flatten(), label=r"$b=7$")
plot(k,array(Wkwork['bpwf'][10,:]).flatten(), label=r"$b=10$")

semilogx()
legend()
ylabel("Band-power window\n" r"function $\mathcal{W}_{bq}$")


subplot(313)
errorbar(bins['ombins'],
         mean(pseudo_binned_Pk,axis=0)/
         array(bins['B']*matrix(Pth.reshape(-1,1))).flatten(),
         yerr=None,
         xerr=bins['xerr'],
         ls='none', lw=3, c='gray', alpha=0.8,
         label=r'mean binned $\tilde \mathcal{P}/(BP)$')

'''
# binned pseudo power over binned mode-coupled theory
errorbar(bins['ombins'],
         mean(pseudo_binned_Pk,axis=0)/
         array(bins['B']*Wkwork['modecoupling']*matrix(Pth.reshape(-1,1))).flatten(),
         yerr=None,
         xerr=bins['xerr'],
         ls='none', lw=10, c='gray', alpha=0.2,
         label=r'mean binned $\tilde \mathcal{P}/(BWP)$')
'''

errorbar(bins['ombins'],
         mean(unbiased_binned_Pk,axis=0)/
         array(bins['B']*matrix(Pth.reshape(-1,1))).flatten(),
         yerr=None, # std(unbiased_binned_Pk,axis=0)/sqrt(Nreal),
         xerr=bins['xerr'],
         ls='none', c='C2',lw=5, alpha=0.3,
         label=r'mean debiased $\mathcal{P}^{\rm obs}/(BP)$')

errorbar(bins['ombins'],
         mean(unbiased_binned_Pk,axis=0)/
         array(Wkwork['bpwf']*matrix(Pth.reshape(-1,1))).flatten(),
         yerr=None, # std(unbiased_binned_Pk,axis=0)/sqrt(Nreal),
         xerr=bins['xerr'],
         ls='none', c='C2',
         label=r'mean debiased $\mathcal{P}^{\rm obs}/(\mathcal{W}P)$')

'''
# Binned theory over band-pass windowed theory
errorbar(bins['ombins'],
         array(bins['B']*matrix(Pth.reshape(-1,1))).flatten()/
         array(Wkwork['bpwf']*matrix(Pth.reshape(-1,1))).flatten(),
         yerr=None, # std(unbiased_binned_Pk,axis=0)/sqrt(Nreal),
         xerr=bins['xerr'],
         ls='none', c='C2',
         label=r'$BP/(\mathcal{W}P)$')
'''

axhline(1.0,c='gray',ls="-",lw=0.5)#,label='unbiased')
annotate('unbiased', xy=(0.2,1.03), color='gray',zorder=0)

xlabel(r"Wavenumber $k$ (Mpc$^{-1}$)")
ylabel(r"binned power ratio")

legend()

semilogx()


savefig('binned_Pk.pdf',bbox_inches='tight')
