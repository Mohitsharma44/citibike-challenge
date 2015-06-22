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
        print 'Calculating usage per hours ...'
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
