from pylab import *
import scipy.stats

from MH_simple import *

close('all')




seed(12345)

info = {}

info['scale'] = 2.5

steps = 2000

Nchains = 3

x = zeros([Nchains,steps])
p = zeros([Nchains,steps])
Aavg = zeros(Nchains)


x0 = scipy.stats.norm.rvs(scale=9, size=Nchains)
x0[0] = 9.0

ymin=-8
ymax=8

print("just right")
for j in range(Nchains) :
    print("Chain",j)
    x[j],p[j],Aavg[j] = MHsteps(x0[j], target1, symm_proposal_rv, steps, info)

#figure(1)
#for j in range(3) :
#    plot(x[j], label="acceptance = %.2f" % (Aavg[j]), lw = 0.7, alpha=0.5)
#
#xlim(0,50)
#legend(loc='lower left')

fs = [10,2]
wr = [6,1]

slbl = "steps"
plbl = "parameter"

fig2, (ax_main, ax_hist) = plt.subplots(1, 2, sharey=True,figsize=fs, gridspec_kw={'width_ratios': wr})
for j in range(3):
        ax_main.plot(x[j], label="acceptance = %.2f" % (Aavg[j]), lw = 0.7, alpha=0.5)

#ax_main.set_xlim(50,steps)
ax_main.set_ylim(ymin,ymax)
ax_main.legend(loc='lower left')
ax_main.set_xlabel(slbl)
ax_main.set_ylabel(plbl)

ax_hist.hist(x[:,50:].flatten(),bins=50,orientation='horizontal',density=True)
tight_layout(pad=0)

xtest = linspace(ymin,ymax,100)
ax_hist.plot(target1(xtest,info),xtest)

savefig("MH_example_just_right.pdf",bbox_inches="tight")

print("too tight")
info['scale'] = 0.1
for j in range(Nchains) :
    print("Chain",j)
    x[j],p[j],Aavg[j] = MHsteps(x0[j], target1, symm_proposal_rv, steps, info)


fig3, (ax_main, ax_hist) = plt.subplots(1, 2, sharey=True,figsize=fs, gridspec_kw={'width_ratios': wr})
for j in range(3):
        ax_main.plot(x[j], label="acceptance = %.2f" % (Aavg[j]), lw = 0.7, alpha=0.5)

ax_main.set_ylim(ymin,ymax)
ax_main.set_xlabel(slbl)
ax_main.set_ylabel(plbl)

ax_main.legend(loc='lower left')
ax_hist.hist(x[:,50:].flatten(),bins=50,orientation='horizontal',density=True)
ax_hist.plot(target1(xtest,info),xtest)
tight_layout(pad=0)

savefig("MH_example_too_tight.pdf",bbox_inches="tight")


print("too loose")
info['scale'] = 50
for j in range(Nchains) :
    print("Chain",j)
    x[j],p[j],Aavg[j] = MHsteps(x0[j], target1, symm_proposal_rv, steps, info)


fig4, (ax_main, ax_hist) = plt.subplots(1, 2, sharey=True,figsize=fs, gridspec_kw={'width_ratios': wr})
for j in range(3):
        ax_main.plot(x[j], label="acceptance = %.2f" % (Aavg[j]), lw = 0.7, alpha=0.5)

ax_main.set_ylim(ymin,ymax)
ax_main.set_xlabel(slbl)
ax_main.set_ylabel(plbl)

ax_main.legend(loc='lower left')

ax_hist.hist(x[:,50:].flatten(),bins=50,orientation='horizontal',density=True)
ax_hist.plot(target1(xtest,info),xtest)
tight_layout(pad=0)


savefig("MH_example_too_loose.pdf",bbox_inches="tight")

# 2d case

#
# C  = [ a b ]
#      [ c d ]
#
# want detC = ad - bc = 1
#
# a = d 
# b = c
#
# C = [ a r ]
#     [ r a ]
# w/
# a^2 - 1 = r^2

ndim = 2

a = 4
r = sqrt(a**2 - 1)

C = array([[ a, r],[r,a]])


info2 = {}

info2['C'] = C
info2['detC'] = det(C)
info2['Cinv'] = inv(C)
info2['ndim'] = ndim


x20 = scipy.stats.norm.rvs(scale=4.0,size=Nchains*ndim).reshape([Nchains,ndim])

steps = 10000

x = zeros([Nchains,steps,ndim])
p = zeros([Nchains,steps])
Aavg = zeros(Nchains)


print("2d")
info2['scale'] = 0.9
for j in range(Nchains) :
    print("Chain",j)
    x[j],p[j],Aavg[j] = MHsteps(x20[j], targetnd, symm_proposal_nd_rv, steps, info2)


fig5, (ax_main, ax_hist, ax_2d) = plt.subplots(1, 3, sharey=True,figsize=fs, gridspec_kw={'width_ratios': [5,1,1]})
for j in range(3):
        ax_main.plot(x[j,:,0], label="acceptance = %.2f" % (Aavg[j]), lw = 0.7, alpha=0.5)

ax_main.set_ylim(ymin,ymax)
ax_main.set_xlabel(slbl)
ax_main.set_ylabel(r'parameter $\Theta_2$')

ax_main.legend(loc='lower left')

ax_hist.hist(x[:,50:,0].flatten(),bins=50,orientation='horizontal',density=True)
ax_hist.plot(scipy.stats.norm.pdf(xtest,scale=sqrt(a)),xtest)

for j in range(3):
    ax_2d.plot(x[j,:,1],x[j,:,0],lw=0.7,alpha=0.3)

ax_2d.set_xlim(ymin,ymax)
ax_2d.set_xlabel(r'parameter $\Theta_1$')

tight_layout(pad=0)

savefig("MH_example_2d.pdf",bbox_inches="tight")
