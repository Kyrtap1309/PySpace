import datetime
import spiceypy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates

from utilities import kernels_load

class Venus:
    def __init__(self):
        self.kernels_path = ['./kernels/lsk/naif0012.tls.txt',
                        './kernels/pck/pck00010.tpc.txt',
                        './kernels/spk/de440s.bsp']
        
        kernels_load(self.kernels_path)

        #Initialization of UTC time interval
        self.init_utc_time = datetime.datetime(year=2001, month=3, day=13,
                                        hour=0, minute=0, second=0)
        
        self.end_utc_time = datetime.datetime(year=2001, month=11, day=25,
                                        hour=0, minute=0, second=0)
        
        self.init_utc_time_str = self.init_utc_time \
            .strftime('%Y-%m-%dT%H:%M:%S')
        
        self.end_utc_time_str = self.end_utc_time \
            .strftime('%Y-%m-%dT%H:%M:%S')
        
        #Initialization of ET time interval
        self.init_et_time = spiceypy.utc2et(self.init_utc_time_str)
        self.end_et_time = spiceypy.utc2et(self.end_utc_time_str)

        #Time interval in seconds is pause in calculating next
        #phase angel
        self.time_interval = np.arange(self.init_et_time, self.end_et_time,
                                       3600) 
        
        #Creating a pandas dataframe to store calculations and parameters
        self.planets_dataframe = pd.DataFrame()

        #Column with ET times
        self.planets_dataframe.loc[:, 'ETs'] = self.time_interval
        
        #column with Utc times
        self.planets_dataframe.loc[:, 'UTCs'] = \
            self.planets_dataframe['ETs'].apply(lambda x:
                                        spiceypy.et2datetime(et=x))
        #Compute an angle between Venus and Sun when we measure it from Earth
        self.planets_dataframe.loc[:, 'Earth_Venus_Sun_Angle'] = \
            self.planets_dataframe['ETs'].apply(lambda x:
                                        np.degrees(spiceypy.phaseq(
                                            et=x,
                                            target='399', #earth NAIF id
                                            illmn='10', #sun NAIF ID
                                            obsrvr='299', #venus NAIF id
                                            abcorr='LT+S',#Correction because of 
                                            #finite light speed
                                            )))
        #Compute an angle between the Venus and the Moon when we measure it from Earth
        self.planets_dataframe.loc[:, 'Earth_Venus_Moon_Angle'] = \
            self.planets_dataframe['ETs'].apply(lambda x:
                                        np.degrees(spiceypy.phaseq(
                                            et=x,
                                            target='399', #earth NAIF id
                                            illmn='301', #moon NAIF ID
                                            obsrvr='299', #venus NAIF id
                                            abcorr='LT+S', #Correction because of 
                                            #finite light speed
                                            )))
        self.planets_dataframe.loc[:, 'Earth_Moon_Sun_Angle'] = \
            self.planets_dataframe['ETs'].apply(lambda x:
                                        np.degrees(spiceypy.phaseq(
                                            et=x,
                                            target='399', #earth NAIF id
                                            illmn='10', #sun NAIF ID
                                            obsrvr='301', #venus NAIF id
                                            abcorr='LT+S',#Correction because of 
                                            #finite light speed
                                            )))
        #Now is needed to make a column which inform us when we can take a photo of
        #a constelation of Venus, Mars and Sun. It is possible when:
        #Moon -- Venus angle < 10 degrees
        #Moon -- Sun angle > 30 degrees
        #Venus -- Sun angle > 30 degrees
        self.planets_dataframe.loc[:,'photo-able'] = \
            self.planets_dataframe.apply(lambda x: 1 if ( \
                                        x['Earth_Venus_Moon_Angle'] < 10.0 ) \
                                        and (x['Earth_Moon_Sun_Angle'] > 30.0) \
                                        and (x['Earth_Venus_Sun_Angle'] > 30.0)\
                                        else 0, axis = 1
                                        )
    def __str__(self):
        """Quick info about computed hours and hours when we can take a photo"""
        info1 = f"Number of hours computed: {len(venus.planets_dataframe)}" + \
                f" (around {round(len(venus.planets_dataframe) / 24)} days)"
        info2 = f"""Number of hours when we can take a photo: {len(venus.planets_dataframe.loc
                                                   [venus.planets_dataframe['photo-able'] == 1])}""" \
                + f" (around {round(len(venus.planets_dataframe.loc[venus.planets_dataframe['photo-able'] == 1]) / 24)} days)" 
    
        return info1+'\n'+info2
    
    def plot(self):
        plt.style.use('dark_background')

        fig, ax =plt.subplots(figsize=(12,8))

        #plotting angles in function of time
        ax.plot(self.planets_dataframe['UTCs'], self.planets_dataframe['Earth_Venus_Sun_Angle'],
                color='yellow', label='Sun and Venus Angle')
        
        ax.plot(self.planets_dataframe['UTCs'], self.planets_dataframe['Earth_Moon_Sun_Angle'],
        color='blue', label='Sun and Moon Angle')

        ax.plot(self.planets_dataframe['UTCs'], self.planets_dataframe['Earth_Venus_Moon_Angle'],
        color='silver', label='Venus and Moon Angle')

        ax.set_facecolor('navy')

        ax.set_xlabel('Dates')
        ax.set_ylabel('Angles')

        fig.set_facecolor('#1E2A4C')

        ax.grid(True, linewidth=0.5, linestyle='dashed', alpha=0.7)

        ax.set_xlim(min(self.planets_dataframe['UTCs']), max(self.planets_dataframe['UTCs']))
        ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
        ax.xaxis.set_minor_locator(matplotlib.dates.DayLocator())

        ax.legend(fancybox=True, loc='upper right', framealpha=1)

        for photogenic_date in self.planets_dataframe.loc[self.planets_dataframe['photo-able'] == 1]['UTCs']:
            ax.axvline(photogenic_date, color='green', alpha=0.1)
        
        plt.xticks(rotation = 45)
        plt.show()
        
if __name__ =='__main__':
    venus = Venus()
    print(venus.__str__())
    venus.plot()
    

        
         
        

             



