import pandas
import numpy as np

def write_base_trx(init,fname):
    ts = init.time
    cs = init.callsign
    actype = 'B733'
    origin = 'K'+init.origin
    dest = 'KPHX'
    lat = init.latitude
    lon = init.longitude
    alt = 0.13
    spd = init.tas
    hdg = init.heading
    cent = 'ZOA'
    sect = 'ZOA46'

    wpts = ".RW01R.SSTIK3.LOSHN..BOILE..BLH.HYDRR1.I07R.RW07R."

    f = open('{}.trx'.format(fname),"w+")
    f.write('TRACK_TIME {}\n'.format(ts.asm8.astype(np.int64)//10**9))
    f.write('TRACK {} {} {} {} {} {} {} {} {}\n'.format(cs,actype,lat*10**4,abs(lon*10**4),int(spd),alt,int(hdg),cent,sect))
    f.write('    FP_ROUTE {}.<>{}<>.{}\n'.format(origin,wpts,dest))
    f.close()
    
    f = open('{}_mfl.trx'.format(fname),"w+")
    f.write('{} 330\n'.format(cs))
    f.close()
