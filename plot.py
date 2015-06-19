import scipy as sp
import pylab as py
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt,pi
import scipy.special as special
from scipy import stats
from scipy.stats import norm
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

def read_file(datafile,name):

    with open(datafile) as f:
        data = f.read()
    data=data.split('\n')
    n=0;i=0
    x=[];px=[];y=[];py=[];t=[];pt=[];
    for row in data:
        if row.startswith('@') or row.startswith('*') \
            or row.startswith('$') or row.startswith('#')\
            or len(row)==0: continue
        else:
            i+=1
            w=" ".join(row.split())
            s=w.split()
            x.append(float(s[2]))
            px.append(float(s[3]))
            y.append(float(s[4]))
            py.append(float(s[5]))
            t.append(float(s[6]))
            pt.append(float(s[7]))
    do_plot(x,px,y,py,t,pt,name)
    return x,px,y,py,t,pt


def do_plot(x,px,y,py,t,pt,name):
    i=1
    fig=plt.gcf()
    fig.set_size_inches(30,10)
    #print x,'\n',px
    #divs=np.array([1e-4 for i in range(100000)])
    #ns=np.array([i for i in range(100000)])
    #alphamap=np.array([a*b for a, b in zip(ns,divs)])

    #a=np.array(x,px)
    plt.subplot(1,3,1)
    plt.plot(x,px,'.',markersize=1)
    plt.subplot(1,3,2)
    plt.plot(y,py,'.',markersize=1)
    plt.subplot(1,3,3)
    plt.plot(t,pt,'.',markersize=1)
    plt.tight_layout()
    plt.savefig(name)

#_s,_betx,_alfx,_gamx =  get_m56.get_values('ptc_abc')

beam0=read_file('trackone',"synch.png")
print "beam file", len(beam0)

#x=[];px=[];y=[];py=[];t=[];pt=[];

#beam1=read_file('synchtrackone',"synch.png")
#print "beam file", len(beam1)


#test_plot_bunch_lengths(beam0,beam1_5,beam2_5)
#plot_bunch_lengths(beam0,beam1_5,beam2_5)

#s,m51,m52,m56,m56p   =  get_m56.get_M5s(_s,_M51,_M52,_M56)
#sigE,sigP,tot_ds,m56label     =  get_m56.get_bunch_lengths(_betx,_alfx,_gamx,_M51,_M52,_M56,ex=1.22e-8,sigP=0.000123)
#print m56label
######READ IN TRACKONE FROM MADX BYPASS OUTPUT######
#plot_bunch_lengths(beam,plot_of='diff',s=s,dl=tot_ds,mlabel=m56label)