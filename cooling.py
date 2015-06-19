from subprocess import call, Popen, PIPE
from math import sin, pi
import time
import multiprocessing
import matplotlib.pyplot as plt
import numpy as np
import os

def get_coords(file,part,batch):

    with open(file) as f:

        data = f.read()
        data=data.split('\n')

        start= data[9]
        a=" ".join(start.split())
        l=a.split()
        x0=l[2];px0=l[3];y0=l[4];py0=l[5];t0=l[6];pt0=l[7]

        okick=data[11]
        b=" ".join(okick.split())
        m=b.split()
        x1=m[2];px1=m[3];y1=m[4];py1=m[5];t1=m[6];pt1=m[7]

        oend=data[13]
        c=" ".join(oend.split())
        n=c.split()
        x2=n[2];px2=n[3];y2=n[4];py2=n[5];t2=n[6];pt2=n[7]

        end=data[15]
        c=" ".join(end.split())
        n=c.split()
        x=n[2];px=n[3];y=n[4];py=n[5];t=n[6];pt=n[7]

    dz=float(t1)-float(t0)
    dE=-0.6*sin(dz*2*pi*0.05e6)

    return x0,px0,y0,py0,t0,pt0,x1,px1,y1,py1,t1,pt1,\
           x2,px2,y2,py2,t2,pt2,x,px,y,py,t,pt,dE,dz,part,batch

def update_track(x,px,y,py,t,pt,part,batch):

    file='particle'+str(batch)+"/cooltrack"+str(part)
    with open(file,'w') as p:
        p.write("ptc_start, x= "+str(x)+", px= "+str(px)+ \
        ", y= "+str(y)+", py="+str(py)+ \
        ", t= "+str(t)+", pt= "+str(pt)+";")

def write_kick(dE):

    file1='particle'+str(batch)+"/cool.kick"
    file2='particle'+str(batch)+"/iota9.madx"
    the_kick="lkick: RFCAVITY, L=0., VOLT="+str(dE)+", LAG=0, HARMON=4;"
    with open(file1,'w') as e:
        e.write(the_kick)

    with open(file2,'r') as f:
        lines=f.readlines()

    lines[3]="call,file=particle"+str(batch)+"/cool.kick;\n"

    with open(file2,'w') as g:
        g.writelines(lines)

def write_run_file(particle):
    file_string=file(particle)
    ntrack='cooltrack'+str(part)

    with open('particle'+str(batch)+'/cool.run','w') as o:
        #data=o.readlines()
        data=file_string
        o.writelines(data)

def sim_cool(cmd,batch,kick):
    _allt=[];_allpt=[];_alldE=[];_alldz=[]

    for particle in range(group):
        write_run_file(particle)

        for turn in range(300):
            print turn
            #Popen(cmd, shell=True,stdout=PIPE).stdout.read()
            devnull = open('/dev/null', 'w')
            #launch particle#
            seed=Popen(cmd, shell=True,stdout=PIPE)
            seed.wait()

            _xP,_pxP,_yP,_pyP,_tP,_ptP,_xK,_pxK,_yK,_pyK,_tK,_ptK,_xL,_pxL,_yL,_pyL,_tL,_ptL,\
            _x,_px,_y,_py,_t,_pt,_dE,_dz,_part,_batch=\
                get_coords('particle'+str(batch)+'/trackone',particle,batch)

            if kick=='yes':

                write_kick(_dE)
                time.sleep(0.1)#let file write

            if kick=='no':
            
                time.sleep(0.1)#let file write

            launch=Popen(cmd, shell=True, stdout=PIPE)#devnull)#,stdout=PIPE).stdout.read()
            launch.wait()

            xP_,pxP_,yP_,pyP_,tP_,ptP_,xK_,pxK_,yK_,pyK_,tK_,ptK_,xL_,pxL_,yL_,pyL_,tL_,ptL_,\
            x_,px_,y_,py_,t_,pt_,dE_,dz_,part_,batch_=\
               get_coords('particle'+str(batch)+'/trackone',particle,batch)

            update_track(x_,px_,y_,py_,t_,pt_,part_,batch_)
            #print tL_, ptL_,turn
            _allt.append(float(tL_))
            _allpt.append(float(ptL_))
            _alldz.append(float(dz_))
            _alldE.append(float(dE_))
            #print t_,pt_,part_,batch_
        plt.plot(_alldz,_alldE,'o',markersize=5,color='black')
        plt.savefig('dE_dz_'+str(batch)+'.png')
        plt.close()
            #plt.plot(tK_,ptK_,'x',markersize=5,color='r')

        colors=['r','b']
        plt.plot(_allt,_allpt,'x',markersize=5,color=colors[batch])
        plt.savefig('t_pt'+str(batch)+'.png')

def file(particle):

    file_string="OPTION, -ECHO;\n\
ptc_enforce6d, flag=true;\n\
call, file=particle"+str(batch)+"/cool.kick\n\
call, file=particle"+str(batch)+"/iota9.madx;\n\
beam, PARTICLE=electron,ENERGY=0.1005110034,radiate;\n\
use, period=osc_iota;\n\
select,flag=twiss,clear;\n\
select, flag=twiss, column=name, s, dx, dpx;\n\
twiss,chrom,file=twiss.values;\n\
PTC_CREATE_UNIVERSE;\n\
PTC_CREATE_LAYOUT,model=2,method=6,nst=1,exact;\n\
call,file=particle"+str(batch)+"/cooltrack"+str(particle)+";\n\
use,period=osc_iota;\n\
PTC_OBSERVE,place=oend;\n\
PTC_OBSERVE,place=okicker;\n\
PTC_TRACK,icase=6,onetable,dump,turns=1,radiation,file=particle"+str(batch)+"/track;\n\
PTC_TRACK_END;\n\
PTC_END;\n\
STOP;"

    return file_string

#######################################################
######################SIMULATION#######################
#######################################################

t0=time.time()
call("madx < eigen_gen.madx", shell=True)
call("python beamgen.py", shell=True)

processors=1
group=1
kickit='yes'
for batch in range(processors):

    num= "%s" %batch
    part= "cool"+num
    cmd= "madx < " +'particle'+num+"/cool.run"

    process = multiprocessing.Process(target=sim_cool,args=(cmd,batch,kickit))
    process.start()
    kickit='noq'
#process.join()

print "total time required (hr)"

#processes = [Popen([cmd, str(i)], shell=True) for i in range(1)]