import scipy as sp
from pylab import *
import get_m56
import labeling
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt,pi
#import scipy.special as special
#from scipy import stats
#from scipy.stats import norm
#from scipy.optimize import curve_fit

def read_file(datafile,nparts,obsv):
    l,z=[],[]
    for o in range(obsv):
        l.append([])
        print len(l)
    with open(datafile) as f:
        data = f.read()
    data=data.split('\n')
    print "data length:", (len(data))
    n=0
    i=0

    nobs = (len(data)-8)/nparts
    print '#obs:', nobs
    for row in data:
        if row.startswith('@') or row.startswith('*') \
            or row.startswith('$') or row.startswith('#')\
            or len(row)==0: continue
        else:
            i+=1
            w=" ".join(row.split())
            s=w.split()
            l[n].append(float(s[6]))
            if i%nparts==0:
                z.append(float(s[8]))
                i=0
                n+=1
    print z,'\n',len(l)
    return l,z

def plot_bunch_lengths(input,plot_of,t511,t512,t516,t522,t526,t566):

    lengths=input[0]
    z=input[1]
    fig=plt.gcf()
    fig.set_size_inches(30,20)
    sqr=1
    for m in (0,2,4,6,8,9):
        diff=[i-j for i, j in zip(lengths[m], lengths[0])]
        histo=diff
        label=['start','BEND1','BEND2','BEND3','BEND4','end']
        plt.subplot(3,3,sqr)

        if plot_of=='real':
            histo=lengths[m]
            rms=get_rms(lengths[m])
        else:
            cut='no'
            if m==8 or m==9:
                cut='yes'
            xmin,rms=get_rms(bunch=diff,cut=cut)
            #print "length of rms return", len(get_rms(bunch=diff,cut=cut))
            #if m==8 or m==9:
            #    plt.xlim(-1e-6,1e-6)
            #    plt.axvline(xmin)

        plt.hist(histo, histtype='step', bins=100, facecolor='blue')
        plt.xlabel('z (m)', fontsize=20)
        plt.ylabel('')
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0),fontsize=20)
        plt.xticks(fontsize=20)
        plt.title(label[sqr-1]+'  '+'RMS = '+str(rms),fontsize=20)
        plt.rc('font', **{'size':'20'})
        sqr+=1
        print m,sqr

    ######plot simgas versus z######
    real_rms=[]
    diff_rms=[]

    for k in range(len(lengths)):
        diff=[a-b for a, b in zip(lengths[k], lengths[0])]
        histo=diff
        x,rms=get_rms(histo,cut='yes')
        diff_rms.append(rms)
        if plot_of=='real':
            histo=lengths[k]
            x,rms=get_rms(bunch=lengths[k],cut='yes')
            real_rms.append(rms)

    del z[10:]          #ONLY WANT THE BYPASS, NOT THE END OF THE RING
    del real_rms[10:]
    del diff_rms[10:]


    plt.subplot(3,1,3)

    if histo==diff:
        plt.plot(z,diff_rms,'-o')

        #plt.plot(s,dl,'-',color='r')
    else:
        plt.plot(z,real_rms,'-o')
    plt.title('RMS VS. Z')
    plt.xlabel('position in bypass (m)',fontsize=20)
    plt.ylabel('bunch length sigma (m)', fontsize=20)
    plt.tight_layout()
    labeling.get_label()
    plt.savefig(plot_of + '_' + labeling.get_label())
    print "created: ", plot_of,labeling.get_label()


    #plt.plot(s,t511)
    #plt.plot(s,t512)
    #plt.semilogy(s,t516)
    #plt.plot(s,t522)

    #plt.semilogy(s,t526)
    #plt.semilogy(s,t566)
    #plt.savefig('tvalues'+labeling.get_label()+'.jpeg')
#def plot_gauss(histo):
#    hist,bin_edges=np.histogram(histo,bins=20)
#    print hist.size
#    bin_centers=(bin_edges[:-1]+bin_edges[1:])/2
#    p0=[1.,0.,1.]
#    coeff,var_matrix=curve_fit(fit_gauss,bin_centers,hist,p0=p0)
#    print 'Fitted mean = ', coeff[1]
#    print 'Fitted standard deviation = ', coeff[2]

#    hist_fit=fit_gauss(bin_centers,*coeff)
#    plt.plot(bin_centers,hist)
#    plt.plot(bin_centers,hist_fit,label='fit')

#def fit_gauss(x,*p):
#    A,mu,sigma=p
#    return A*np.exp(-(x-mu)**2/2.*sigma**2)

#def plot_gauss2(histo):
#    sigma=2.5
#    count, bins, ignored = plt.hist(histo, 30, normed=True)
#    plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi))*\
#                   np.exp( - (bins - mu)**2 / (2 * sigma**2) ),linewidth=2, color='r')
def get_rms(bunch,cut):
    xmin='None'
    if cut=='yes':
        bunch=apply_cut(bunch)
    square=[i ** 2 for i in bunch]
    rms=np.sqrt(np.mean(square))
    #rms=np.std(bunch)
    return xmin, rms

def apply_cut(bunch):
    STDEV=std(bunch)
    trunc_bunch = [x for x in bunch if abs(x) <= 3*STDEV]
    return trunc_bunch

_s,_betx,_alfx,_gamx =  get_m56.get_values('ptc_abc')
_s,_M51,_M52,_M56    =  get_m56.get_values('ptc_rmatrix')

s,m51,m52,m56,m56p   =  get_m56.get_M5s(_s,_M51,_M52,_M56)
t11,t12,t16,t22,t26,t56=get_m56.get_t_values('ptc_tmatrix')
print "TTTT!!!!!!!!",t11
#sigE,sigP,tot_ds,m56label     =  get_m56.get_bunch_lengths(_betx,_alfx,_gamx,_M51,_M52,_M56,ex=1.22e-8,sigP=0.000123)
#print m56label
######READ IN TRACKONE FROM MADX BYPASS OUTPUT######
n_obsv=11
beam=read_file('../beam99', nparts=10000,obsv=n_obsv)
plot_bunch_lengths(beam,plot_of='diff',t511=t11,t512=t12,t516=t16,t522=t22,t526=t26,t566=t56)