#This takes the output ptc_twiss and transform the eigenvalues into a V matrix.
# knowing that the beam matrix is described as sig=VeVT

import numpy as np
import matplotlib.pyplot as plt
import os
import shutil

def write_to_file(x, y,filename):
    fileobj= open(filename,'a')
    print >> fileobj, 'x', ' ', 'z'
    for key, value in zip(x,y):
        print >> fileobj, key,value
    fileobj.close()

def read_eigen_vecs(input_file):
    ev,betx,bety,_s=[],[],[],[]
    with open(input_file) as f:
        data = f.read()
    data=data.split('\n')
    for row in data:
        if row.startswith('@') or row.startswith('*') \
            or row.startswith('$') or len(row)==0:continue
        else:
            w=" ".join(row.split())
            s=w.split()
            row.lstrip()
            _s.append(s[-5])
            if s[0]=='"OSC_IOTA$START"':
                for i in range(len(s)-1): #make sure only reading in 36 values
                    ev.append(s[i+1])
    print len(ev)
    return ev

def get_cov(dataset,ex,ey,ez):
    emat=np.matrix([[ex,0,0,0,0,0],[0,ex,0,0,0,0],[0,0,ey,0,0,0],\
        [0,0,0,ey,0,0],[0,0,0,0,ez,0],[0,0,0,0,0,ez]])
    evs=read_eigen_vecs(dataset)
    #einv=emat.I
    ev1=map(float,evs)
    ev2=np.asarray(ev1)
    v=(ev2.reshape(6,6))
    vt=v.transpose()
    mat=v*vt
    print "v*vt"; see(mat)
    a=emat*vt #beam=[V][e][V]T
    b=v*a
    print "v*e*vt"; see(b)
    #c=v*einv;d=c*a;see(d)
    return b

def see(matrix):
    np.set_printoptions(precision=3)
    print matrix

def clear_all():
    for pr in range(33):
        directory='particle'+str(pr)
        if os.path.exists(directory)==True:
            shutil.rmtree(directory)

def make_beam(beam):

    xb=beam[0];pxb=beam[1]
    yb=beam[2];pyb=beam[3]
    tb=beam[4];ptb=beam[5]

    for i in range(len(xb)):
        x=xb[i];px=pxb[i]
        y=yb[i];py=pyb[i]
        t=tb[i];pt=ptb[i]
        directory='particle'+str(i)

        for j in range(len(x)):

            zeros.append(0); w.append(1)
            start.append('ptc_start,'); scom.append(';')
            sx.append('x='); sy.append(', y='); st.append(', t=')
            spx.append(', px='); spy.append(', py='); spt.append(', pt=')

        if not os.path.exists(directory):
            os.makedirs(directory)
        #shutil.copyfile('cool.run', directory+'/cool.run')
        shutil.copyfile('iota9.madx', directory+'/iota9.madx')
        shutil.copyfile('cool.kick', directory+'/cool.kick')

        #write cool.run

        with open('particle'+str(i)+'/input.beam'+str(i),'w') as g:
                for g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14 \
                    in zip(start, sx, x, spx, px, sy, y, spy, py, st, t, spt, pt, scom):
                    print >> g, g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14

    for proc in range(processors):
        for part in range(group):
            #write individual tracks from input_beam
            with open('particle'+str(proc)+'/input.beam'+str(proc),'r') as f:
                line = f.readlines()[part]
                with open('particle'+str(proc)+'/cooltrack'+str(part),'w') as f1:
                    f1.writelines(line)

def chunk(l,n):
    if n < 1:
        n = 1
    return [l[i:i + n] for i in range(0, len(l), n)]

##########################################################################
#######################   CREATE BEAM   ##################################
##########################################################################



etot=3.98e-9
emx=etot/2
emy=emx
sigt=0.197236030163993
sige=1.120662937626496e-4
emz=sige*sigt

processors=4
group=33
nparts=processors*group
V=get_cov('../cooling/ptc_track',ex=emx,ey=emy,ez=emz)

#print "items",V.item(0),V.item(1),V.item(6),V.item(7)
points=np.random.multivariate_normal\
        ([0,0],[[V.item(0),V.item(1)],[V.item(6),V.item(7)]],nparts)

x,px,y,py,t,pt = np.random.multivariate_normal([0,0,0,0,0,0],V,nparts).T

zeros,w,start,scom=[],[],[],[]
sx,sy,st,spx,spy,spt=[],[],[],[],[],[]

z=[x,px,y,py,t,pt]

xb=  chunk(z[0],group);pxb= chunk(z[1],group)
yb=  chunk(z[2],group);pyb= chunk(z[3],group)
tb=  chunk(z[4],group);ptb= chunk(z[5],group)

b=[xb,pxb,yb,pyb,tb,ptb]
print len(b),len(b[0]),len(b[0][0])
clear_all()
make_beam(b)

"""plt.subplot(3,1,1)
plt.plot(x,pt,'x')
plt.subplot(3,1,2)
plt.plot(t,px,'*')
plt.subplot(3,1,3)
plt.plot(px,pt,'.')
plt.show()
"""
e= open('emittances.txt','w')
e.write(str(emx)+'\n'+str(emy)+'\n'+str(emz))

print "x", np.std(x),'\n',"px", np.std(px),'\n',"y",np.std(y),'\n',"py", np.std(py),\
    '\n',"t", np.std(t),'\n',"pt", np.std(pt)
print "created input beams"