from pylab import *

def nice_plot_p(p,X,Y,minx,maxx,miny,maxy,filename) :

    x0,y0 = linspace(minx,maxx,p.shape[1]),linspace(miny,maxy,p.shape[0])
    x = stack([X,Y], axis=2)

    
    fig, axs = plt.subplots(2, 2,figsize=[4,4],gridspec_kw={
        'width_ratios': [4, 1],
        'height_ratios': [1, 4] })

    fig.subplots_adjust(wspace=0, hspace=0)
    # Hide x-ticks for the top plot so they don't overlap the one below it
    axs[0, 0].set_xticklabels([])
    # Hide y-ticks for the bottom right plot so they don't overlap the one to the left
    axs[1, 1].set_yticklabels([])

    
    axs[1,0].contour(p,levels=linspace(0.0,amax(p),10),extent=[minx,maxx,miny,maxy],origin='lower',linewidths=1)


    p0 = sum(p,axis=0)
    p1 = sum(p,axis=1)

    p0 /= amax(p0)
    p1 /= amax(p1)

    xmargpeak = x0[argmax(p0)]
    ymargpeak = y0[argmax(p1)]

    xpeak = x[unravel_index(argmax(p),shape(p))]

    xmean = sum(X*p)/sum(p)
    ymean = sum(Y*p)/sum(p)


    axs[1,0].plot(xpeak[0],xpeak[1],'ko', ms=4,label="Posterior max.")
    axs[1,0].plot(xmean,ymean,'kx', ms=8, mfc='none',label="Posterior mean")

    axs[1,0].axhline(ymargpeak,ls=":",lw=0.7,label='Marginal peaks')
    axs[1,0].axvline(xmargpeak,ls=":",lw=0.7)

    axs[1,0].legend(loc='lower left')

    #figure()
    axs[0,0].plot(x0,p0)
    
    
    axs[0,0].set_xlim(minx,maxx)
    axs[0,0].set_ylim(0,1.1)
    axs[0,0].axvline(xmargpeak,ls=":",lw=0.7)

    axs[1,0].set_xlabel(r"parameter $\Theta_1$")
    axs[1,0].set_ylabel(r"parameter $\Theta_2$")
   
    axs[1,1].plot(p1,y0)
    axs[1,1].set_xlim(0,1.1)
    axs[1,1].set_ylim(miny,maxy)
    axs[1,1].axhline(ymargpeak,ls=":",lw=0.7)

    axs[0,1].set_visible(False)


    #tight_layout(pad=0)

    savefig(filename,bbox_inches='tight')

    return()
