
# TO DO make plot animated

import datetime 
import spiceypy
import numpy as np
import matplotlib.pyplot as plt

from kernel_manager import kernels_load

class FirstKepler:
    def __init__(self):
        #spicepy needs a kernels loaded to work properly
        self.kernels_path = ['./kernels/lsk/naif0012.tls.txt',
                        './kernels/pck/pck00010.tpc.txt',
                        './kernels/spk/de440s.bsp']

        kernels_load(self.kernels_path)

        #Initialization of UTC time
        self.init_utc_time = datetime.datetime(year=2000, month=1, day=1,
                                        hour=0, minute=0, second=0)

        #how many days between end of calculations and initialization time
        self.days_diff = 40000
        self.end_utc_time = self.init_utc_time + datetime.timedelta(days=self.days_diff)

        #Convert dates to strings
        self.init_utc_time_str = self.init_utc_time.strftime('%Y-%m-%dT%H:%M:%S')
        self.end_utc_time_str = self.end_utc_time.strftime('%Y-%m-%dT%H:%M:%S')

        #Print the starting and end times
        print(f"Start day: {self.init_utc_time_str}")
        print(f"End day: {self.end_utc_time_str}")

        #Ephemeris time 
        self.init_et_time = spiceypy.utc2et(self.init_utc_time_str)
        self.end_et_time = spiceypy.utc2et(self.end_utc_time_str)

        #create numpy array with one day interval between start and end day
        self.time_array = np.linspace(self.init_et_time, self.end_et_time, self.days_diff) 

        #Array with all positions of solar system barycentre
        self.solar_system_barycentre_pos = []

        for time in self.time_array:
            _position, _ =spiceypy.spkgps(targ=0, et=time, ref ='ECLIPJ2000',
                                        obs = 10)
            self.solar_system_barycentre_pos.append(_position)

        #convert to numpy array
        self.solar_system_barycentre_pos = np.array(self.solar_system_barycentre_pos)

        #import sun radius
        _, sun_radius_arr = spiceypy.bodvcd(bodyid=10, item='RADII', maxn=3)
        self.sun_radius = sun_radius_arr[0]

        #Scalled solar system barycentre position (in Sun radii)
        self.solar_system_barycentre_pos_scalled = self.solar_system_barycentre_pos/self.sun_radius

        #Plotting trajectory of solar system barycentre (only needed x and y coordinates)
        self.solar_system_barycentre_pos_scalled_plane = self.solar_system_barycentre_pos_scalled[:, 0:2]

    def trajectory(self):
        plt.style.use('dark_background')

        fig, ax = plt.subplots(figsize=(15, 10))

        #Begin with plotting the sun
        sun_plot = plt.Circle((0.0, 0.0), 1.0, color='yellow')
        ax.add_artist(sun_plot)
        ax.plot(self.solar_system_barycentre_pos_scalled_plane[:, 0], 
                self.solar_system_barycentre_pos_scalled_plane[:, 1],
                color='green')
        ax.grid(True, linewidth=0.5, linestyle='dashed', alpha=0.7)
        ax.set_aspect('equal')
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)


        ax.set_xlabel('x in sun radius')
        ax.set_ylabel('y in sun radius')
        plt.title('Trajectory of solar system barycentrum')

        plt.show()

if __name__ == "__main__":
    first_kepler = FirstKepler()
    first_kepler.trajectory()
