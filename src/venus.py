import datetime
import spiceypy
import numpy as np
import pandas as pd

from utilities import kernels_load

class Venus:
    def __init__(self):
        self.kernels_path = ['./kernels/lsk/naif0012.tls.txt',
                        './kernels/pck/pck00010.tpc.txt',
                        './kernels/spk/de440s.bsp']
        
        kernels_load(self.kernels_path)

        #Initialization of UTC time interval
        self.init_utc_time = datetime.datetime(year=2020, month=1, day=1,
                                        hour=0, minute=0, second=0)
        
        self.end_utc_time = datetime.datetime(year=2020, month=6, day=1,
                                        hour=0, minute=0, second=0)
        
        self.init_utc_time_str = self.init_utc_time \
            .strftime('%Y-%m-%d%H:%M:%S')
        
        self.end_utc_time_str = self.end_utc_time \
            .strftime('%Y-%m-%d%H:%M:%S')
        
        self.init_et_time = spiceypy.utc2et(self.init_utc_time_str)
        self.end_et_time = spiceypy.utc2et(self.end_utc_time_str)

                



