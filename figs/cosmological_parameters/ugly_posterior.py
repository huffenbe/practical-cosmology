from pylab import *

from MH_simple import *

from nice_plot_posterior import *

from scipy.ndimage import gaussian_filter

with open("../plotstyle.py", "r") as f:
    exec(f.read())

close('all')




minx = -2
maxx = 2
miny = -2
maxy = 2
Ngrid = 1000

t = 45/180*pi

R = array([[cos(t), sin(t)],
          [-sin(t), cos(t)]])

x0,y0 = linspace(minx,maxx,Ngrid),linspace(miny,maxy,Ngrid)


X,Y = meshgrid(x0,y0)

cx = -0.811
cy = -0.591


Rad = ((X-cx)**2 + (Y-cy)**2)**0.5
Theta = atan2(Y-cy,X-cx)

x = stack([X,Y], axis=2)

C = [[ 2 , 0],
     [ 0 , .3]]

info2 = {}

info2['C'] = C
info2['detC'] = det(C)
info2['Cinv'] = inv(C)
info2['ndim'] = 2


Rx = tensordot(x,R,axes=[-1,0])
RTx = tensordot(x,R.T,axes=[-1,0])

#p = (targetnd(Rx - array([-2.,0]),info2) + targetnd(RTx - array([2.,0]),info2)) * target0(x[:,:,0],info2)**1

p  = exp(-(Rad-1)**2/2/0.2**2) * exp(-(Theta - pi/5)**2/2/(pi/4)**2)




nice_plot_p(p,X,Y,minx,maxx,miny,maxy,"posterior_curved.pdf")

### make polygon shaped


cx=0
cy=0

r1 = sqrt( (Rx[:,:,0] - cx)**2 + (Rx[:,:,1] - cy)**2)
t1 = arctan2( Rx[:,:,1]-cy,Rx[:,:,0] - cx)

t1[t1<0] += 2*pi

sides = 3

sector = floor(t1/(2*pi/sides))

sectort = (2*pi/sides)*(sector + 0.5)

sectnx = cos(sectort)
sectny = sin(sectort)

sectd = Rx[:,:,0]*sectnx + Rx[:,:,1]*sectny

p = exp(-sectd**2/2/0.4**2)
#p = exp(-sectd/2/0.1)

p = gaussian_filter(p,20)

#figure()
#imshow(t1)

#figure()
#imshow(sectort)

#figure()
#imshow(sectd)

#figure()
#imshow(p)



nice_plot_p(p,X,Y,minx,maxx,miny,maxy,"posterior_triangle.pdf")



p = targetnd(1.6*Rx,info2)

nice_plot_p(p,X,Y,minx,maxx,miny,maxy,"posterior_gaussian.pdf")

