# TO DO make it object oriented
# TO DO make plot animated

import datetime 
import spiceypy
import numpy as np
import matplotlib.pyplot as plt

from kernel_manager import kernels_load

#spicepy needs a kernels loaded to work properly
kernels_path = ['./kernels/lsk/naif0012.tls.txt',
                './kernels/pck/pck00010.tpc.txt',
                './kernels/spk/de440s.bsp']

kernels_load(kernels_path)

#Initialization of UTC time
init_utc_time = datetime.datetime(year=2000, month=1, day=1,
                                  hour=0, minute=0, second=0)

#how many days between end of calculations and initialization time
days_diff = 40000
end_utc_time = init_utc_time + datetime.timedelta(days=days_diff)

#Convert dates to strings
init_utc_time_str = init_utc_time.strftime('%Y-%m-%dT%H:%M:%S')
end_utc_time_str = end_utc_time.strftime('%Y-%m-%dT%H:%M:%S')

#Print the starting and end times
print(f"Start day: {init_utc_time_str}")
print(f"End day: {end_utc_time_str}")

#Ephemeris time 
init_et_time = spiceypy.utc2et(init_utc_time_str)
end_et_time = spiceypy.utc2et(end_utc_time_str)

#create numpy array with one day interval between start and end day
time_array = np.linspace(init_et_time, end_et_time, days_diff) 

#Array with all positions of solar system barycentre
solar_system_barycentre_pos = []

for time in time_array:
    _position, _ =spiceypy.spkgps(targ=0, et=time, ref ='ECLIPJ2000',
                                  obs = 10)
    solar_system_barycentre_pos.append(_position)

#convert to numpy array
solar_system_barycentre_pos = np.array(solar_system_barycentre_pos)

#import sun radius
_, sun_radius_arr = spiceypy.bodvcd(bodyid=10, item='RADII', maxn=3)
sun_radius = sun_radius_arr[0]

#Scalled solar system barycentre position (in Sun radii)
solar_system_barycentre_pos_scalled = solar_system_barycentre_pos/sun_radius

#Plotting trajectory of solar system barycentre (only needed x and y coordinates)
solar_system_barycentre_pos_scalled_plane = solar_system_barycentre_pos_scalled[:, 0:2]

plt.style.use('dark_background')

fig, ax = plt.subplots(figsize=(15, 10))

#Begin with plotting the sun
sun_plot = plt.Circle((0.0, 0.0), 1.0, color='yellow')
ax.add_artist(sun_plot)
ax.plot(solar_system_barycentre_pos_scalled_plane[:, 0], 
        solar_system_barycentre_pos_scalled_plane[:, 1],
        color='green')
ax.grid(True, linewidth=0.5, linestyle='dashed', alpha=0.7)
ax.set_aspect('equal')
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)


ax.set_xlabel('x in sun radius')
ax.set_ylabel('y in sun radius')
plt.title('Trajectory of solar system barycentrum')


plt.show()

