from pylab import *
import scipy.stats

seed(76)

close('all')

def like(x) :
    return(  scipy.stats.norm.pdf(x) )



N = 1000

Nsteps = 8000

Xtrue = zeros(Nsteps)
X = zeros(Nsteps)
w = zeros(Nsteps)

Z = 0

Thetachain = zeros(Nsteps)
Lchain = zeros(Nsteps)

Thetarange = 20

Theta = scipy.stats.uniform.rvs(-Thetarange/2,Thetarange,N)
Xtrue[0] = 1
X[0] = 1

L = like(Theta)

for i in range(Nsteps):


    iLmin = argmin(L)

    if (i>0) : 
        Xtrue[i] = (amax(Theta) - amin(Theta))/Thetarange
        X[i] = exp(-i/N)
        w[i] = X[i-1] - X[i]
        Z += w[i] * L[iLmin]

    Thetachain[i] = Theta[iLmin]
    Lchain[i] = L[iLmin]

    Thetaprune = Theta[iLmin != arange(N)]
    Thetaprunemin = amin(Thetaprune)
    Thetaprunerange = amax(Thetaprune) - Thetaprunemin

    print(Thetaprunerange)
    
    Theta[iLmin] = scipy.stats.uniform.rvs(Thetaprunemin,Thetaprunerange)
    L[iLmin] = like(Theta[iLmin])


H = sum(w * log(Lchain/Z))


figure()
plot(Thetachain,Lchain)
