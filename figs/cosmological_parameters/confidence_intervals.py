from pylab import *
import matplotlib.gridspec as gridspec

with open("../plotstyle.py", "r") as f:
    exec(f.read())

close('all')



x = linspace(0,5,701)

pv = linspace(0.007,0.999,1000)

fig = figure(1,figsize=[10,4])
gs = gridspec.GridSpec(1, 4, figure=fig, wspace=0.05)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1],sharex=ax1,sharey=ax1)
ax3 = fig.add_subplot(gs[0, 3],sharex=ax1,sharey=ax1)
ax4 = fig.add_subplot(gs[0, 2],sharex=ax1,sharey=ax1)

setp(ax2.get_yticklabels(), visible=False)
setp(ax3.get_yticklabels(), visible=False)
setp(ax4.get_yticklabels(), visible=False)

p1 = exp(-(x-2.5)**2/2/0.7**2)
ax1.plot(x,p1)
ax1.set_xlim(0,amax(x))
ax1.set_ylim(0,1.01)
ax1.set_xlabel(r"Parameter $\Theta$")
ax1.set_ylabel(r"$p(\Theta)/(\text{max}\ p(\Theta))$")



c1 = cumsum(p1)/sum(p1)

Pv = zeros(len(pv))
cross = zeros([len(pv),2],dtype=int)

for i,pv0 in enumerate(pv):
    cross[i] = where(diff(sign(p1 - pv0)))[0]
    Pv[i] = c1[cross[i,1]] - c1[cross[i,0]]

interval68 = argmin( (Pv - 0.68)**2)
interval95 = argmin( (Pv - 0.95)**2)

ax1.axhline(pv[interval68],label="68% interval",color='black',linestyle=":")
ax1.axhline(pv[interval95],label="95% interval",color='gray',linestyle=":")

ax1.fill_between( x[cross[interval68,0]:cross[interval68,1]], p1[cross[interval68,0]:cross[interval68,1]],color='blue',alpha=0.5)

ax1.fill_between( x[cross[interval95,0]:cross[interval95,1]], p1[cross[interval95,0]:cross[interval95,1]],color='blue', alpha=0.5)




p2 = exp(-(log(x) - log(1.0))**2/2/0.5**2)
ax2.plot(x,p2)
ax2.set_xlim(0,amax(x))


c2 = cumsum(p2)/sum(p2)

Pv = zeros(len(pv))
cross = zeros([len(pv),2],dtype=int)

for i,pv0 in enumerate(pv):
    cross[i] = where(diff(sign(p2 - pv0)))[0]
    Pv[i] = c2[cross[i,1]] - c2[cross[i,0]]

interval68 = argmin( (Pv - 0.68)**2)
interval95 = argmin( (Pv - 0.95)**2)

ax2.axhline(pv[interval68],label="68% interval",color='black',linestyle=":")
ax2.axhline(pv[interval95],label="95% interval",color='gray',linestyle=":")

ax2.fill_between( x[cross[interval68,0]:cross[interval68,1]], p2[cross[interval68,0]:cross[interval68,1]],color='blue',alpha=0.5)

ax2.fill_between( x[cross[interval95,0]:cross[interval95,1]], p2[cross[interval95,0]:cross[interval95,1]],color='blue', alpha=0.5)




p3 = exp(-x/1.0)
ax3.plot(x,p3)
ax3.set_xlim(0,amax(x))


c3 = cumsum(p3)/sum(p3)

Pv = zeros(len(pv))
cross = zeros([len(pv),1],dtype=int)

for i,pv0 in enumerate(pv):
    cross[i] = where(diff(sign(p3 - pv0)))[0][0]
    Pv[i] = c3[cross[i]]

interval68 = argmin( (Pv - 0.68)**2)
interval95 = argmin( (Pv - 0.95)**2)

ax3.axhline(pv[interval68],label="68%",color='black',linestyle=":")
ax3.axhline(pv[interval95],label="95%",color='gray',linestyle=":")

ax3.fill_between( x[0:cross[interval68][0]], p3[0:cross[interval68][0]],color='blue',alpha=0.5)
ax3.fill_between( x[0:cross[interval95][0]], p3[0:cross[interval95][0]],color='blue',alpha=0.5)

ax3.legend()

#fill_between( x[0:cross[interval95]], p2[cross[interval95,0]:cross[interval95,1]],color='blue', alpha=0.5)








p4 = exp(-(x-0.8)**2/2/0.7**2)
ax4.plot(x,p4)





c4 = cumsum(p4)/sum(p4)

Pv = zeros(len(pv))
cross = zeros([len(pv),2],dtype=int)

for i,pv0 in enumerate(pv):
    cross[i] = where(diff(sign(p4 - pv0)))[0]
    Pv[i] = c4[cross[i,1]] - c4[cross[i,0]]

interval68 = argmin( (Pv - 0.68)**2)
interval95 = argmin( (Pv - 0.95)**2)
xinterval95 = argmin( (c4 - 0.95)**2)

ax4.axhline(pv[interval68],label="68% interval",color='black',linestyle=":")
ax4.axhline(p4[xinterval95],label="95% interval",color='gray',linestyle=":")

ax4.fill_between( x[cross[interval68,0]:cross[interval68,1]], p4[cross[interval68,0]:cross[interval68,1]],color='blue',alpha=0.5)

ax4.fill_between( x[0:xinterval95], p4[0:xinterval95],color='blue', alpha=0.5)


savefig("confidence_intervals.pdf",bbox_inches='tight')










#gs.tight_layout(fig)











