import spiceypy
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utilities import kernels_load
from utilities import NAIF_PLANETS_ID
from utilities import PLANETS_COLOR
from utilities import PLANETS_SIZE


class Map:
    def __init__(self):
        self.kernels_path = ['./kernels/lsk/naif0012.tls.txt',
                        './kernels/pck/pck00010.tpc.txt',
                        './kernels/spk/de440s.bsp']
        
        kernels_load(self.kernels_path)

        #Initialization of UTC time 
        self.utc_time_str = datetime.datetime(year=2013, month=3, day=13,
                                        hour=0, minute=0, second=0) \
            .strftime('%Y-%m-%dT%H:%M:%S')
        
        #Initialization of ET time 
        self.et_time = spiceypy.utc2et(self.utc_time_str)

        #Initizalization of planets and ecliptic coordinates
        #at the map
        self.map_init()
        self.ecliptic_init()

       
    def map_init(self):
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

            
            self.map_dataframe.loc[:, f"{planets_name}_longtitude_plt"] = \
            self.map_dataframe[f"{planets_name}_longtitude"].apply(
                                    lambda x: -1*((x % np.pi) - np.pi) \
                                        if x > np.pi else -1 * x)
    
    def ecliptic_init(self):
        #Creating a pandas dataframe to store calculations and parameters
        self.ecliptic_dataframe = pd.DataFrame()

        #Ecliptic longs and lats coordinates (we will calculate vector of ecliptic plane
        #for constant latitude)
        self.ecliptic_dataframe.loc[:, 'Ecliptic_longtitudes'] = np.linspace(0, 
                                                            2*np.pi, 200) 
        
        self.ecliptic_dataframe.loc[:, 'Ecliptic_latitudes'] = np.pi/2.0 

        self.ecliptic_dataframe.loc[:, 'Ecliptic_direction'] = self.ecliptic_dataframe.apply(
                                                lambda x: spiceypy.sphrec(r=1,
                                                            colat=x['Ecliptic_latitudes'],
                                                            lon=x['Ecliptic_longtitudes']),
                                                axis=1)

        #Transformation from ecliptic to equator coordinates 
        ecl_to_equ = spiceypy.pxform(fromstr='ECLIPJ2000',
                                          tostr='J2000',
                                          et=self.et_time)
        
        self.ecliptic_dataframe.loc[:, 'Equator_direction'] = \
            self.ecliptic_dataframe['Ecliptic_direction'].apply(lambda x: ecl_to_equ.dot(x))
        
        self.ecliptic_dataframe.loc[:, 'Equator_long'] = \
            self.ecliptic_dataframe['Equator_direction'].apply(
                                    lambda x: spiceypy.recrad(x)[1])
        
        self.ecliptic_dataframe.loc[:,'Equator_long_plt'] = \
            self.ecliptic_dataframe['Equator_long'].apply(
                                    lambda x: -1*((x % np.pi) - np.pi) \
                                        if x > np.pi else -1 * x)
        
        self.ecliptic_dataframe.loc[:,'Equator_lat'] = \
            self.ecliptic_dataframe['Equator_direction'].apply(
                                    lambda x: spiceypy.recrad(x)[2])
        



    
    def plot_map(self):
        plt.style.use('dark_background')

        plt.figure(figsize=(12,8))

        plt.subplot(projection="aitoff")

        plt.title(f'{self.utc_time_str}')

        for planet_name in NAIF_PLANETS_ID.keys():
            plt.plot(self.map_dataframe[f"{planet_name}_longtitude_plt"],
                     self.map_dataframe[f"{planet_name}_longtitude"],
                     color = PLANETS_COLOR[planet_name],
                     marker = 'o',
                     markersize = PLANETS_SIZE[planet_name],
                     label =planet_name.capitalize(),
                     linestyle='None')

        plt.plot(self.ecliptic_dataframe['Equator_long_plt'],
                 self.ecliptic_dataframe['Equator_lat'],
                 linestyle='None',
                 marker = '_',
                 markersize=2,
                 label = 'Ecliptic',
                 color = 'tab:red')
                

        plt.xlabel("Longtitude")
        plt.ylabel("Latitude")

        plt.legend(loc = 'upper right', bbox_to_anchor=[1.1,1.1],
                   prop = {'size': 10})

        plt.grid(True)

        plt.show()

if __name__ == '__main__':
    map = Map()
    map.plot_map()
            






        
        
        
        
    