import pylab as pl

def loadlist(ipt):
    lines = open(ipt, 'r')
    lines = map(lambda x: float(x.strip()), lines)
    return lines
    
def plot():
    list_file = ['email/nmi/I2lmd0.txt',\
                 'email/nmi/I2lmd0.5.txt',\
                 'email/nmi/I2lmd1.txt', \
                 'email/nmi/I2lmd5.txt', \
                 'email/nmi/I2lmd10.txt']
    list_file = ['email/nmi/I2lmd0.txt',\
                 'email/nmi/I2lmd0.0.txt']
    list_data = []
    for f in list_file:
        list_data.append(loadlist(f))
    x = range(1, len(list_data[0])+1)
    pl.plot(x, list_data[0], '-r', label='lmd=0')
    pl.plot(x, list_data[1], '-g', label='lmd=0.0')
    '''
    pl.plot(x, list_data[0], '-r', label='lmd=0.0')
    pl.plot(x, list_data[1], '-g', label='lmd=0.5')
    pl.plot(x, list_data[2], '-b', label='lmd=1.0')
    pl.plot(x, list_data[3], '-m', label='lmd=5')
    pl.plot(x, list_data[4], '-k', label='lmd=10')
    '''
    pl.xlabel('Time Slice')
    pl.ylabel('NMI')
    pl.legend(loc='lower right')
    pl.ylim(0.5,1)
    pl.savefig('nmi.png', format='png')
    
if __name__ == '__main__':
    plot()
