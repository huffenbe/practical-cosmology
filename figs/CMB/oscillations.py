from pylab import *

with open("../plotstyle.py", "r") as f:
    exec(f.read())


close('all')

x0 = linspace(0,10,100)
t0 = linspace(0,10,800)

Nosc = 4

k = zeros(Nosc)
w = zeros(Nosc)

t,x = meshgrid(t0,x0)

d = zeros([Nosc,len(x0),len(t0)])

k0 = 2*pi / 10
w0 = 2*pi / 40

k[0] = 2 * k0
w[0] = w0 

k[1] = 4 * k0
w[1] = w0 * 2

k[2] = 6 * k0
w[2] = w0*3

k[3] = 10 * k0
w[3] = w0 * 11

fig = figure(1,figsize=[8,4.5])


gs = fig.add_gridspec(Nosc,1, wspace=0.05, hspace=0.02)

for i in range(Nosc):
    d[i] = sin(k[i]*x)*sin(w[i]*t)

    #subplot(Nosc * 100 + 10 + i+1)
    ax = fig.add_subplot(gs[i])
    ax.imshow(d[i],cmap='gray',extent=[0,1,0,1/8])

    ax.tick_params(
        axis='both',       # changes apply to both x and y axes
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        left=False,        # ticks along the left edge are off
        right=False,       # ticks along the right edge are off
        labelbottom=False, # labels along the bottom edge are off
        labelleft=False    # labels along the left edge are off
    )

    if i == 0:
        ax.set_ylabel("lower $k$", rotation=0, ha='right')
    if i == Nosc -1 :
        ax.set_ylabel("higher $k$", rotation=0, ha='right')
        ax.tick_params(
            axis='x',
            bottom=True,
            labelbottom=True
        )
    
fig.supylabel(r"comoving $x$")
fig.supxlabel(r'time $t/t_{\rm CMB}$')



show()

savefig("oscillations.pdf",bbox_inches='tight')
