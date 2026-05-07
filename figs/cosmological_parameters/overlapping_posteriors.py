from pylab import *

from MH_simple import *

from nice_plot_posterior import *

with open("../plotstyle.py", "r") as f:
    exec(f.read())


close('all')


minx = -2
maxx = 2
miny = -2
maxy = 2
Ngrid = 1000

ta = 45/180*pi

Ra = array([[cos(ta), sin(ta)],
          [-sin(ta), cos(ta)]])

x0,y0 = linspace(minx,maxx,Ngrid),linspace(miny,maxy,Ngrid)
X,Y = meshgrid(x0,y0)

x = stack([X,Y], axis=2)


Rax = tensordot(x-[-0.5,0],Ra,axes=[-1,0])

Ca = [[ 3 , 0],
     [ 0 , .1]]

info2 = {}

info2['C'] = Ca
info2['detC'] = det(Ca)
info2['Cinv'] = inv(Ca)
info2['ndim'] = 2

pa = targetnd(Rax - [0,0],info2)

tb = 120/180*pi

Rb = array([[cos(tb), sin(tb)],
          [-sin(tb), cos(tb)]])


Cb = [[ 2, 0 ],
      [ 0.0, 0.2] ]

infob = {}

infob['C'] = Cb
infob['detC'] = det(Cb)
infob['Cinv'] = inv(Cb)
infob['ndim'] = 2

Rbx = tensordot(x-[0.1,-0.5],Rb,axes=[-1,0])

pb = targetnd(Rbx,infob)

pc = pa*pb


fig, axs = plt.subplots(2, 2,figsize=[4,4],gridspec_kw={
    'width_ratios': [4, 1],
    'height_ratios': [1, 4] })

fig.subplots_adjust(wspace=0, hspace=0)
# Hide x-ticks for the top plot so they don't overlap the one below it
axs[0, 0].set_xticklabels([])
# Hide y-ticks for the bottom right plot so they don't overlap the one to the left
axs[1, 1].set_yticklabels([])

Ncont = 4

axs[1,0].contour(pa,levels=linspace(0.0,amax(pa),Ncont),extent=[minx,maxx,miny,maxy],origin='lower',cmap="Reds",linewidths=1)
axs[1,0].contour(pb,levels=linspace(0.0,amax(pb),Ncont),extent=[minx,maxx,miny,maxy],origin='lower',cmap="Blues",linewidths=1)
axs[1,0].contour(pc,levels=linspace(0.0,amax(pc),Ncont),extent=[minx,maxx,miny,maxy],origin='lower',cmap="Purples",linewidths=1)


pa0 = sum(pa,axis=0)
pa1 = sum(pa,axis=1)
pa0 /= amax(pa0)
pa1 /= amax(pa1)

pb0 = sum(pb,axis=0)
pb1 = sum(pb,axis=1)
pb0 /= amax(pb0)
pb1 /= amax(pb1)

pc0 = sum(pc,axis=0)
pc1 = sum(pc,axis=1)
pc0 /= amax(pc0)
pc1 /= amax(pc1)



xamargpeak = x0[argmax(pa0)]
yamargpeak = y0[argmax(pa1)]

xapeak = x[unravel_index(argmax(pa),shape(pa))]

xamean = sum(X*pa)/sum(pa)
yamean = sum(Y*pa)/sum(pa)


#axs[1,0].plot(xapeak[0],xapeak[1],'ko', ms=4,label="Posterior max.")
#axs[1,0].plot(xamean,yamean,'kx', ms=8, mfc='none',label="Posterior mean")

#axs[1,0].axhline(yamargpeak,ls=":",lw=0.7,label='Marginal peaks')
#axs[1,0].axvline(xamargpeak,ls=":",lw=0.7)

#axs[1,0].legend(loc='lower left')

#figure()
axs[0,0].plot(x0,pa0,c='red')
axs[0,0].plot(x0,pb0,c='blue')
axs[0,0].plot(x0,pc0,c='purple')


axs[0,0].set_xlim(minx,maxx)
axs[0,0].set_ylim(0,1.1)
#axs[0,0].axvline(xamargpeak,ls=":",lw=0.7)

axs[1,0].set_xlabel(r"parameter $\Theta_1$")
axs[1,0].set_ylabel(r"parameter $\Theta_2$")

axs[1,1].plot(pa1,y0,c='red')
axs[1,1].plot(pb1,y0,c='blue')
axs[1,1].plot(pc1,y0,c='purple')


