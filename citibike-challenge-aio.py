import pylab as plt
import pandas as pd
import numpy as np
import datetime as dt
def datestr_as_datetime(dstr):
    #2014-01-27 12:28:45
    dstr=dstr.split()
    y,mo,day=dstr[0].split('-')
    hh,mm,ss=dstr[1].split(':')

    return dt.datetime(int(y),int(mo),int(day),int(hh),int(mm),int(ss))

cbs=pd.read_csv("./citibike-files/2013-07.csv")

pk=np.array( [datestr_as_datetime(st) for st in cbs.starttime])
hh=np.array( [float(st.split()[1].split(':')[0])+float(st.split()[1].split(':')[1])/60.0 for st in cbs.starttime])


fig=plt.figure(figsize=(15,10))

ax1 =plt.subplot2grid((2,2),(0,0),colspan=2)
ax1.set_title("Peak Hour for July 2013")
ax1.set_xlabel("Hour of the day")
ax1.set_ylabel("Number of People")
ax1.grid()
ax1.set_xticks(range(24))

n,bins,patches=ax1.hist([hh[np.array(cbs.gender)==1], hh[np.array(cbs.gender)==2],hh[np.array(cbs.gender)==0]], 24, stacked=True, label=['male','female','undetermined'], color=['LightSteelBlue','SteelBlue','MidnightBlue'])

n1,bins1=np.histogram(hh,24)
colors=['pink','yellow','green','orange','brown','purple']

plt.legend()

for i in range(6):
	ax1.bar(i*4,np.mean(n1[i*4:i*4+4]),width=4,alpha=0.5, color=colors[i])
        ax1.text(i*4+2, np.mean(n1[i*4:i*4+4])+400,'%d'%np.mean(n1[i*4:i*4+4]), ha="center")

ax1.plot(bins1[:-1]+0.5,n1,'r-')


n2,b2=np.histogram(cbs['gender'][cbs['gender']>0],2)
ax2 = plt.subplot2grid((2,2),(1,0),colspan=1)
ax2.set_title("Rides by Man vs Women")
ax2.set_ylabel("Number of People")
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off') # labels along the bottom edge are off
ax2.bar(np.array([1,2]),n2,width=0.5, color='SteelBlue')
ax2.text(0.3,0.5,'Male',transform=ax2.transAxes, ha='center')
ax2.text(0.3,0.3,'%d'%n2[0],transform=ax2.transAxes, ha='center')
ax2.text(0.7,0.5,'Female',transform=ax2.transAxes, ha='center')
ax2.text(0.7,0.3,'%d'%n2[1],transform=ax2.transAxes, ha='center')
ax2.grid()
ax2.xaxis.grid()
ax2.set_xlim((0.5,3))
ax2.set_ylim((0,max(n2)*1.5))


tur=cbs.usertype=='Customer'
nyc=cbs.usertype=='Subscriber'

ax3 = plt.subplot2grid((2,2),(1,1),colspan=1)
ax3.set_title("NewYorkers vs Tourists")
'''
tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off') # labels along the bottom edge are off



ax3.set_ylabel("Number of Customers")
ax3.bar(np.array([1,2]),[sum(nyc),sum(tur)],width=0.5, color='SteelBlue')
ax3.yaxis.grid()
ax3.text(0.3,0.5,'New Yorkers',transform=ax3.transAxes, ha='center')
ax3.text(0.3,0.3,'%d'%sum(nyc),transform=ax3.transAxes, ha='center')
ax3.text(0.7,0.5,'Tourists',transform=ax3.transAxes, ha='center')
ax3.text(0.7,0.3,'%d'%sum(tur),transform=ax3.transAxes, ha='center')
ax3.set_xlim((0.5,3))
ax3.set_ylim((0,max([sum(nyc),sum(tur)])*1.5))
'''

labels = 'New Yorkers\n(%d)'%sum(nyc), 'Tourists\n(%d)'%sum(nyc)
fracs = np.array([sum(nyc),sum(tur)])

ax3.pie(fracs,  labels=labels,
                autopct='%1.1f%%', shadow=True, startangle=0, colors=['SteelBlue','purple'])

ax3.axis('equal')
plt.show()
