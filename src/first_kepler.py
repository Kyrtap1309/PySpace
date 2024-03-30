import datetime 
import spiceypy
import numpy as np

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


