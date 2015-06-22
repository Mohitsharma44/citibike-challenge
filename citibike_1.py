import numpy as np
from datetime import datetime, timedelta
from sys import argv
import matplotlib.pyplot as plt

class CitiBikeChallenge():
    def __init__(self):
        pass

    def load_file(self, path):
        print 'Loading data ... '
        self.data = np.genfromtxt(path, dtype=None, 
                             delimiter=',', skip_header=True)
        return self.data
    
    def gender(self, data):
        print 'Detecting gender Distribution...'
        self.males = np.zeros(data.shape[0])
        self.females = np.zeros(data.shape[0])
        self.unknown = np.zeros(data.shape[0])

        self.males = np.char.strip(data[0:, 14], 
                                   '"').astype(np.float) == 1
        self.females = np.char.strip(data[0:, 14],
                                     '"').astype(np.float) == 2
        self.unknown = np.char.strip(data[:,14], 
                                     '"').astype(np.float) == 0

        return(self.males.astype(int), self.females.astype(int), 
               self.unknown.astype(int))

    def avg_ride_time(self, data):
        print 'Calculating average ride time ...'
        def _calc_time(data):
            return datetime.strptime(str(np.char.strip(data,
                                                       '"')), 
                                     '%Y-%m-%d %H:%M:%S')
        # Vectorize method
        v_calc_time = np.vectorize(_calc_time)
        self.start = v_calc_time(data[:,1])
        self.stop = v_calc_time(data[:,2])

        # Take Average
        self.diff = np.subtract(self.stop, self.start)
        return (np.sum(self.diff)/self.start.shape[0], self.start, 
                self.stop, self.diff)
        
    def peak_hours(self, start_time):
        self.idx = np.zeros([24, start_time.shape[0]])
        print 'Calculating peak hours ...'
        def _check(start_time, _cond):
            # Classify rides into hours
            if start_time.hour == _cond.total_seconds()/3600:                
                return 1
            else:
                return 0
        # Vectorize method
        vcheck = np.vectorize(_check)
        for i in xrange(24):
            _cond = timedelta(hours = i)
            self.idx[i] = vcheck(start_time, 
                                 _cond)#.nonzero()[0].shape[0]
        return self.idx

    def tourists(self, data):
        print 'Detecting tourists ...'
        self.tourists = np.char.strip(data[:,12], '"') == 'Subscriber'
        self.customers = np.char.strip(data[:,12], '"') == 'Customer'

        return(self.tourists, self.customers)
            
