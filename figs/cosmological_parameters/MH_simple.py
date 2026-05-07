from pylab import *
import scipy.stats

def target0(x,info):
    return( scipy.stats.norm.pdf(x) )

def target1(x,info):
    return( 5/6*scipy.stats.norm.pdf(x-3) + 1/6*scipy.stats.norm.pdf(x+3) )


def targetnd(x,info) :
    Cinv = info['Cinv']
    detC = info['detC']
    ndim = info['ndim']

    Cinvx = tensordot(x,Cinv,axes=[-1,0])
    xCinvx = sum( x * Cinvx, axis=-1)
    
    return( exp(-xCinvx/2)/(2*pi*detC)**(ndim/2)  )
    


def symm_proposal_rv(info) :
    return(  scipy.stats.norm.rvs(scale=info["scale"]) )

def symm_proposal_nd_rv(info) :
    return(  scipy.stats.norm.rvs(scale=info["scale"],size=info["ndim"]) )

def MHsteps(x0, target, symm_proposal_rv, steps, info):

    xold = x0
    pold = target(xold,info)

    if (type(x0) == float64) :
        x = zeros(steps)
    else :
        x = zeros([steps,len(x0)])
    p = zeros(steps)
    Aavg = 0
    
    for i in range(steps) :
        xnew = xold + symm_proposal_rv(info)

        pnew = target(xnew,info)

        A = amin([1,pnew/pold])

        u = scipy.stats.uniform.rvs()

        if (u <= A) :  # accept
            x[i] = xnew
            p[i] = pnew
            xold = xnew
            pold = pnew
            Aavg += 1
        else :     # reject
            x[i] = xold
            p[i] = pold

    Aavg /= steps
    return(x,p,Aavg)