axs[1,1].set_xlim(0,1.1)
axs[1,1].set_ylim(miny,maxy)
#axs[1,1].axhline(yamargpeak,ls=":",lw=0.7)

axs[0,1].set_visible(False)


#tight_layout(pad=0)

savefig("overlapping_posteriors_1.pdf",bbox_inches='tight')

#################################################
#################################################
##
##
##  Second Figure
##
##
#################################################
#################################################

Rdx = tensordot(x-[-1.5,0.5],Ra,axes=[-1,0])

Cd = [[ 0.5 , 0],
     [ 0 , .1]]

infod = {}

infod['C'] = Cd
infod['detC'] = det(Cd)
infod['Cinv'] = inv(Cd)
infod['ndim'] = 2

pd = targetnd(Rdx - [0,0],infod)

te = 120/180*pi

Re = array([[cos(te), sin(te)],
          [-sin(te), cos(te)]])


Ce = [[ 0.5, 0 ],
      [ 0.0, 0.2] ]

infoe = {}

infoe['C'] = Ce
infoe['detC'] = det(Ce)
infoe['Cinv'] = inv(Ce)
infoe['ndim'] = 2

Rex = tensordot(x-[1.8,1.5],Re,axes=[-1,0])

pe = targetnd(Rex,infob)

pf = pd*pe



fig, axs = plt.subplots(2, 2,figsize=[4,4],gridspec_kw={
    'width_ratios': [4, 1],
    'height_ratios': [1, 4] })


fig.subplots_adjust(wspace=0, hspace=0)
# Hide x-ticks for the top plot so they don't overlap the one below it
axs[0, 0].set_xticklabels([])
# Hide y-ticks for the bottom right plot so they don't overlap the one to the left
axs[1, 1].set_yticklabels([])



axs[1,0].contour(pd,levels=linspace(0.0,amax(pd),Ncont),extent=[minx,maxx,miny,maxy],origin='lower',cmap="Reds",linewidths=1)
axs[1,0].contour(pe,levels=linspace(0.0,amax(pe),Ncont),extent=[minx,maxx,miny,maxy],origin='lower',cmap="Blues",linewidths=1)
axs[1,0].contour(pf,levels=linspace(0.0,amax(pf),Ncont),extent=[minx,maxx,miny,maxy],origin='lower',cmap="Purples",linewidths=1)


pd0 = sum(pd,axis=0)
pd1 = sum(pd,axis=1)
pd0 /= amax(pd0)
pd1 /= amax(pd1)

pe0 = sum(pe,axis=0)
pe1 = sum(pe,axis=1)
pe0 /= amax(pe0)
pe1 /= amax(pe1)

pf0 = sum(pf,axis=0)
pf1 = sum(pf,axis=1)
pf0 /= amax(pf0)
pf1 /= amax(pf1)



xamargpeak = x0[argmax(pa0)]
yamargpeak = y0[argmax(pa1)]

xapeak = x[unravel_index(argmax(pa),shape(pa))]

xamean = sum(X*pa)/sum(pa)
yamean = sum(Y*pa)/sum(pa)


#axs[1,0].plot(xapeak[0],xapeak[1],'ko', ms=4,label="Posterior max.")
#axs[1,0].plot(xamean,yamean,'kx', ms=8, mfc='none',label="Posterior mean")

#axs[1,0].axhline(yamargpeak,ls=":",lw=0.7,label='Marginal peaks')
#axs[1,0].axvline(xamargpeak,ls=":",lw=0.7)

#axs[1,0].legend(loc='lower left')

#figure()
axs[0,0].plot(x0,pd0,c='red')
axs[0,0].plot(x0,pe0,c='blue')
axs[0,0].plot(x0,pf0,c='purple')


axs[0,0].set_xlim(minx,maxx)
axs[0,0].set_ylim(0,1.1)
#axs[0,0].axvline(xamargpeak,ls=":",lw=0.7)

axs[1,0].set_xlabel(r"parameter $\Theta_1$")
axs[1,0].set_ylabel(r"parameter $\Theta_2$")

axs[1,1].plot(pd1,y0,c='red')
axs[1,1].plot(pe1,y0,c='blue')
axs[1,1].plot(pf1,y0,c='purple')


axs[1,1].set_xlim(0,1.1)
axs[1,1].set_ylim(miny,maxy)
#axs[1,1].axhline(yamargpeak,ls=":",lw=0.7)

axs[0,1].set_visible(False)


#tight_layout(pad=0)
savefig("overlapping_posteriors_2.pdf",bbox_inches='tight')