if __name__ == '__main__':
    print 'Please Wait ..'
    path = argv[1]
    cbc = CitiBikeChallenge()
    
    # Read file
    f = cbc.load_file(argv[1])
    print 'Total entries read: ',f.shape[0]
    
    # Gender
    g = cbc.gender(f)
    print 'Total Male: ',g[0]
    print 'Total Female: ',g[1]
    
    # Average Ride Time
    art,start,_,_ = cbc.avg_ride_time(f)
    print 'Average Ride Time: ',art
    
    # Peak Hours
    pk = cbc.peak_hours(start)
    
    # Tourists
    utype = cbc.tourists(f)
    print 'Total New Yorkers: ',utype[0]
    print 'Total Tourists: ',utype[1]
    
    # Plotting Stuff
    fig = plt.figure()
    x_g = 0.22
    y_g = 0.5
    x_t = 0.22
    y_t = 0.5
    ap_width = 0.16*4
    ap_ind = np.arange(4)
    # For Average Peak Hours
    
    ax = fig.add_subplot(111)
    rect1 = ax.bar(np.arange(24), pk, width=ap_width/4,
                   color='#3F5D7D',edgecolor=None, alpha=1)
    ax.set_xlabel('Hour of the Day')
    ax.set_xticks(np.arange(pk.shape[0]))
    ax.set_xlim(right = pk.shape[0])
    ax.axis('tight')
    ax.grid(color='grey', linestyle='--', linewidth=1, alpha=0.2)
    ax.set_ylabel('Number of People')
    ax.set_title('Peak Hour for January 2014')
    
    # Avg Peak Hours
    #ax = fig.add_subplot(111)
    ap1 = ax.bar(ap_ind[0], np.average(pk[0:6]), width=ap_width,
                 color='red', edgecolor=None, alpha=0.7)

    ap2 = ax.bar(ap_ind[1]+ap_width, np.average(pk[6:12]), width=ap_width,
                 color='blue', edgecolor=None, alpha=0.7)

    ap3 = ax.bar(ap_ind[2]+ap_width*2, np.average(pk[12:18]), width=ap_width,
                 color='green', edgecolor=None, alpha=0.7)

    ap4 = ax.bar(ap_ind[3]+ap_width*3, np.average(pk[18:24]), width=ap_width,
                 color='black', edgecolor=None, alpha=0.7)

    #ax.set_xticks(ap_ind+ap_width)
    #ax.set_xticklabels(('0- 6am', '6- 12noon', '12- 6pm', 
    #                    '6- 12am'))
    '''
    def autolabel(aps):
        for ap in aps:
            h = ap.get_height()
            ax.text(ap.get_x()+ap.get_width()/2., 1.05*h, '%d'%int(h),
                    ha='center', va='bottom')
    '''
    #autolabel(ap1)
    #autolabel(ap2)
    #autolabel(ap3)
    #autolabel(ap4)

    # For Gender
    '''
    bx = fig.add_subplot(211)
    rect2 = bx.bar(np.arange(2)+0.3, g, 0.3, color='#3F5D7D', 
                   edgecolor=None, alpha=0.7)
    bx.set_xlabel('Gender')
    bx.set_ylabel('Number of people')
    bx.set_title('Rides by Men vs Women')
    bx.grid(color='grey', linestyle='--', linewidth=1, alpha=0.2)
    bx.set_xlim([0, 2])
    bx.set_ylim(top = 1.02 * f.shape[0])
    bx.axes.get_xaxis().set_visible(False)
    bx.tick_params(labelsize=8)
    bx.text(x_g, y_g, 'Male', horizontalalignment='center',
            verticalalignment='center', color='#303030',
            weight='ultralight', rotation='horizontal', transform=bx.transAxes)
    bx.text(x_g, y_g-0.2, np.sum(g[0]), horizontalalignment='center',
            verticalalignment='center', color='#303030',
            weight='ultralight', rotation='horizontal', transform=bx.transAxes)
    
    bx.text(x_g+0.5, y_g, 'Female', horizontalalignment='center',
            verticalalignment='center', color='#303030',
            weight='ultralight', rotation='horizontal', transform=bx.transAxes)
    bx.text(x_g+0.5, y_g-0.2, np.sum(g[1]), horizontalalignment='center',
            verticalalignment='center', color='#303030',
            weight='ultralight', rotation='horizontal', transform=bx.transAxes)
    '''

    # For Tourists
    '''
    cx = fig.add_subplot(212)
    rect3 = cx.bar(np.arange(2)+0.3, utype, 0.3, color='#3F5D7D',
                   edgecolor=None, alpha=0.7)
    cx.set_xlabel('Types of Customers')
    cx.set_ylabel('Number of Customers')
    cx.set_title('Tourists vs Residents')
    cx.grid(color='grey', linestyle='--', linewidth=1, alpha=0.2)
    cx.set_xlim([0, 2])
    cx.set_ylim(top = 1.02 * f.shape[0])
    cx.axes.get_xaxis().set_visible(False)
    cx.tick_params(labelsize=8)
    cx.text(x_t, y_t, 'New \nYorkers', horizontalalignment='center',
            verticalalignment='center', color='#303030',
            weight='ultralight', rotation='horizontal', transform=cx.transAxes)
    cx.text(x_t, y_t-0.2, utype[0], horizontalalignment='center',
            verticalalignment='center', color='#303030',
            weight='ultralight', rotation='horizontal', transform=cx.transAxes)
    
    cx.text(x_t+0.5, y_t, 'Tourists', horizontalalignment='center',
            verticalalignment='center', color='#303030',
            weight='ultralight', rotation='horizontal', transform=cx.transAxes)
    cx.text(x_t+0.5, y_t-0.2, utype[1], horizontalalignment='center',
            verticalalignment='center', color='#303030',
            weight='ultralight', rotation='horizontal', transform=cx.transAxes)
    '''

    # Show it!
    plt.show()
    
