import spiceypy
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utilities import kernels_load
from utilities import NAIF_PLANETS_ID

class Map:
    def __init__(self):
        self.kernels_path = ['./kernels/lsk/naif0012.tls.txt',
                        './kernels/pck/pck00010.tpc.txt',
                        './kernels/spk/de440s.bsp']
        
        kernels_load(self.kernels_path)

        #Initialization of UTC time 
        self.utc_time_str = datetime.datetime.now() \
            .strftime('%Y-%m-%dT%H:%M:%S')
        
        #Initialization of ET time 
        self.et_time = spiceypy.utc2et(self.utc_time_str)

        #Creating a pandas dataframe to store calculations and parameters
        self.map_dataframe = pd.DataFrame()

        #Column with UTC and ET time
        self.map_dataframe.loc[:, 'ET'] = [self.et_time]
        self.map_dataframe.loc[:, 'UTC'] = [self.utc_time_str]

        for planets_name in NAIF_PLANETS_ID.keys():
            #Calculation of earth - planet vector coordinates
            self.map_dataframe.loc[:, f"{planets_name}-earth_vector"] = \
            self.map_dataframe['ET'].apply(lambda x: spiceypy.spkezp(
                                        targ=NAIF_PLANETS_ID[planets_name],
                                        et=x,
                                        ref='ECLIPJ2000',
                                        abcorr='LT+S',
                                        obs=399)[0])
            
            #Calculation of longtitude and latitude in relation to ECLIPJ2000
            #of planet
            self.map_dataframe.loc[:, f"{planets_name}_longtitude"] = \
            self.map_dataframe[f"{planets_name}-earth_vector"].apply(
                                    lambda x: spiceypy.recrad(x)[1])
            
            self.map_dataframe.loc[:, f"{planets_name}_latitude"] = \
            self.map_dataframe[f"{planets_name}-earth_vector"].apply(
                                    lambda x: spiceypy.recrad(x)[2])
            
            #Convertion of longtitude angles to be able to plot them 
            #in matplotlib - range from 0 to 2pi rads must be convert from -90
            # to 90 degrees

            
            self.map_dataframe.loc[:, f"{planets_name}_latitude_plt"] = \
            self.map_dataframe[f"{planets_name}_longtitude"].apply(
                                    lambda x: -1*((x % np.pi) - np.pi) \
                                        if x > np.pi else -1 * x)
            
    
    def plot_map(self):
        plt.style.use('dark_background')

        plt.figure(figsize=(12,8))

        plt.subplot(projection="aitoff")
        
        plt.xlabel("Longtitude")
        plt.ylabel("Latitude")

        plt.grid(True)

        plt.show()

if __name__ == '__main__':
    map = Map()
    map.plot_map()
            






        
        
        
        
    